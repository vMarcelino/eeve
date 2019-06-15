import os


def run(path: str, return_full_path: bool = False):
    """Gets all files and folders from a path and stores them into $file_list
    
    Arguments:
        path {str} -- The path to get files and folders from
    
    Keyword Arguments:
        return_full_path {bool} -- True to return the full path of the file instead of just the file name (default: {False})
    
    Returns:
        file_list {List[str]} -- list of files and folders
    """
    result = os.listdir(path)
    if return_full_path:
        for i, f in enumerate(result):
            result[i] = os.path.join(path, f)
    return {'file_list': result}


actions = {"list dir":  run}
