# ==========================================================
# Astro IA
# Génération preview vision LLaVA
# FITS linéaire RGB -> PNG couleur
# ==========================================================


from pathlib import Path

import numpy as np

from astropy.io import fits
from PIL import Image

from core.config import load_config



# ==========================================================
# STRETCH CANAL
# ==========================================================


def stretch_channel(channel):

    """
    Stretch visuel astronomique.
    Usage uniquement affichage LLaVA.
    """

    channel = np.asarray(
        channel,
        dtype=np.float32
    )


    channel = np.nan_to_num(
        channel,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )


    low = np.percentile(
        channel,
        0.5
    )

    high = np.percentile(
        channel,
        99.7
    )


    if high <= low:

        raise ValueError(
            "Contraste impossible."
        )


    channel = np.clip(
        channel,
        low,
        high
    )


    channel = (
        channel - low
    ) / (
        high - low
    )


    stretch = 10.0


    channel = (

        np.arcsinh(
            stretch * channel
        )

        /

        np.arcsinh(
            stretch
        )

    )


    return channel



# ==========================================================
# CREATION PREVIEW
# ==========================================================


def create_vision_preview(fits_path):


    """
    Création d'une image PNG couleur
    destinée à LLaVA.

    Aucun calcul scientifique :
    - FWHM
    - HFR
    - bruit
    - photométrie
    """



    fits_path = Path(
        fits_path
    ).resolve()



    if not fits_path.exists():

        raise FileNotFoundError(
            fits_path
        )



    # ======================================================
    # DOSSIER SORTIE
    # ======================================================


    config = load_config()


    images_dir = (

        config
        .get(
            "paths",
            {}
        )
        .get(
            "images"
        )

    )


    if not images_dir:

        raise ValueError(
            "Chemin images absent du config.json"
        )



    temp_dir = (

        Path(images_dir)
        /
        "x_temp"

    )


    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    output = (

        temp_dir
        /
        "vision_preview.png"

    )



    # ======================================================
    # LECTURE FITS
    # ======================================================


    with fits.open(
        fits_path
    ) as hdul:


        data = hdul[0].data

        header = hdul[0].header



    if data is None:

        raise ValueError(
            "Aucune donnée FITS."
        )



    print("\n==============================")
    print("DEBUG FITS VISION")
    print("==============================")
    print(
        "Shape :",
        data.shape
    )
    print(
        "dtype :",
        data.dtype
    )
    print(
        "NAXIS :",
        header.get("NAXIS")
    )
    print("==============================\n")



    data = np.asarray(
        data,
        dtype=np.float32
    )



    # ======================================================
    # FITS RGB
    # ======================================================


    if data.ndim == 3 and data.shape[0] == 3:


        print(
            "FITS RGB détecté"
        )


        r = stretch_channel(
            data[0]
        )


        g = stretch_channel(
            data[1]
        )


        b = stretch_channel(
            data[2]
        )


        rgb = np.dstack(
            (
                r,
                g,
                b
            )
        )



    # ======================================================
    # MONO
    # ======================================================


    elif data.ndim == 2:


        print(
            "FITS monochrome détecté"
        )


        mono = stretch_channel(
            data
        )


        rgb = np.dstack(
            (
                mono,
                mono,
                mono
            )
        )



    else:


        raise ValueError(
            f"Format FITS non supporté : {data.shape}"
        )



    # ======================================================
    # PNG
    # ======================================================


    rgb = (

        rgb * 255

    ).clip(
        0,
        255
    ).astype(
        np.uint8
    )



    img = Image.fromarray(
        rgb,
        "RGB"
    )



    img.thumbnail(
        (
            1024,
            1024
        )
    )



    img.save(
        output,
        "PNG",
        optimize=True
    )



    print(
        "Preview couleur créée :",
        output
    )


    return output



# ==========================================================
# TEST CHARGEMENT MODULE
# ==========================================================


print(
    "vision_preview.py chargé OK"
)

print(
    "create_vision_preview disponible"
)