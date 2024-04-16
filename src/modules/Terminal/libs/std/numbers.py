"""Numbers related commands."""

from ...locals import Action


def calc(args: list[str]) -> list[Action]:
    """Calculate a math expression.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    output = str(eval(" ".join(args)))  # TODO: REMOVE EVAL
    return [Action("terminal.output", [output])]


def convert(args: list[str]) -> list[Action]:
    """Convert numbers to another unit.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    num, to = args
    try:
        num = int(num)
    except ValueError:
        return [Action("terminal.output", ["Invalid number"])]
    to = to.lower()

    match to:
        case "fahrenheit" | "f":
            ans = str((num * 9 / 5) + 32) + "F"
        case "kelvin" | "k":
            ans = str(num + 273.15) + "K"
        case "rankine" | "r":
            ans = str((num + 273.15) * 9 / 5) + "R"
        case _:
            ans = "Unknown unit"

    return [Action("terminal.output", [str(ans)])]


# def add(lib, num1, num2, _print=True):
#     """
#     Adds 2 numbers (int/float)
#     """
#     out = round(float(num1) + float(num2), 4)
#     if not _print:
#         return out
#     print(out)
#
#
# def sub(lib, num1, num2, _print=True):
#     """
#     Subtracts 2 numbers (int/float)
#     """
#     out = round(float(num1) - float(num2), 4)
#     if not _print:
#         return out
#     print(out)
#
#
# def mul(lib, num1, num2, _print=True):
#     """
#     Multiplies 2 numbers (int/float)
#     """
#     out = round(float(num1) * float(num2), 4)
#     if not _print:
#         return out
#     print(out)
#
#
# def div(lib, num1, num2, _print=True):
#     """
#     Divides 2 numbers (int/float)
#     """
#     out = round(float(num1) / float(num2), 4)
#     if not _print:
#         return out
#     print(out)
