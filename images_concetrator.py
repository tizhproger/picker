import os
import argparse as parser


parent_dir = os.getcwd()


def main(modes):
    global parent_dir

    paths = []
    folders = []
    search_generator = os.walk(parent_dir)
    for item in search_generator:
        paths.append(item)

    for address, dirs, files in paths:
        for file in files:
            if "Pics" not in address and "Gifs" not in address and "Coubs" not in address:
                folders.append(address + '\\' + file)

    if modes['a']:
        images(folders)
        gifs(folders)
        coubs(folders)
        print("All media has been moved!")
    elif modes['i']:
        images(folders)
        print("Images has been moved!")
    elif modes['g']:
        gifs(folders)
        print("Gifs has been moved!")
    elif modes['c']:
        coubs(folders)
        print("Coubs has been moved!")
    else:
        print("Choose a right mode or check the arguments!")


def images(file_paths):
    global parent_dir
    images_dir = parent_dir + "\\" + "Pics"

    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    for file in file_paths:
        if ".jpeg" in file.split('\\')[-1] or ".png" in file.split('\\')[-1]:
            os.replace(file, images_dir + '\\' + file.split('\\')[-1])
            print("Image " + file.split('\\')[-1] + " moved!")


def gifs(file_paths):
    global parent_dir
    gifs_dir = parent_dir + "\\" + "Gifs"

    if not os.path.exists(gifs_dir):
        os.mkdir(gifs_dir)

    for file in file_paths:
        if ".gif" in file.split('\\')[-1]:
            os.replace(file, gifs_dir + '\\' + file.split('\\')[-1])
            print("Gif " + file.split('\\')[-1] + " moved!")


def coubs(file_paths):
    global parent_dir
    coubs_dir = parent_dir + "\\" + "Coubs"

    if not os.path.exists(coubs_dir):
        os.mkdir(coubs_dir)

    for file in file_paths:
        if ".mp3" in file.split('\\')[-1] or ".mp4" in file.split('\\')[-1]:
            os.replace(file, coubs_dir + '\\' + file.split('\\')[-1])
            print("Coub file " + file.split('\\')[-1] + " moved!")


if __name__ == "__main__":
    args = parser.ArgumentParser(description="This script extracts images, coubs or gifs from all folders to one place!")
    args.add_argument("-i", "--i", help="Extract only images", action='store_true')
    args.add_argument("-g", "--g", help="Extract only gifs",
                      action='store_true')
    args.add_argument("-c", "--c", help="Extract only coubs",
                      action='store_true')
    args.add_argument("-a", "--a", help="Extract all", action='store_true')

    arguments = args.parse_args()

    main(vars(arguments))
