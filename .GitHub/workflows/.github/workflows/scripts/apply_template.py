import sys, shutil, os, pathlib

def copy_tree(src, dst):
    src = pathlib.Path(src)
    dst = pathlib.Path(dst)
    for root, dirs, files in os.walk(src):
        rel = pathlib.Path(root).relative_to(src)
        dest_dir = dst / rel
        dest_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            shutil.copy2(src / file, dest_dir / file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python apply_template.py <source_dir> <destination_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    destination_dir = sys.argv[2]

    print(f"Copying from {source_dir} to {destination_dir}...")
    copy_tree(source_dir, destination_dir)
    print("Template application complete ✅")
