# ==========================================================
# Astro IA
# Génération preview vision LLaVA
# FITS linéaire -> PNG affichage
# ==========================================================

from pathlib import Path

import numpy as np
from astropy.io import fits
from PIL import Image

from core.config import load_config


# ==========================================================
# CREATION PREVIEW
# ==========================================================

def create_vision_preview(fits_path):
    """
    Conversion d'un FITS astronomique linéaire
    en PNG destiné uniquement à LLaVA.

    Cette image est uniquement une visualisation.

    Le FITS original reste inchangé.

    Aucun calcul scientifique :

    - pas de FWHM
    - pas de HFR
    - pas de photométrie
    - pas de mesure de bruit
    """

    fits_path = Path(fits_path).resolve()

    if not fits_path.exists():
        raise FileNotFoundError(fits_path)

    # ======================================================
    # DOSSIER TEMPORAIRE
    # ======================================================

    config = load_config()

    images_dir = (
        config
        .get("paths", {})
        .get("images")
    )

    if not images_dir:
        raise ValueError(
            "Chemin 'images' absent du config.json."
        )

    images_dir = Path(images_dir)

    temp_dir = images_dir / "x_temp"

    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output = temp_dir / "vision_preview.png"

    # ======================================================
    # LECTURE FITS
    # ======================================================

    with fits.open(fits_path) as hdul:

        header = hdul[0].header
        data = hdul[0].data

        print("\n==============================")
        print("DIAGNOSTIC FITS")
        print("==============================")
        print("Shape :", data.shape)
        print("Type  :", data.dtype)
        print("NAXIS :", header.get("NAXIS"))
        print("NAXIS1:", header.get("NAXIS1"))
        print("NAXIS2:", header.get("NAXIS2"))
        print("NAXIS3:", header.get("NAXIS3"))
        print("BAYERPAT :", header.get("BAYERPAT"))
        print("BAYERPAT2:", header.get("BAYERPAT2"))
        print("COLORSPC :", header.get("COLORSPC"))
        print("==============================\n")

    if data is None:
        raise ValueError(
            "Aucune donnée image dans le FITS."
        )

    # ======================================================
    # SUPPRESSION DES DIMENSIONS INUTILES
    # ======================================================

    while data.ndim > 2:
        data = data[0]

    data = np.asarray(
        data,
        dtype=np.float32
    )

    # ======================================================
    # NETTOYAGE
    # ======================================================

    data = np.nan_to_num(
        data,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    low = np.percentile(
        data,
        0.5
    )

    high = np.percentile(
        data,
        99.7
    )

    if high <= low:
        raise ValueError(
            "Impossible de créer le contraste."
        )

    data = np.clip(
        data,
        low,
        high
    )

    data = (
        data - low
    ) / (
        high - low
    )

    # ======================================================
    # STRETCH ASINH
    # ======================================================

    stretch = 10.0

    data = (
        np.arcsinh(
            stretch * data
        )
        /
        np.arcsinh(stretch)
    )

    # ======================================================
    # CONVERSION PNG
    # ======================================================

    image = (
        data * 255
    ).astype(np.uint8)

    img = Image.fromarray(
        image,
        mode="L"
    )

    img.thumbnail(
        (
            1024,
            1024
        )
    )

    img.save(
        output,
        format="PNG",
        optimize=True
    )

    print(f"Preview enregistrée : {output}")

    return output