import os
import json
import yaml
import joblib
import base64


import cv2
from pathlib import Path
from typing import Tuple

from victimDetector import logger

from pathlib import Path
from typing import Any, List

from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from victimDetector import logger


# -------------------- YAML UTILS --------------------

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a YAML file and return its contents as ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file

    Raises:
        ValueError: If YAML file is empty

    Returns:
        ConfigBox: Parsed YAML content
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)

        if content is None:
            raise BoxValueError("YAML file is empty")

        logger.info(f"YAML file loaded successfully: {path_to_yaml}")
        return ConfigBox(content)

    except BoxValueError:
        raise ValueError("YAML file is empty")

    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e


# -------------------- DIRECTORY UTILS --------------------

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


# -------------------- JSON UTILS --------------------

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save dictionary data to a JSON file.

    Args:
        path (Path): JSON file path
        data (dict): Data to save
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load JSON file and return as ConfigBox.

    Args:
        path (Path): Path to JSON file

    Returns:
        ConfigBox: Loaded JSON data
    """
    with open(path, "r") as f:
        content = json.load(f)

    logger.info(f"JSON file loaded successfully: {path}")
    return ConfigBox(content)


# -------------------- BINARY UTILS --------------------

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save any Python object as a binary file using joblib.

    Args:
        data (Any): Object to save
        path (Path): Path to binary file
    """
    joblib.dump(data, path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load a binary file using joblib.

    Args:
        path (Path): Path to binary file

    Returns:
        Any: Loaded object
    """
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data


# -------------------- FILE SIZE UTILS --------------------

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get file size in KB.

    Args:
        path (Path): File path

    Returns:
        str: File size in KB
    """
    size_kb = round(os.path.getsize(path) / 1024, 2)
    return f"{size_kb} KB"


# -------------------- BASE64 IMAGE UTILS (API SUPPORT) --------------------

def decode_base64_image(img_string: str, output_path: Path):
    """
    Decode base64 image string and save as file.

    Args:
        img_string (str): Base64 encoded image
        output_path (Path): Output image path
    """
    image_bytes = base64.b64decode(img_string)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    logger.info(f"Image decoded and saved at: {output_path}")


def encode_image_to_base64(image_path: Path) -> bytes:
    """
    Encode an image file to base64.

    Args:
        image_path (Path): Image file path

    Returns:
        bytes: Base64 encoded image
    """
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read())

    logger.info(f"Image encoded to base64: {image_path}")
    return encoded





# -------------------- VIDEO UTILS --------------------

def validate_video_file(video_path: Path):
    """
    Validate whether the given file is a readable video.

    Args:
        video_path (Path): Path to input video
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        cap.release()
        raise ValueError(f"Unable to open video file: {video_path}")

    cap.release()
    logger.info(f"Validated video file: {video_path}")


def get_video_properties(video_path: Path) -> Tuple[int, int, int]:
    """
    Get FPS, width, and height of a video.

    Args:
        video_path (Path): Path to input video

    Returns:
        Tuple[int, int, int]: fps, width, height
    """
    cap = cv2.VideoCapture(str(video_path))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()

    logger.info(
        f"Video properties | FPS: {fps}, Width: {width}, Height: {height}"
    )
    return fps, width, height


def create_video_writer(
    output_path: Path,
    fps: int,
    frame_size: Tuple[int, int]
) -> cv2.VideoWriter:
    """
    Create a VideoWriter object for saving output video.

    Args:
        output_path (Path): Output video path
        fps (int): Frames per second
        frame_size (Tuple[int, int]): (width, height)

    Returns:
        cv2.VideoWriter
    """
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        frame_size
    )

    logger.info(f"Video writer initialized at: {output_path}")
    return writer


def generate_output_video_path(
    input_video_path: Path,
    output_dir: Path
) -> Path:
    """
    Generate output video path based on input filename.

    Args:
        input_video_path (Path): Input video
        output_dir (Path): Output directory

    Returns:
        Path: Output video path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"output_{input_video_path.name}"

    logger.info(f"Generated output video path: {output_path}")
    return output_path