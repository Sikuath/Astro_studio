from pathlib import Path
from astropy.io import fits


def read_fits_header(filepath):

    """
    Lecture du header FITS
    Retourne un dictionnaire exploitable par Astro IA
    """

    filepath = Path(filepath)

    if not filepath.exists():
        return {
            "error": "Fichier introuvable"
        }


    try:

        with fits.open(filepath) as hdul:

            header = hdul[0].header


            data = {

                # Objet
                "OBJECT":
                    header.get("OBJECT", "Inconnu"),


                # Date
                "DATE-OBS":
                    header.get("DATE-OBS", "Inconnue"),


                # Instrument
                "TELESCOP":
                    header.get("TELESCOP", "Inconnu"),


                "INSTRUME":
                    header.get("INSTRUME", "Inconnu"),


                # Optique
                "FOCALLEN":
                    header.get("FOCALLEN", "Inconnue"),


                # Caméra
                "XPIXSZ":
                    header.get("XPIXSZ", "Inconnue"),


                "YPIXSZ":
                    header.get("YPIXSZ", "Inconnue"),


                # Acquisition
                "EXPTIME":
                    header.get("EXPTIME",
                               header.get("EXPOSURE",
                               "Inconnue")),


                "GAIN":
                    header.get("GAIN", "Inconnu"),


                "OFFSET":
                    header.get("OFFSET", "Inconnu"),


                "FILTER":
                    header.get("FILTER", "Inconnu"),


                # Coordonnées
                "RA":
                    header.get("RA", "Inconnue"),


                "DEC":
                    header.get("DEC", "Inconnue"),


                # Température
                "CCD-TEMP":
                    header.get("CCD-TEMP",
                               header.get("CCD_TEMP",
                               "Inconnue"))

            }


            return data


    except Exception as e:

        return {
            "error": str(e)
        }