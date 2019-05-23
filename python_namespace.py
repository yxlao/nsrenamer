from pathlib import Path
import open3d as o3d
import inspect
import importlib
import re

if __name__ == "__main__":
    root_dir = Path("/home/ylao/repo/Open3D/examples/Python")

    # List modules
    module_names = []
    for module_name in dir(o3d):
        try:
            module = importlib.import_module('.'.join(
                ["open3d", "open3d", module_name]))
            if inspect.ismodule(module):
                module_names.append(module_name)
        except:
            pass
    print(module_names)

    # Build rename map
    map_obj_name_to_full_obj_name = dict()
    for module_name in module_names:
        module = importlib.import_module('.'.join(
            ["open3d", "open3d", module_name]))
        class_names = [
            name for name in dir(module)
            if inspect.isclass(getattr(module, name))
        ]
        function_names = [
            name for name in dir(module)
            if inspect.isbuiltin(getattr(module, name))
        ]
        obj_names = class_names + function_names

        for obj_name in obj_names:
            full_obj_name = '.'.join(["o3d", module_name, obj_name])
            map_obj_name_to_full_obj_name[obj_name] = full_obj_name

    def process_line(src_line):
        dst_line = src_line
        for obj_name, full_obj_name in map_obj_name_to_full_obj_name.items():
            dst_line = re.sub(r'\b%s\b' % obj_name, full_obj_name, dst_line)
        return dst_line

    def process_file(file_path):
        # Read
        # print(f"Processing {file_path}")
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Process
        changed = False
        processed_lines = []
        for line in lines:
            processed_line = process_line(line)
            # if processed_line != line:
            #     print("From:", line.strip())
            #     print("To  :", processed_line.strip())
            processed_lines.append(processed_line)

        # Write
        with open(file_path, "w") as f:
            for processed_line in processed_lines:
                f.write(processed_line)

    for file_path in root_dir.glob('**/*.py'):
        process_file(file_path)
