import shutil
import uuid
from pathlib import Path

import pytest


@pytest.fixture
def tmp_path():
    """Workspace-local replacement for pytest's tmp_path.

    The desktop sandbox can deny access to pytest-managed Windows temp dirs.
    Keeping test scratch space under the writable repository root makes the
    offline suite reproducible in this environment.
    """
    root = Path(__file__).resolve().parents[1] / "test_tmp"
    root.mkdir(exist_ok=True)
    path = root / uuid.uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
        try:
            root.rmdir()
        except OSError:
            pass
