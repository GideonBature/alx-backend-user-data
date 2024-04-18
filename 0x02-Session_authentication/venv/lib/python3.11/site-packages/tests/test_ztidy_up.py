"""Used for tidying up any changes made during testing"""
import shutil


def test_tidy_up():  # pragma: no cover
    """Delete all files and folders created during testing"""
    try:
        shutil.rmtree('config')
    except (FileNotFoundError, PermissionError):
        pass

    assert True
