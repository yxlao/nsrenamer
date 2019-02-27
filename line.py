import re

def process_line(line, object_names, name_space):
    return line

    # for object_name in object_names:
    #     line = 'TEST(PinholeCameraIntrinsic, Constructor_Kinect2ColorCameraDefault) {'
    #     line = 'look, "PinholeCameraIntrinsic" is good'
    #     # regex = r'(?!%s|%s|%s)(%s)' % (f'{object_name}.h', f'"{object_name}"', f'TEST\({object_name}', object_name)
    #     regex = r'(?!"PinholeCameraIntrinsic")(PinholeCameraIntrinsic)'
    #     line_sub = re.sub(regex, f'{name_space}::{object_name}', line)
    # return line


if __name__ == '__main__':
    pass
