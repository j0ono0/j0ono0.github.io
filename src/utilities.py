import shutil
import os


def copy_dir(src, dst):

    dst.mkdir(parents=True, exist_ok=True)

    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            copy_dir(s, d)
        else:
            shutil.copy2(str(s), str(d))
