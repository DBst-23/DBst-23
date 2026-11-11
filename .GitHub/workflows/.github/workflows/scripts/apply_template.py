import sys, shutil, os, pathlib

def copy_tree(src, dst):
    src = pathlib.Path(src)
    dst = pathlib.Path(dst)
    for root, dirs, files in os.walk(src):
        rel = pathlib.Path(root).relative_to(src)
        for d in dirs:
            (dst / rel / d).mkdir(parents=True, exist_ok=True)
        for f in files:
            s = pathlib.Path(root) / f
            t = dst / rel / f
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, t)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: apply_template.py <template_dir> <dest_dir>")
        sys.exit(2)
    template_dir, dest_dir = sys.argv[1], sys.argv[2]
    copy_tree(template_dir, dest_dir)
    print(f"[charlotte] copied {template_dir} -> {dest_dir}")
