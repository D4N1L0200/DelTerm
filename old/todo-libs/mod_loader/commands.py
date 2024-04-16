import os
import shutil


def load_modpack(pack_name):
    source_folder = r"E:\pynative\reports\\"
    destination_folder = r"E:\pynative\account\\"

    # fetch all files
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = source_folder + file_name
        destination = destination_folder + file_name
        # move only files
        if os.path.isfile(source):
            shutil.move(source, destination)
            print("Moved:", file_name)


def main():
    os.system("cls")
    print("Minecraft mod loader loaded etc bla bla.")

    while True:
        inp = input("> ")
        if inp == "exit":
            break
        elif inp == "load":
            pack_name = inp("Modpack's name: ")
            load_modpack(pack_name)


if __name__ == "__main__":
    main()
