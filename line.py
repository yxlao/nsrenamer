import re

enum_classes = {
    "PinholeCameraIntrinsicParameters",
    "GeometryType",
    "ColorToIntensityConversionType",
    "FilterType",
    "SearchType",
    "TSDFVolumeColorType",
    "SelectionMode",
    "TextureInterpolationOption",
    "PointColorOption",
    "MeshShadeOption",
    "MeshColorOption",
    "ImageStretchOption",
    "ColorMapOption",
    "SectionPolygonType",
    "TextColor",
    "VerbosityLevel",
    "TransformationEstimationType",
}


def process_line_one(line, object_name, namespace, verbose=False):
    if "TEST" in line:
        return line

    if "//" == line.strip()[:2]:
        return line

    if "#include" == line.strip()[:8]:
        return line

    if "PrintInfo" == line.strip()[:9] and object_name != "PrintInfo":
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

    line = re.sub(
        rf"{object_name}::{namespace}::{object_name}",
        f"{object_name}::{object_name}",
        line,
    )
    if verbose:
        print(f"[constructor    ]: {line}")

    line = re.sub(
        rf"{object_name}::~{namespace}::{object_name}",
        f"{object_name}::~{object_name}",
        line,
    )
    if verbose:
        print(f"[destructor     ]: {line}")

    for enum_class in enum_classes:
        line = re.sub(rf"{enum_class}::{namespace}::", f"{enum_class}::", line)
    if verbose:
        print(f"[enum class     ]: {line}")

    line = re.sub(rf"{namespace}::{namespace}::", f"{namespace}::", line)
    if verbose:
        print(f"[duplicate ns   ]: {line}")

    line = line.replace(f"->{namespace}::{object_name}", f"->{object_name}")
    line = line.replace(f".{namespace}::{object_name}", f".{object_name}")
    if verbose:
        print(f"[pointer fix    ]: {line}")

    if verbose:
        print()
    return line


map_object_name_to_ignored_files = {
    "CropPointCloud": {
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygon.cpp",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygon.h",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygonVolume.cpp",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygonVolume.h",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Visualizer/VisualizerWithEditing.cpp",
    },
    "CropTriangleMesh": {
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygon.cpp",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygon.h",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygonVolume.cpp",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Utility/SelectionPolygonVolume.h",
        "/home/ylao/repo/Open3D/src/Open3D/Visualization/Visualizer/VisualizerWithEditing.cpp",
    },
}


def process_line(line, object_names, namespace, file_path=None):
    new_line = line
    for object_name in object_names:
        if (
            object_name in map_object_name_to_ignored_files
            and str(file_path) in map_object_name_to_ignored_files[object_name]
        ):
            new_line = new_line
        else:
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

    # Test 4: destructor
    before = "PinholeCameraIntrinsic::~PinholeCameraIntrinsic"
    after = "camera::PinholeCameraIntrinsic::~PinholeCameraIntrinsic"
    if after != process_line_one(before, "PinholeCameraIntrinsic", "camera"):
        raise ValueError(f"Test filed for:\n {before}\n")

    # Test 5: enum class
    before = "if (!ptr || ptr->GetGeometryType() != Geometry::GeometryType::PointCloud)"
    after = "if (!ptr || ptr->GetGeometryType() != Geometry::GeometryType::PointCloud)"
    if after != process_line_one(before, "PointCloud", "geometry"):
        raise ValueError(f"Test filed for:\n {before}\n")

    # Test 6 points
    before = "source_ptr = polygon_volume->CropPointCloud(*source_ptr);"
    after = "source_ptr = polygon_volume->CropPointCloud(*source_ptr);"
    if after != process_line_one(before, "CropPointCloud", "geometry", verbose=True):
        raise ValueError(f"Test filed for:\n {before}\n")
