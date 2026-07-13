from astropy.io import fits
import numpy as np
from pathlib import Path
from astropy.io import fits

def load_fits(path):
    data = fits.getdata(path).astype(np.float32)

    try:
        header = fits.getheader(path)
    except:
        header = None

    return data, header


def save_fits(path, data, header=None):
    fits.PrimaryHDU(
        data.astype(np.float32),
        header=header
    ).writeto(path, overwrite=True)

def get_reference_header(workdir, reference=None):
    """
    Retourne un header FITS astronomique propre.

    reference :
        - fichier explicite (L_linear.fit, HA_linear.fit...)
        - sinon recherche automatique
    """

    workdir = Path(workdir)

    # Si une référence est fournie
    if reference:
        reference_file = workdir / reference

    else:
        # ordre de priorité
        candidates = [
            "HA_linear.fit",
            "L_linear.fit",
            "R_linear.fit"
        ]

        reference_file = None

        for file in candidates:
            test = workdir / file

            if test.exists():
                reference_file = test
                break


    if reference_file is None or not reference_file.exists():
        raise FileNotFoundError(
            "Aucune image FITS de référence trouvée"
        )


    source = fits.getheader(reference_file)


    header = fits.Header()


    # uniquement les métadonnées astro utiles
    keep = [
        "DATE-OBS",
        "EXPTIME",
        "TELESCOP",
        "FOCALLEN",
        "XBINNING",
        "YBINNING",
        "XPIXSZ",
        "YPIXSZ",
        "INSTRUME",
        "CCD-TEMP",
        "GAIN",
        "OFFSET",
        "OBJECT",
        "SITELAT",
        "SITELONG",
        "OBJCTRA",
        "OBJCTDEC",
        "RA",
        "DEC",

        # WCS astrométrie
        "CTYPE1",
        "CTYPE2",
        "CUNIT1",
        "CUNIT2",
        "CRPIX1",
        "CRPIX2",
        "CRVAL1",
        "CRVAL2",
        "CD1_1",
        "CD1_2",
        "CD2_1",
        "CD2_2"
    ]


    for key in keep:
        if key in source:
            header[key] = source[key]


    return header
