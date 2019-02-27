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

    if "//" == line[:2]:
        return line

    if verbose:
        print(f"[init           ]: {line}")

    line = re.sub(rf"\b{object_name}\b", f"{namespace}::{object_name}", line)
    if verbose:
        print(f"[all_replace    ]: {line}")

    line = re.sub(rf"{namespace}::{object_name}\.h", f"{object_name}.h", line)
    if verbose:
        print(f"[back_header    ]: {line}")

    line = re.sub(rf'"{namespace}::{object_name}"', f'"{object_name}"', line)
    if verbose:
        print(f"[back_quote     ]: {line}")

    line = re.sub(rf"TEST\({namespace}::{object_name}", f"TEST({object_name}", line)
    if verbose:
        print(f"[back_quote     ]: {line}")

    line = re.sub(
        rf"class {namespace}::{object_name};",
        f"namespace {namespace} {{class {object_name};}}",
        line,
    )
    if verbose:
        print(f"[forward_declare]: {line}")

    line = re.sub(rf"{object_name}::{namespace}::{object_name}", f"{object_name}::{object_name}", line)
    if verbose:
        print(f"[constructor    ]: {line}")

    if verbose:
        print()
    return line


def process_line(line, object_names, namespace):
    new_line = line
    for object_name in object_names:
        new_line = process_line_one(new_line, object_name, namespace)
    return new_line


if __name__ == "__main__":
    # Test 0
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

    # Test 1
    before = "ReadPinholeCameraTrajectory(argv[1], trajectory);"
    after = before
    if after != process_line_one(before, "PinholeCameraTrajectory", "camera"):
        raise ValueError(f"Test filed for:\n {before}\n")

    # Test 2: forward declaration
    before = "class PinholeCameraIntrinsic;"
    after = "namespace camera {class PinholeCameraIntrinsic;}"
    if after != process_line_one(before, "PinholeCameraIntrinsic", "camera"):
        raise ValueError(f"Test filed for:\n {before}\n")

    # Test 3: constructor
    before = "PinholeCameraIntrinsic::PinholeCameraIntrinsic"
    after = "camera::PinholeCameraIntrinsic::PinholeCameraIntrinsic"
    if after != process_line_one(before, "PinholeCameraIntrinsic", "camera"):
        raise ValueError(f"Test filed for:\n {before}\n")
