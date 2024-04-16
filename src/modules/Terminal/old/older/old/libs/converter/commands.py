def convert(lib, type, num, from_, to, _print=True):
    """
    Converts numbers to another type.
    """
    num = int(num)
    match type:
        case "temperature" | "temp":
            match from_:
                # Convert 'from_' to celsius
                case "fahrenheit" | "f":
                    Cans = (num - 32) * 5 / 9
                case "kelvin" | "k":
                    Cans = num - 273.15
                case "rankine" | "r":
                    Cans = (num - 491.67) * 5 / 9
                case "celsius" | "c":
                    Cans = num
            match to:
                # Convert celsius to 'to'
                case "fahrenheit" | "f":
                    ans = (Cans * 9 / 5) + 32
                case "kelvin" | "k":
                    ans = Cans + 273.15
                case "rankine" | "r":
                    ans = (Cans + 273.15) * 9 / 5
                case "celsius" | "c":
                    ans = Cans
                    
    if not _print:
        return ans
    print(f"{ans} {to}")
	