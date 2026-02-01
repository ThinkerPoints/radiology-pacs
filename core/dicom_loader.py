import os
import pydicom
from pydicom.dataset import FileDataset
from PySide6.QtGui import QImage,QPixmap
import numpy as np

def load_dicom_series(folder):
    files = []
    for f in os.listdir(folder):
        if f.lower().endswith(".dcm"):
            files.append(os.path.join(folder, f))

    datasets = [pydicom.dcmread(f) for f in files]
    return datasets

# def dicom_to_pixmap(ds, frame_index=0):
#     img = ds.pixel_array

#     # Multi-frame handling
#     if img.ndim == 3 and img.shape[-1] != 3:
#         # (F, H, W)
#         img = img[frame_index]

#     elif img.ndim == 4 and img.shape[-1] == 3:
#         # (F, H, W, 3)
#         img = img[frame_index]

#     # Normalize to 8-bit
#     img = img.astype(np.float32)
#     img -= img.min()
#     img /= img.max() if img.max() != 0 else 1
#     img *= 255
#     img = img.astype(np.uint8)

#     # Grayscale
#     if img.ndim == 2:
#         h, w = img.shape
#         qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)

#     # RGB
#     elif img.ndim == 3 and img.shape[2] == 3:
#         h, w, _ = img.shape
#         qimg = QImage(img.data, w, h, 3 * w, QImage.Format_RGB888)

#     else:
#         raise ValueError(f"Unsupported DICOM image shape: {img.shape}")

#     return QPixmap.fromImage(qimg.copy())


def extract_frame(pixel_array, frame_index=0):
    """
    Handles:
    (H, W)
    (H, W, 3)
    (F, H, W)
    (F, H, W, 3)
    """
    if pixel_array.ndim == 2:
        return pixel_array

    if pixel_array.ndim == 3:
        # Could be (F, H, W) or (H, W, 3)
        if pixel_array.shape[-1] == 3:
            return pixel_array  # RGB single frame
        return pixel_array[frame_index]  # multi-frame grayscale

    if pixel_array.ndim == 4:
        # (F, H, W, 3)
        return pixel_array[frame_index]

    raise ValueError(f"Unsupported DICOM pixel array shape: {pixel_array.shape}")


def normalize_to_uint8(img):
    img = img.astype(np.float32)
    min_val = img.min()
    max_val = img.max()

    if max_val > min_val:
        img = (img - min_val) / (max_val - min_val)
    else:
        img = np.zeros_like(img)

    img = (img * 255).astype(np.uint8)
    return img


def dicom_to_qimage(ds, frame_index=0):
    pixel_array = ds.pixel_array
    frame = extract_frame(pixel_array, frame_index)
    frame = normalize_to_uint8(frame)
    # frame = frame.astype(np.float32)

    if frame.ndim == 2:
        h, w = frame.shape
        bytes_per_line = w
        return QImage(frame.data, w, h, bytes_per_line, QImage.Format_Grayscale8).copy()

    if frame.ndim == 3 and frame.shape[2] == 3:
        h, w, _ = frame.shape
        bytes_per_line = 3 * w
        return QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()

    raise ValueError(f"Unsupported frame shape after extraction: {frame.shape}")


def dicom_to_pixmap(ds, frame_index=0):
    qimg = dicom_to_qimage(ds, frame_index)
    return QPixmap.fromImage(qimg)

# def load_dicom(path):
#     ds = pydicom.dcmread(path)
#     img = ds.pixel_array
#     spacing = None
#     if "PixelSpacing" in ds:
#         spacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]))
#     return ds, spacing

def load_dicom(input_obj):
    if isinstance(input_obj, FileDataset):
        ds = input_obj
    else:
        ds = pydicom.dcmread(input_obj)

    spacing = None
    if hasattr(ds, "PixelSpacing"):
        spacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]))

    return ds, spacing
    

def get_rescaled_pixels(ds):
    arr = ds.pixel_array.astype(np.float32)
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    return arr * slope + intercept


