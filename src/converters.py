import pydicom
import numpy as np
from PIL import Image
from pathlib import Path

def dcm_to_jpg(
    dcm_path: str | Path,
    jpg_path: str | Path,
    window_center: int = -600,
    window_width: int  = 1600,
    output_size: tuple[int, int] = (1024, 1024)
) -> None:
    """
    Read a DICOM file, apply a lung-window (window center/width), 
    convert to 8-bit, resize, and save as JPG.

    Parameters
    ----------
    dcm_path : str or Path
        Path to the input .dcm file.
    jpg_path : str or Path
        Path where the .jpg will be written.
    window_center : int
        Window Level (center) in Hounsfield units.
    window_width : int
        Window Width in Hounsfield units.
    output_size : (width, height)
        Desired pixel dimensions of the output image.
    """
    dcm_path = Path(dcm_path)
    jpg_path = Path(jpg_path)
    # Load DICOM
    ds = pydicom.dcmread(str(dcm_path))
    arr = ds.pixel_array.astype(np.int16)

    # Apply rescale if present
    intercept = getattr(ds, "RescaleIntercept", 0)
    slope     = getattr(ds, "RescaleSlope", 1)
    arr = arr * slope + intercept

    # Window‐level transform
    lo = window_center - window_width // 2
    hi = window_center + window_width // 2
    arr = np.clip(arr, lo, hi)
    arr = ((arr - lo) / (hi - lo) * 255).astype(np.uint8)

    # Convert to PIL image and resize
    img = Image.fromarray(arr)
    img = img.resize(output_size, Image.LANCZOS)

    # Ensure output directory exists
    jpg_path.parent.mkdir(parents=True, exist_ok=True)
    # Save as JPEG
    img.save(str(jpg_path), format="JPEG", quality=95)