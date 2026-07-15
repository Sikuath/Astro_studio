from pathlib import Path
import json
import shutil
from datetime import datetime


# ==========================================================
# FICHIERS
# ==========================================================

CONFIG_FILE = Path("config.json")
DEFAULT_FILE = Path("config_default.json")
BACKUP_DIR = Path("backups")


# ==========================================================
# CREATION DOSSIER BACKUP
# ==========================================================

BACKUP_DIR.mkdir(exist_ok=True)


# ==========================================================
# CHARGEMENT
# ==========================================================

def load_config():

    """
    Charge config.json.
    Si le fichier n'existe pas,
    il est automatiquement recréé
    depuis config_default.json.
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
    Sauvegarde la configuration.
    Une copie est créée automatiquement.
    """

    backup_config()

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# BACKUP
# ==========================================================

def backup_config():

    """
    Sauvegarde horodatée
    avant modification.
    """

    if not CONFIG_FILE.exists():
        return

    now = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    destination = (
        BACKUP_DIR /
        f"config_{now}.json"
    )

    shutil.copy2(
        CONFIG_FILE,
        destination
    )


# ==========================================================
# RESTAURATION USINE
# ==========================================================

def restore_default():

    """
    Copie config_default.json
    vers config.json
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

    """
    Vérifie les rubriques
    essentielles.
    """

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
# CONFIGURATION VALIDE ?
# ==========================================================

def is_config_valid():

    """
    Retourne True
    si la configuration est correcte.
    """

    config = load_config()

    missing = validate_config(
        config
    )

    return len(missing) == 0