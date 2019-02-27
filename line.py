import re

# for object_name in object_names:
#     line = 'TEST(PinholeCameraIntrinsic, Constructor_Kinect2ColorCameraDefault) {'
#     line = 'look, "PinholeCameraIntrinsic" is good'
#     # regex = r'(?!%s|%s|%s)(%s)' % (f'{object_name}.h', f'"{object_name}"', f'TEST\({object_name}', object_name)
#     regex = r'(?!"PinholeCameraIntrinsic")(PinholeCameraIntrinsic)'
#     line_sub = re.sub(regex, f'{name_space}::{object_name}', line)
# return line

def process_line_one(line, object_name, name_space):
    print(f"[init       ]: {line}")
    line = re.sub(rf'{object_name}\b', rf'{name_space}::{object_name}', line)
    print(f"[all_replace]: {line}")
    line = re.sub(rf'{name_space}::{object_name}\.h', rf'{object_name}.h', line)
    print(f"[back_header]: {line}")
    line = re.sub(rf'"{name_space}::{object_name}"', rf'"{object_name}"', line)
    print(f"[back_quote ]: {line}")
    print()
    return line


def process_line(line, object_names, name_space):
    new_line = line
    for object_name in object_names:
        new_line = process_line_one(line, object_name, name_space)
    return new_line


if __name__ == "__main__":
    before_lines = [
        '#include <Open3D/Camera/PinholeCameraIntrinsic.h>',
        'py::class_<PinholeCameraIntrinsic> pinhole_intr(m, "PinholeCameraIntrinsic",',
        '"PinholeCameraIntrinsic");',
        'py::detail::bind_default_constructor<PinholeCameraIntrinsic>(pinhole_intr);',
        'TEST(PinholeCameraIntrinsic, GetFocalLength) {',
        'PinholeCameraIntrinsicParameters::Kinect2ColorCameraDefault)'
    ]
    after_lines = [
        '#include <Open3D/Camera/PinholeCameraIntrinsic.h>',
        'py::class_<camera::PinholeCameraIntrinsic> pinhole_intr(m, "PinholeCameraIntrinsic",',
        '"PinholeCameraIntrinsic");',
        'py::detail::bind_default_constructor<camera::PinholeCameraIntrinsic>(pinhole_intr);',
        'TEST(PinholeCameraIntrinsic, GetFocalLength) {',
        'PinholeCameraIntrinsicParameters::Kinect2ColorCameraDefault)'
    ]

    for before_line in before_lines:
        process_line_one(before_line, 'PinholeCameraIntrinsic', 'camera')

