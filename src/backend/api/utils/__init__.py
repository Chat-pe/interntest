



def  remove_null_keys(dictionary):
    """
    Removes all keys with null values from a dictionary.
    """
    return {k: v for k, v in dictionary.items() if v is not None}