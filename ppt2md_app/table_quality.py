import re
from dataclasses import dataclass
from typing import Literal


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class TableQualityIssue:
    code: str
    severity: Severity
    message: str
    evidence: str | None = None

    def to_dict(self):
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class TableQualityResult:
    reliable: bool
    row_count: int
    column_counts: list[int]
    errors: list[TableQualityIssue]
    warnings: list[TableQualityIssue]

    def to_dict(self):
        return {
            "reliable": self.reliable,
            "row_count": self.row_count,
            "column_counts": self.column_counts,
            "errors": [issue.to_dict() for issue in self.errors],
            "warnings": [issue.to_dict() for issue in self.warnings],
        }


def assess_table_markdown(text: str) -> TableQualityResult:
    rows = _table_rows(text)
    errors: list[TableQualityIssue] = []
    warnings: list[TableQualityIssue] = []
    if not rows:
        errors.append(_issue("table_empty", "error", "表格 block 没有可解析的行。"))
        return TableQualityResult(False, 0, [], errors, warnings)

    cells = [_split_cells(row) for row in rows]
    column_counts = [len(row_cells) for row_cells in cells]
    separator_index = _separator_row_index(cells)

    if separator_index is None:
        errors.append(_issue("table_separator_missing", "error", "Markdown 表格缺少分隔行。", rows[0]))
    elif separator_index != 1:
        warnings.append(_issue("table_separator_position", "warning", "Markdown 表格分隔行不在表头之后。", rows[separator_index]))

    expected_columns = column_counts[0] if column_counts else 0
    if expected_columns < 2:
        errors.append(_issue("table_too_few_columns", "error", "表格列数少于 2，无法可靠确认行列关系。", rows[0]))

    if any(count != expected_columns for count in column_counts):
        errors.append(
            _issue(
                "table_column_mismatch",
                "error",
                "Markdown 表格行列数不一致。",
                ", ".join(str(count) for count in column_counts),
            )
        )

    if separator_index is not None:
        body_rows = cells[separator_index + 1 :]
        if not body_rows:
            warnings.append(_issue("table_shell", "warning", "表格只有表头和分隔行，没有数据行。"))
        if _header_missing(cells[0]):
            warnings.append(_issue("table_header_missing", "warning", "表格表头为空或缺失。", rows[0]))
        if _mostly_empty_body(body_rows):
            warnings.append(_issue("table_body_empty", "warning", "表格主体大多为空。"))

    garbled_ratio = _garbled_ratio(rows)
    if garbled_ratio >= 0.25:
        warnings.append(
            _issue(
                "table_garbled_text",
                "warning",
                "表格疑似包含较多乱码或不确定字符。",
                f"garbled_ratio={garbled_ratio:.2f}",
            )
        )

    reliable = not errors and not any(
        issue.code in {"table_shell", "table_body_empty", "table_garbled_text"} for issue in warnings
    )
    return TableQualityResult(reliable, len(rows), column_counts, errors, warnings)


def is_probably_markdown_table(text: str) -> bool:
    rows = _table_rows(text)
    return len(rows) >= 2 and any(_is_separator_cells(_split_cells(row)) for row in rows)


def _table_rows(text: str) -> list[str]:
    rows = []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            continue
        if "|" in stripped:
            rows.append(stripped)
    return rows


def _split_cells(row: str) -> list[str]:
    stripped = row.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _separator_row_index(rows: list[list[str]]) -> int | None:
    for index, row in enumerate(rows):
        if _is_separator_cells(row):
            return index
    return None


def _is_separator_cells(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def _header_missing(cells: list[str]) -> bool:
    return not any(cell.strip() for cell in cells)


def _mostly_empty_body(rows: list[list[str]]) -> bool:
    if not rows:
        return False
    total = sum(len(row) for row in rows)
    empty = sum(1 for row in rows for cell in row if not cell.strip())
    return total > 0 and empty / total >= 0.75


def _garbled_ratio(rows: list[str]) -> float:
    text = "".join(rows)
    meaningful = [ch for ch in text if not ch.isspace() and ch not in "|:-"]
    if not meaningful:
        return 0.0
    garbled = sum(1 for ch in meaningful if ch in "?？�□" or ch == "\ufffd")
    return garbled / len(meaningful)


def _issue(code: str, severity: Severity, message: str, evidence: str | None = None) -> TableQualityIssue:
    return TableQualityIssue(code=code, severity=severity, message=message, evidence=evidence)
