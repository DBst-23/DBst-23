import sys, shutil, os, pathlib

DEFAULT_SRC = "templates/api_runner"
DEFAULT_DST = "."

def copy_tree(src, dst):
    src = pathlib.Path(src)
    dst = pathlib.Path(dst)
    for root, dirs, files in os.walk(src):
        rel = pathlib.Path(root).relative_to(src)
        dest_dir = dst / rel
        dest_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            shutil.copy2(pathlib.Path(root) / file, dest_dir / file)

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_SRC
    dst = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_DST
    print(f"[charlotte] copying from {src} to {dst} ...")
    copy_tree(src, dst)
    print("[charlotte] done.")
