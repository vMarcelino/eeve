import random


def get_random(lst: list):
    """Returns a random item from the given list
    
    Arguments:
        lst {list} -- the list which to choose from
    
    Returns:
        result -- the randomly selected item in the list
    """
    return {'result': random.choice(lst)}


actions = {"choose random":  get_random}
