def add(lib, num1, num2, _print=True):
    """
    Adds 2 numbers (int/float)
    """
    out = round(float(num1) + float(num2), 4)
    if not _print:
        return out
    print(out)


def sub(lib, num1, num2, _print=True):
    """
    Subtracts 2 numbers (int/float)
    """
    out = round(float(num1) - float(num2), 4)
    if not _print:
        return out
    print(out)


def mul(lib, num1, num2, _print=True):
    """
    Multiplies 2 numbers (int/float)
    """
    out = round(float(num1) * float(num2), 4)
    if not _print:
        return out
    print(out)


def div(lib, num1, num2, _print=True):
    """
    Divides 2 numbers (int/float)
    """
    out = round(float(num1) / float(num2), 4)
    if not _print:
        return out
    print(out)
