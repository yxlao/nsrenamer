import re
from pathlib import Path
import subprocess

def format_file(file_path):
    cmd = ['/usr/bin/clang-format-5.0',
           '-i',
           file_path]
    subprocess.run(cmd)


def process_line(line, object_names, new_name_space):
    for object_name in object_names:
        regex = r'(?!%s)(?!%s)(?!%s)(%s)' % (f'{object_name}.h', f'"{object_name}"', f'TEST\({object_name}', object_name)
        if re.search(regex, line):
            print(regex)
            print(line.strip())
    return line


def process_file(file_path, object_names, new_name_space):
    # Read
    # print(f"Processing {file_path}")
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process
    changed = False
    processed_lines = []
    for line in lines:
        processed_line = process_line(line, object_names, new_name_space)
        processed_lines.append(processed_line)
        if processed_line != line:
            changed = True

    # Write
    with open(file_path, 'w') as f:
        for processed_line in processed_lines:
            f.write(processed_line)

    # Format
    if changed:
        format_file(file_path)


def rename_namesapce(object_names, new_name_space, include_dirs, exclude_files):
    target_files = []
    for include_dir in include_dirs:
        target_files.extend(list(include_dir.glob("**/*.cpp")))
        target_files.extend(list(include_dir.glob("**/*.h")))
    target_files = [f for f in target_files if str(f) not in exclude_files]
    for target_file in target_files:
        process_file(target_file, object_names, new_name_space)


if __name__ == "__main__":
    root_dir = Path.home() / "repo" / "Open3D"
    include_dirs = [root_dir / "src", root_dir / "examples", root_dir / "docs" / "_static" / "C++"]
    exclude_files = {
        "/home/ylao/repo/Open3D/src/Open3D/Camera/PinholeCameraIntrinsic.cpp",
        "/home/ylao/repo/Open3D/src/Open3D/Camera/PinholeCameraIntrinsic.h",
    }
    object_names = ["PinholeCameraIntrinsic", "PinholeCameraIntrinsicParameters"]
    new_name_space = "camera"

    rename_namesapce(object_names, new_name_space, include_dirs, exclude_files)
