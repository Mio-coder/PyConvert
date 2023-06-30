import sys
from itertools import chain
from json import load
from os.path import exists, isfile, sep, join, abspath
from tempfile import mkdtemp
from zipfile import ZipFile


from cv2 import imread, imwrite, VideoCapture, VideoWriter


def get_path(file):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = abspath(".")
    return join(base_path, file)


with open(get_path("fileTypesData.json")) as f:
    file_types = load(f)
file_types: dict[str, list[str]] = {k: list(map(str.lower, chain.from_iterable(v))) for k, v in file_types.items()}


def convert(what: str, where: str, do_zip: bool) -> str:
    if not exists(what):
        return f"File {what!s} does not exist"
    if not isfile(what):
        return f"Folder {what!s} is not a file"
    ext = what.split(".")[-1]
    if ext not in list(chain.from_iterable(file_types.values())):
        return f"File {what!s} does not have valid extension ({ext}) " \
               f"({', '.join(map(str.lower, map(str, file_types.values())))}))"
    ext2 = where.split(".")[-1]
    if ext2 not in list(chain.from_iterable(file_types.values())):
        return f"File {where!s} does not have valid extension ({ext2}) ({', '.join(map(str.lower, map(str, file_types.values())))}))"

    if ext in file_types["Image"]:
        image = imread(what)
        if image is None:
            return f"Could not read the image {what!s}."
        if ext2 in file_types["Video"]:
            # image -> video
            output = VideoWriter(where)
            output.write(image)
            output.release()
            return "success"
        if ext2 in file_types["Image"]:
            imwrite(where, image)
            return "success"
    if ext in file_types["Video"]:
        video = VideoCapture(str(what))
        if not video.isOpened():
            return f"Could not read the video {what!s}."
        if ext2 in file_types["Image"]:
            if not do_zip:
                frame_i = 0
                while video.isOpened():
                    ret, frame = video.read()
                    if ret:
                        imwrite(where.format(frame_i), frame)
                    else:
                        break
                    frame_i += 1
                video.release()
                return "success"
            if do_zip:
                where.split(sep)
                zip_path = where[:-1]
                image_name = where[-1:]
                image_tmp_path = mkdtemp()
                frame_i = 0
                while video.isOpened():
                    ret, frame = video.read()
                    if ret:
                        imwrite(image_tmp_path + image_name.format(frame_i), frame)
                    else:
                        break
                    frame_i += 1
                video.release()
                with ZipFile(zip_path, "w") as f:
                    for i in range(frame_i):
                        f.write(image_tmp_path + image_name.format(frame_i))
                return "success"
        if ext2 in file_types["Video"]:
            # video -> video
            output = VideoWriter(where)
            while video.isOpened():
                ret, frame = video.read()
                if ret:
                    output.write(frame)
                else:
                    break
            video.release()
            output.release()
            return "success"
    return "error"


# print(convert(r"C:\Users\oparm\Downloads\random.png", r"C:\Users\oparm\Downloads\random.jpg", False))
