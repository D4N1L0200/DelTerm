from ...locals import Action


def calc(args: list[str]) -> list[Action]:
    output = str(eval(" ".join(args))) + "\n"
    return [Action("terminal.output", [output])]


def convert(args: list[str]) -> list[Action]:
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

    #     case "temperature" | "temp":
    #         match from_:
    #             # Convert 'from_' to celsius
    #             case "fahrenheit" | "f":
    #                 Cans = (num - 32) * 5 / 9
    #             case "kelvin" | "k":
    #                 Cans = num - 273.15
    #             case "rankine" | "r":
    #                 Cans = (num - 491.67) * 5 / 9
    #             case "celsius" | "c":
    #                 Cans = num
    #         match to:
    #             # Convert celsius to 'to'
    #             case "fahrenheit" | "f":
    #                 ans = (Cans * 9 / 5) + 32
    #             case "kelvin" | "k":
    #                 ans = Cans + 273.15
    #             case "rankine" | "r":
    #                 ans = (Cans + 273.15) * 9 / 5
    #             case "celsius" | "c":
    #                 ans = Cans
    #
    # if not _print:
    #     return ans
    # print(f"{ans} {to}")


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
