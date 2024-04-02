def help_(lib, function=""):
    """
    Replies with a helpful message about the function.
    """
    try:
        eval(f"help(lib.{function})")
    except AttributeError:
        print(f"Function <{function}> not found.")