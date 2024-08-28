import pytest

from src.support_function import check_extensions_path


@pytest.mark.parametrize('path, extensions',
                         [(r'C:\test\data\test.doc', ".doc"),
                          (r'C:\test\data\test.docx', ".docx")])
def test_check_extensions_path(path, extensions):
    assert check_extensions_path(
        path=path,
        extensions=extensions
    ) == True, "Function check_extensions_path Error"
