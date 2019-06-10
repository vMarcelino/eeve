def test_credentials_check():
    import os, sys
    file_location = os.path.dirname(os.path.realpath(__file__))
    p = os.path.abspath(os.path.join(file_location, '..', 'eeve', 'eeve actions'))
    sys.path.insert(0, p)
    from eeve_GUI.Controllers.LoginController import check_credentials
    from eeve import database
    database.open_db_file(None)
    database.add_default_event()
    assert check_credentials('root', 'toor')