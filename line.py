import re

# for object_name in object_names:
#     line = 'TEST(PinholeCameraIntrinsic, Constructor_Kinect2ColorCameraDefault) {'
#     line = 'look, "PinholeCameraIntrinsic" is good'
#     # regex = r'(?!%s|%s|%s)(%s)' % (f'{object_name}.h', f'"{object_name}"', f'TEST\({object_name}', object_name)
#     regex = r'(?!"PinholeCameraIntrinsic")(PinholeCameraIntrinsic)'
#     line_sub = re.sub(regex, f'{namespace}::{object_name}', line)
# return line


def process_line_one(line, object_name, namespace, verbose=False):
    if "TEST" in line:
        return line

    if verbose:
        print(f"[init       ]: {line}")

    line = re.sub(rf"{object_name}\b", f"{namespace}::{object_name}", line)
    if verbose:
        print(f"[all_replace]: {line}")

    line = re.sub(rf"{namespace}::{object_name}\.h", f"{object_name}.h", line)
    if verbose:
        print(f"[back_header]: {line}")

    line = re.sub(rf'"{namespace}::{object_name}"', f'"{object_name}"', line)
    if verbose:
        print(f"[back_quote ]: {line}")

    line = re.sub(rf"TEST\({namespace}::{object_name}", f"TEST({object_name}", line)
    if verbose:
        print(f"[back_quote ]: {line}")
        print()

    return line


def process_line(line, object_names, namespace):
    new_line = line
    for object_name in object_names:
        new_line = process_line_one(new_line, object_name, namespace)
    return new_line


if __name__ == "__main__":
    before_lines = [
        "#include <Open3D/Camera/PinholeCameraIntrinsic.h>",
        'py::class_<PinholeCameraIntrinsic> pinhole_intr(m, "PinholeCameraIntrinsic",',
        '"PinholeCameraIntrinsic");',
        "py::detail::bind_default_constructor<PinholeCameraIntrinsic>(pinhole_intr);",
        "TEST(PinholeCameraIntrinsic, GetFocalLength) {",
        "PinholeCameraIntrinsicParameters::Kinect2ColorCameraDefault)",
    ]
    after_lines = [
        "#include <Open3D/Camera/PinholeCameraIntrinsic.h>",
        'py::class_<camera::PinholeCameraIntrinsic> pinhole_intr(m, "PinholeCameraIntrinsic",',
        '"PinholeCameraIntrinsic");',
        "py::detail::bind_default_constructor<camera::PinholeCameraIntrinsic>(pinhole_intr);",
        "TEST(PinholeCameraIntrinsic, GetFocalLength) {",
        "PinholeCameraIntrinsicParameters::Kinect2ColorCameraDefault)",
    ]

    for before, after in zip(before_lines, after_lines):
        if after != process_line_one(before, "PinholeCameraIntrinsic", "camera"):
            raise ValueError(f"Test filed for:\n {before}\n")
