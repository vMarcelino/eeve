import eeve, sys


def exit_eeve(exit_value: int = 0):
    """Exits eeve by unregistering all events
    and then calling a sys.exit with the exit code
    supplied in the argument
    
    Keyword Arguments:
        exit_value {int} -- the exxit code to return (default: {0})
    """
    print('unregistering')
    for event in eeve.events:
        event.unregister()

    print('exiting')
    sys.exit(exit_value)


actions = {'exit eeve': exit_eeve}
