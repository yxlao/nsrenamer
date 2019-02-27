from pathlib import Path
import subprocess
from line import process_line
import tempfile
from shutil import copyfile
from pprint import pprint
import re


def format_file(file_path):
    cmd = ["/usr/bin/clang-format-5.0", "-i", file_path]
    subprocess.run(cmd)


def git_reset(root_dir):
    cmd = ["git", "-C", str(root_dir), "reset", "--hard", "HEAD"]
    subprocess.run(cmd)


def process_file(file_path, object_names, namespace):
    # Read
    # print(f"Processing {file_path}")
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Process
    changed = False
    processed_lines = []
    for line in lines:
        processed_line = process_line(
            line, object_names, namespace, file_path=file_path
        )
        processed_lines.append(processed_line)
        if processed_line != line:
            changed = True
            # print(f"[Changed] {file_path}\n{line.strip()}\n{processed_line.strip()}\n")
    print(f"[Changed] {file_path}")

    # Write
    with open(file_path, "w") as f:
        for processed_line in processed_lines:
            f.write(processed_line)

    # Format
    if changed:
        format_file(file_path)


def rename_namespace(
    object_names, namespace, include_dirs, exclude_files, reset_only=False
):
    print("[exclude_files]")
    pprint(exclude_files)
    print("[object_names]")
    pprint(object_names)
    print("[namespace]")
    print(namespace)

    with tempfile.TemporaryDirectory() as temp_dir:
        for exclude_file in exclude_files:
            temp_exclude_file = Path(temp_dir + exclude_file)
            temp_exclude_file.parent.mkdir(parents=True, exist_ok=True)
            copyfile(exclude_file, temp_exclude_file)
        git_reset(root_dir)
        for exclude_file in exclude_files:
            temp_exclude_file = Path(temp_dir + exclude_file)
            copyfile(temp_exclude_file, exclude_file)

    if reset_only:
        return

    target_files = []
    for include_dir in include_dirs:
        target_files.extend(list(include_dir.glob("**/*.cpp")))
        target_files.extend(list(include_dir.glob("**/*.h")))
    target_files = [f for f in target_files if str(f) not in exclude_files]
    for target_file in target_files:
        process_file(target_file, object_names, namespace)


def glob_cpp_and_h_in_folder(foder_path):
    files = list(foder_path.glob("**/*.cpp"))
    files.extend(list(foder_path.glob("**/*.h")))
    files = [str(f) for f in files]
    return files


def glob_h_in_folder(foder_path):
    files = list(foder_path.glob("**/*.h"))
    files = [str(f) for f in files]
    return files


def camel_to_snake(name):
    # https://stackoverflow.com/a/1176023/1255535
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


if __name__ == "__main__":
    root_dir = Path.home() / "repo" / "Open3D"
    include_dirs = [
        root_dir / "src",
        root_dir / "examples",
        root_dir / "docs" / "_static" / "C++",
    ]

    # Config: camera
    # exclude_dir = Path("/home/ylao/repo/Open3D/src/Open3D/Camera")
    # object_names = [
    #     "PinholeCameraIntrinsicParameters",
    #     "PinholeCameraIntrinsic",
    #     "PinholeCameraParameters",
    #     "PinholeCameraTrajectory",
    # ]

    # # Config: color_map
    # exclude_dir = Path("/home/ylao/repo/Open3D/src/Open3D/ColorMap")
    # object_names = [
    #     "ColorMapOptimizationOption",
    #     "ColorMapOptimization",
    #     "ColorMapOptimizationJacobian",
    #     "ComputeJTJandJTrNonRigid",
    #     "ImageWarpingField",
    #     "Project3DPointAndGetUVDepth",
    #     "CreateVertexAndImageVisibility",
    #     "QueryImageIntensity",
    #     "SetProxyIntensityForVertex",
    #     "SetGeometryColorAverage",
    # ]

    # Config: geometry
    exclude_dir = Path("/home/ylao/repo/Open3D/src/Open3D/Geometry")
    object_names = [
        "Geometry",
        "Geometry2D",
        "Geometry3D",
        # Image
        "Image",
        "CreateDepthToCameraDistanceMultiplierFloatImage",
        "PointerAt",
        "ConvertDepthToFloatImage",
        "FlipImage",
        "FilterImage",
        "FilterHorizontalImage",
        "DownsampleImage",
        "DilateImage",
        "LinearTransformImage",
        "ClipIntensityImage",
        "CreateImageFromFloatImage",
        "ImagePyramid",
        "FilterImagePyramid",
        "CreateImagePyramid",
        "CreateDepthBoundaryMask",
        # KDTree
        "KDTreeFlann",
        "KDTreeSearchParam",
        "KDTreeSearchParamKNN",
        "KDTreeSearchParamRadius",
        "KDTreeSearchParamHybrid",
        # LineSet
        "LineSet",
        # PointCloud
        "PointCloud",
        "CreatePointCloudFromDepthImage",
        "CreatePointCloudFromRGBDImage",
        "SelectDownSample",
        "VoxelDownSample",
        "VoxelDownSampleAndTrace",
        "UniformDownSample",
        "CropPointCloud",
        "RemoveRadiusOutliers",
        "RemoveStatisticalOutliers",
        "EstimateNormals",
        "OrientNormalsToAlignWithDirection",
        "OrientNormalsTowardsCameraLocation",
        "ComputePointCloudToPointCloudDistance",
        "ComputePointCloudMeanAndCovariance",
        "ComputePointCloudMahalanobisDistance",
        "ComputePointCloudNearestNeighborDistance",
        # RGBDImage
        "RGBDImage",
        "CreateRGBDImageFromColorAndDepth",
        "CreateRGBDImageFromRedwoodFormat",
        "CreateRGBDImageFromTUMFormat",
        "CreateRGBDImageFromSUNFormat",
        "CreateRGBDImageFromNYUFormat",
        "RGBDImagePyramid",
        "FilterRGBDImagePyramid",
        "CreateRGBDImagePyramid",
        # TriangleMesh
        "TriangleMesh",
        "SelectDownSample",
        "CropTriangleMesh",
        "CreateMeshBox",
        "CreateMeshSphere",
        "CreateMeshCylinder",
        "CreateMeshCone",
        "CreateMeshArrow",
        "CreateMeshCoordinateFrame",
        # VoxelGrid
        "VoxelGrid",
        "CreateSurfaceVoxelGridFromPointCloud",
    ]

    # Config: utility
    # exclude_dir = Path("/home/ylao/repo/Open3D/src/Open3D/Utility")
    # object_names = [
    #     "Timer",
    #     "ScopeTimer",
    #     "FPSTimer",
    #     "IJsonConvertible",
    #     "SplitString",
    #     "TransformVector6dToMatrix4d",
    #     "TransformMatrix4dToVector6d",
    #     "SolveLinearSystemPSD",
    #     "SolveJacobianSystemAndObtainExtrinsicMatrix",
    #     "SolveJacobianSystemAndObtainExtrinsicMatrixArray",
    #     "ComputeJTJandJTr",
    # ]

    namespace = camel_to_snake(exclude_dir.name)
    exclude_files = glob_cpp_and_h_in_folder(exclude_dir)
    rename_namespace(
        object_names, namespace, include_dirs, exclude_files, reset_only=False
    )
