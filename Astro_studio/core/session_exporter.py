from pathlib import Path
from datetime import datetime
import json

from astropy.io import fits

from core.config import load_config


# ==========================================================
# Détection du mode
# ==========================================================

def detect_mode(workdir):

    workdir = Path(workdir)

    hasL = (workdir / "L_linear.fit").exists()
    hasR = (workdir / "R_linear.fit").exists()
    hasG = (workdir / "G_linear.fit").exists()
    hasB = (workdir / "B_linear.fit").exists()

    hasHA = (workdir / "HA_linear.fit").exists()
    hasO = (workdir / "OIII_linear.fit").exists()
    hasS = (workdir / "SII_linear.fit").exists()


    if hasHA and hasO and hasS and not hasL:

        return "SHO"


    if hasHA and hasO and hasS and hasL:

        return "LSHO"


    if hasL and hasR and hasG and hasB:

        return "LRGB"


    return "UNKNOWN"



# ==========================================================
# Liste des couches
# ==========================================================

def get_layers(mode):


    if mode == "SHO":

        return [

            "HA_linear.fit",
            "OIII_linear.fit",
            "SII_linear.fit"

        ]



    if mode == "LSHO":

        return [

            "L_linear.fit",
            "HA_linear.fit",
            "OIII_linear.fit",
            "SII_linear.fit"

        ]



    if mode == "LRGB":

        return [

            "L_linear.fit",
            "R_linear.fit",
            "G_linear.fit",
            "B_linear.fit"

        ]


    return []



# ==========================================================
# Lecture header FITS
# ==========================================================

def read_header(file):

    return fits.getheader(file)



# ==========================================================
# Informations couche
# ==========================================================

def layer_infos(file):


    h = read_header(file)


    return {


        "stack":

            int(

                h.get(
                    "STACKCNT",
                    1
                )

            ),



        "livetime":

            float(

                h.get(

                    "LIVETIME",

                    h.get(
                        "EXPTIME",
                        0
                    )

                )

            ),



        "unit":

            float(

                h.get(
                    "EXPTIME",
                    0
                )

            ),



        "filter":

            h.get(

                "FILTER",

                Path(file).stem

            )

    }



# ==========================================================
# Analyse session complète
# ==========================================================

def collect_session(workdir):


    workdir = Path(workdir)


    mode = detect_mode(workdir)


    files = get_layers(mode)



    if not files:

        raise RuntimeError(

            "Aucune combinaison SHO / LSHO / LRGB détectée."

        )



    session = {}

    reference = None


    total_stack = 0

    total_live = 0



    for f in files:


        path = workdir / f



        if not path.exists():

            continue



        info = layer_infos(path)



        session[f] = info



        total_stack += info["stack"]

        total_live += info["livetime"]



        if reference is None:

            reference = read_header(path)



    return {


        "mode": mode,

        "layers": session,

        "reference": reference,

        "total_stack": total_stack,

        "total_livetime": total_live

    }

def update_rgb_header(workdir):

    workdir = Path(workdir)

    session = collect_session(workdir)

    rgb = workdir / "RGB_final.fit"

    if not rgb.exists():
        print("RGB_final.fit introuvable.")
        return

    with fits.open(rgb, mode="update") as hdul:

        hdr = hdul[0].header

        hdr["LIVETIME"] = (
            session["total_livetime"],
            "Temps integration total (s)"
        )

        hdr["STACKCNT"] = (
            session["total_stack"],
            "Nombre total de poses"
        )

        hdul.flush()

# ==========================================================
# Export JSON Astro IA
# ==========================================================

def export_session_json(workdir, output_dir):


    workdir = Path(workdir)
    output_dir = Path(output_dir)


    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    session = collect_session(workdir)

    ref = session["reference"]


    now = datetime.now()


    filename = (
        "astro_session_"
        +
        now.strftime("%Y%m%d_%H%M%S")
        +
        ".json"
    )


    json_file = output_dir / filename



    data = {


        "created":

            now.isoformat(),


        "mode":

            session["mode"],



        "project":

            ref.get(
                "OBJECT",
                "Unknown"
            ),



        "camera":

            ref.get(
                "INSTRUME",
                ""
            ),



        "telescope":

            ref.get(
                "TELESCOP",
                ""
            ),



        "focal_length":

            ref.get(
                "FOCALLEN",
                0
            ),



        "gain":

            ref.get(
                "GAIN",
                ""
            ),



        "offset":

            ref.get(
                "OFFSET",
                ""
            ),



        "ccd_temp":

            ref.get(
                "CCD-TEMP",
                ""
            ),



        "ra":

            ref.get(
                "RA",
                ""
            ),



        "dec":

            ref.get(
                "DEC",
                ""
            ),



        "total_stack":

            session["total_stack"],



        "total_livetime":

            session["total_livetime"],



        "layers":

            session["layers"]

    }



    with open(

        json_file,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )


    print(
        f"✔ Session JSON créée : {json_file}"
    )


    return json_file

# ==========================================================
# Fonction principale
# ==========================================================

def run_session_export(

        workdir,

        output_dir

):

    """
    Lance :
    - analyse des couches linear
    - mise à jour RGB_final.fit
    - export astro_session JSON
    """

    update_rgb_header(workdir)

    return export_session_json(

        workdir,

        output_dir

    )



# ==========================================================
# Chargement configuration Astro Studio
# ==========================================================

def load_astro_config():

    """
    Lecture du config.json Astro Studio
    """

    config_file = Path(
        "config.json"
    )


    if not config_file.exists():

        raise FileNotFoundError(
            "config.json Astro Studio introuvable"
        )


    with open(

        config_file,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)



# ==========================================================
# Export depuis configuration Astro Studio
# ==========================================================

def run_from_config():

    """
    Utilisation normale depuis Astro Studio

    Aucun chemin manuel.
    """

    config = load_astro_config()



    # dossier principal traitement

    workdir = Path(

        config.get(

            "workdir",

            ""

        )

    )



    if not workdir.exists():

        raise FileNotFoundError(

            f"Dossier travail absent : {workdir}"

        )



    # dossier partagé Astro IA

    output_dir = (

        workdir

        /

        "x_projects"

        /

        "data_sessions"

    )



    print(
        "================================="
    )

    print(
        " Astro Session Export"
    )

    print(
        "================================="
    )


    print(

        f"Projet : {workdir}"

    )


    print(

        f"Sortie JSON : {output_dir}"

    )



    return run_session_export(

        workdir,

        output_dir

    )



# ==========================================================
# TEST AUTONOME
# ==========================================================

if __name__ == "__main__":


    try:


        json_file = run_from_config()


        print()

        print(
            "✔ Export terminé"
        )

        print(
            json_file
        )



    except Exception as e:


        print()

        print(
            "❌ Erreur export session"
        )

        print(
            e
        )