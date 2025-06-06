import os
import shutil
from html_builder import generate_page

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
    print(os.getcwd())
    static_path = os.path.join("static")
    public_path = os.path.join("public")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir("public")
    copy_dir(static_path, public_path)

def main():
    stage_public()
    generate_page("content/index.md", "template.html", "public/index.html")



if __name__ == "__main__":
    main()