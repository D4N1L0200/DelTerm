def isValid(s):
    brackets = []
    for bracket in s:
        match bracket:
            case '(' | ')':
                brackets.append("p")
            case '{' | '}':
                brackets.append("c")
            case '[' | ']':
                brackets.append("s")
            case _:
                return False

    try:
        log = [brackets[0]]
    except IndexError:
        return True

    for item in brackets[1:]:
        if log:
            lastitem = log[-1]
        else:
            lastitem = False
        if item == lastitem:
            log.pop()
        else:
            log.append(item)

    return False if log else True

if __name__ == "__main__":
    while True:
        line = input(">>> ")
        if isValid(line):
            print("Valid")
        else:
            print("Invalid")