def encode(string, min_size):
    window = ""
    en_string = ""
    while len(string):
        match = False
        for i in reversed(range(len(string) - 1)):
            if string[:i] in window and i != 0:
                match = string[:i]
                l = len(match)
                d = len(window) - window.index(match)
                break
                
        if match and l > min_size:
            en_string += f"{d},{l}."
        else:
            l = 1
            en_string += string[0]

        window += string[:l]
        string = string[l:]
    return en_string

def decode(string):
    de_string = ""
    while len(string):
        try:
            int(string[0])
            comma, dot = string.index(","), string.index(".")
            shift, lenght = int(string[:comma]), int(string[comma+1:dot])
            de_string += de_string[-shift:-shift+lenght]
            string = string[dot+1:]
        except:
            de_string += string[0]
            string = string[1:]
    return de_string

def encodeFile(file_from, file_to):
    with open(file_from, "r") as ff:
        with open(file_to, "w") as ft:
            ft.write(encode(ff.read(), 1))

def decodeFile(file_from, file_to):
    with open(file_from, "r") as ff:
        with open(file_to, "w") as ft:
            ft.write(decode(ff.read()))