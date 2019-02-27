import re

def process_line(line, object_names, new_name_space):
    for object_name in object_names:
        line = 'TEST(PinholeCameraIntrinsic, Constructor_Kinect2ColorCameraDefault) {'
        line = 'look, "PinholeCameraIntrinsic" is good'
        # regex = r'(?!%s|%s|%s)(%s)' % (f'{object_name}.h', f'"{object_name}"', f'TEST\({object_name}', object_name)
        regex = r'(?!"PinholeCameraIntrinsic")(PinholeCameraIntrinsic)'
        line_sub = re.sub(regex, f'{new_name_space}::{object_name}', line)
        print(line)
        print(line_sub)
        exit(0)
    return line


if __name__ == '__main__':
    pass
