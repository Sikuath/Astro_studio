from pathlib import Path
import json
import shutil


# ==========================================================
# FICHIERS
# ==========================================================

CONFIG_FILE = Path("config.json")

DEFAULT_FILE = Path("config_default.json")

# ==========================================================
# PATHS
# ==========================================================

def get_path(name):

    config = load_config()

    try:

        return Path(
            config["paths"][name]
        )

    except KeyError:

        raise KeyError(
            f"Chemin absent dans config.json : {name}"
        )

# ==========================================================
# CHARGEMENT
# ==========================================================

def load_config():

    """
    Charge uniquement config.json.

    Si absent :
    création depuis config_default.json.
    """

    if not CONFIG_FILE.exists():

        restore_default()


    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# ==========================================================
# SAUVEGARDE
# ==========================================================

def save_config(config):

    """
    Ecrit directement config.json.
    Aucun historique.
    Aucun backup.
    """

    temp = Path(
        "config.tmp"
    )


    with open(
        temp,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )


    temp.replace(
        CONFIG_FILE
    )



# ==========================================================
# RESTAURATION USINE
# ==========================================================

def restore_default():

    """
    Remplace config.json
    par la configuration usine.
    """

    if not DEFAULT_FILE.exists():

        raise FileNotFoundError(
            "config_default.json introuvable."
        )


    shutil.copy2(

        DEFAULT_FILE,

        CONFIG_FILE

    )



# ==========================================================
# VALIDATION
# ==========================================================

def validate_config(config):

    required = [

        "paths",

        "ollama",

        "instruments",

        "current_setup"

    ]


    missing = []


    for key in required:

        if key not in config:

            missing.append(key)


    return missing



# ==========================================================
# CONFIG VALIDE ?
# ==========================================================

def is_config_valid():

    config = load_config()

    missing = validate_config(
        config
    )

    return len(missing) == 0