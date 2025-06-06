import os
import shutil
import sys

from html_builder import generate_page, generate_pages_recursive


def copy_dir(src, dst):
    for fn in os.listdir(src):
        if os.path.isfile(os.path.join(src, fn)):
            shutil.copy(os.path.join(src, fn), dst)
        elif os.path.isdir(os.path.join(src, fn)):
            os.makedirs(os.path.join(dst, fn))
            fn_path = os.path.join(src, fn)
            dst_path = os.path.join(dst, fn)
            copy_dir(fn_path, dst_path)

def stage_public():
    static_path = os.path.join("static")
    public_path = os.path.join("docs")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir("docs")
    copy_dir(static_path, public_path)

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        print("basepath didnt work")
        basepath = "/"
    stage_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)




if __name__ == "__main__":
    main()