import pytest


def test_load_actions_from_path():
    import eeve
    with pytest.raises(TypeError) as e_info:
        eeve.load_actions_from_path(None)


def test_import_from_folder():
    import eeve
    with pytest.raises(TypeError) as e_info:
        eeve.importer.import_from_folder(None)