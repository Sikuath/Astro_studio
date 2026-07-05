import numpy as np
from astropy.io import fits

# =========================================================
# BASIC FITS EXPORT
# =========================================================

def save_fits(path, data, header=None):
    """
    Save a single FITS file (float32 linear data)
    """
    data = np.asarray(data, dtype=np.float32)

    hdu = fits.PrimaryHDU(data, header=header)
    hdu.writeto(path, overwrite=True)


# =========================================================
# SHO TRIPLET EXPORT (R / G / B separés)
# =========================================================

def export_sho_triplet(prefix, R, G, B, hR=None, hG=None, hB=None):
    """
    Export SHO channels as 3 FITS files.

    Output:
        prefix_R.fit
        prefix_G.fit
        prefix_B.fit
    """
    save_fits(f"{prefix}_R.fit", R, hR)
    save_fits(f"{prefix}_G.fit", G, hG)
    save_fits(f"{prefix}_B.fit", B, hB)


# =========================================================
# RGB FITS CUBE EXPORT (3D FITS)
# Shape: (3, Y, X)
# =========================================================

def export_rgb_fits(path, R, G, B, header=None):
    """
    Export RGB as a single 3-channel FITS cube.

    Format:
        (3, height, width)
    """
    rgb = np.stack([R, G, B], axis=0).astype(np.float32)

    hdu = fits.PrimaryHDU(rgb, header=header)
    hdu.writeto(path, overwrite=True)


# =========================================================
# NORMALIZATION FOR DISPLAY EXPORT (OPTIONAL PNG)
# =========================================================

def _normalize(img):
    """
    Simple astrophotography-friendly normalization
    (NOT scientific, only for preview export)
    """
    lo = np.percentile(img, 0.5)
    hi = np.percentile(img, 99.5)

    if hi - lo == 0:
        return np.zeros_like(img)

    img = (img - lo) / (hi - lo)
    return np.clip(img, 0, 1)


# =========================================================
# PNG EXPORT (quick preview sharing)
# =========================================================

def export_png(path, RGB):
    """
    Export RGB image as 8-bit PNG.

    RGB expected shape:
        (H, W, 3) in float [0..1] or linear
    """
    from PIL import Image

    img = _normalize(RGB)
    img = (img * 255).astype(np.uint8)

    Image.fromarray(img).save(path)


# =========================================================
# EXPORT FULL SHO PACKAGE (CONVENIENCE FUNCTION)
# =========================================================

def export_full_package(
    prefix,
    R, G, B,
    hR=None, hG=None, hB=None,
    export_cube=True,
    export_triplet=True,
    export_png_preview=None
):
    """
    One-click export of everything useful.
    """

    if export_triplet:
        export_sho_triplet(prefix, R, G, B, hR, hG, hB)

    if export_cube:
        export_rgb_fits(f"{prefix}_RGB.fit", R, G, B)

    if export_png_preview is not None:
        export_png(export_png_preview, np.dstack([R, G, B]))
