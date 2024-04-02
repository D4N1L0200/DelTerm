def calPoints(ops) -> int:
    record = []
    for op in ops:
        match op:
            case "C":
                record.pop()
            case "D":
                record.append(record[-1] * 2)
            case "+":
                record.append(record[-1] + record[-2])
            case _:
                record.append(int(op))

    result = 0
    for num in record:
        result += num
    return result

if __name__ == "__main__":
    line = input(">>> ")
    ops = line.strip().split()

    print(calPoints(ops))

# 5 2 3
# 5 - [5]
# 2 - [5, 2]
# 3 - [5, 2, 3]
# 10

# 5 2 3 C D +
# 5 - [5]
# 2 - [5, 2]
# 3 - [5, 2, 3]
# C - [5, 2]
# D - [5, 2, 4]
# + - [5, 2, 4, 6]
# 17