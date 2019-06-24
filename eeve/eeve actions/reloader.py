import os, eeve


def reload_events():
    """Reloads eeve events by unregistering
    current events and re-registering events in database
    """
    for event in eeve.events:
        event.unregister()

    eeve.load_events_from_db()


def reload_scripts():
    """Reloads eeve scripts from the folders and then reloads the events

    Events are reloaded so that the triggers and actions within then are
    also updated
    """
    eeve.load_actions_from_path(os.path.join(eeve.script_root, 'eeve actions'))
    eeve.load_actions_from_path(os.path.join(eeve.script_root, 'eeve plugins'))

    eeve.load_triggers_from_path(os.path.join(eeve.script_root, 'eeve triggers'))
    eeve.load_triggers_from_path(os.path.join(eeve.script_root, 'eeve plugins'))

    reload_events()


actions = {'reload scripts': reload_scripts, 'reload events': reload_events}
