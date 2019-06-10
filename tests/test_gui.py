def test_credentials_check():
    import os, sys
    file_location = os.path.dirname(os.path.realpath(__file__))
    p = os.path.abspath(os.path.join(file_location, '..', 'eeve', 'eeve actions'))
    sys.path.insert(0, p)
    from eeve_GUI.Controllers.LoginController import check_credentials
    from eeve import database
    database.open_db_file(None)
    database.add_default_event()
    session = database.Session()
    for user in session.query(database.User):
        assert check_credentials(user.login, user.password)

    session.close()

def test_create_default_data_in_database():
    from eeve import database
    import sqlalchemy

    database.open_db_file(None)

    session = database.Session()
    classes = [database.User, database.Event, database.Trigger, database.TriggerArgument, database.Action, database.ActionArgument, database.Task]
    count = 0
    for c in classes:
        count += session.query(sqlalchemy.func.count(c.id)).scalar()

    assert count == 0
    session.close()


    database.add_default_event()

    session = database.Session()
    classes = [database.User, database.Event, database.Trigger, database.TriggerArgument, database.Action, database.ActionArgument, database.Task]
    count = 0
    for c in classes:
        count += session.query(sqlalchemy.func.count(c.id)).scalar()

    assert count == 1+1+1+0+1+0+1
    session.close()