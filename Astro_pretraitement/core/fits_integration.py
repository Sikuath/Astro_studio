from pathlib import Path

from astropy.io import fits


# ==========================================================
# Analyse intégration FITS
# ==========================================================


def read_linear_header(file_path):

    """
    Lecture des informations d'intégration
    d'un fichier *_linear.fit
    """

    file_path = Path(file_path)

    if not file_path.exists():

        return None


    try:

        with fits.open(file_path) as hdul:

            header = hdul[0].header


            return {

                "file": file_path.name,

                "filter": header.get(
                    "FILTER",
                    "Unknown"
                ),

                "frames": header.get(
                    "STACKCNT",
                    0
                ),

                "livetime": header.get(
                    "LIVETIME",
                    0
                ),

                "exposure": header.get(
                    "EXPTIME",
                    0
                )

            }


    except Exception as e:

        print(
            f"Erreur lecture {file_path}: {e}"
        )

        return None




# ==========================================================
# Analyse dossier complet
# ==========================================================


def analyze_linear_files(folder):


    folder = Path(folder)


    results = []


    for file in folder.glob("*_linear.fit"):


        data = read_linear_header(file)


        if data:

            results.append(data)



    return build_summary(results)




# ==========================================================
# Construction résumé session
# ==========================================================


def build_summary(layers):


    session = {

        "layers": {},

        "total_frames": 0,

        "total_time": 0

    }


    for layer in layers:


        filt = layer["filter"]


        session["layers"][filt] = {

            "file": layer["file"],

            "frames": layer["frames"],

            "livetime": layer["livetime"],

            "exposure": layer["exposure"]

        }


        session["total_frames"] += int(
            layer["frames"]
        )


        session["total_time"] += float(
            layer["livetime"]
        )



    return session