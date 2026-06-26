from docpage2md_app.run_logger import RunLogger


def test_run_logger_writes_chinese_progress_messages(tmp_path, capsys):
    log_path = tmp_path / "process.log"
    logger = RunLogger(log_path, echo=True)

    logger.info("Hybrid crop vision batch start: blocks=12, workers=6")
    logger.info("Hybrid Brain batch start: pages=4, workers=4, requested_workers=60, thinking=disabled")
    logger.info("Hybrid crop vision batch done: blocks=12, succeeded=11, failed=1, elapsed=8.5s")
    logger.info("Hybrid Brain batch done: pages=4, statuses=ok:3;partial:1, elapsed=30.2s")
    logger.info("Hybrid page 2 Brain done: status=ok, ops_requested=3, applied=3, rejected=0, elapsed=12.4s")
    logger.info("Hybrid Brain latency summary: pages=4, p50=12.4s, p90=18.0s, max=19.0s, slowest=4:19.0s;2:12.4s, tail_ratio=1.53")
    logger.info("Hybrid Brain latency warning: tail_ratio=1.80, advice=try_brain_workers_3_6_12")
    logger.info("Dual parser upload PDF physically cropped: source=notes.pdf, page_ranges=5-20, pages=16, original_bytes=35651584, upload_bytes=4194304")
    logger.info("Submitting one local file to MinerU: notes.pdf upload=notes__pages_abcd.pdf (4194304 bytes)")
    logger.info("Submitting local file to PaddleOCR: notes.pdf upload=notes__pages_abcd.pdf (4194304 bytes)")
    logger.info("Markdown rendering done: pages=4, elapsed=0.2s")

    captured = capsys.readouterr()
    log_text = log_path.read_text(encoding="utf-8")

    assert "开始并行识别裁剪块：裁剪块=12，并发=6" in log_text
    assert "开始并行 Brain 精修：页数=4，实际并发=4，配置上限=60，模式=关闭思考/快速模式" in log_text
    assert "裁剪块并行识别完成：总数=12，成功=11，失败=1，耗时=8.5秒" in log_text
    assert "Brain 并行精修完成：页数=4，状态=正常:3；部分完成:1，耗时=30.2秒" in log_text
    assert "Brain 完成第 2 页：状态=正常，请求操作=3，应用=3，拒绝=0，耗时=12.4秒" in log_text
    assert "Brain 耗时分布：页数=4，p50=12.4秒，p90=18.0秒，最慢=19.0秒" in log_text
    assert "Brain 出现明显长尾：长尾系数=1.80" in log_text
    assert "双引擎解析上传 PDF 已物理裁剪：源文件=notes.pdf，页码=5-20，上传页数=16，原始大小=34.0MB，上传大小=4.0MB" in log_text
    assert "正在提交单个本地文件到 MinerU：源文件=notes.pdf，上传文件=notes__pages_abcd.pdf，大小=4.0MB" in log_text
    assert "正在提交本地文件到 PaddleOCR：源文件=notes.pdf，上传文件=notes__pages_abcd.pdf，大小=4.0MB" in log_text
    assert "Markdown 渲染完成：页数=4，耗时=0.2秒" in log_text
    assert "Hybrid crop vision batch start" not in log_text
    assert "开始并行识别裁剪块" in captured.out
