from pathlib import Path
import shutil
import re

# =====================================================
# Rejet d'une image
# =====================================================

def reject_file(file, rejected_folder):
    """
    Déplace une image vers le dossier Rejected.
    """

    file = Path(file)
    rejected_folder = Path(rejected_folder)

    rejected_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = rejected_folder / file.name

    shutil.move(
        str(file),
        str(destination)
    )


# =====================================================
# Restauration d'une image
# =====================================================

def restore_file(file, lights_folder):
    """
    Replace une image du dossier Rejected
    vers le dossier Lights.
    """

    file = Path(file)
    lights_folder = Path(lights_folder)

    lights_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = lights_folder / file.name

    shutil.move(
        str(file),
        str(destination)
    )


# =====================================================
# Vidage du dossier Rejected
# =====================================================
def check_trash_folder(trash_folder):
    """
    Vérifie si un dossier Lights_trash contient des fichiers.

    Retourne :
    - True si des fichiers sont présents
    - False sinon
    """

    trash = Path(trash_folder)

    if not trash.exists():
        return False

    for item in trash.iterdir():

        if item.is_file():

            return True

    return False

def clear_trash_folder(trash_folder):
    """
    Vide complètement le dossier Lights_trash.
    """

    trash = Path(trash_folder)

    if not trash.exists():
        return 0


    deleted = 0


    for item in trash.iterdir():

        try:

            if item.is_file():

                item.unlink()
                deleted += 1


            elif item.is_dir():

                shutil.rmtree(item)
                deleted += 1


        except Exception:

            pass


    return deleted

def clear_rejected_folder(rejected_folder):
    """
    Supprime tout le contenu du dossier Rejected.
    Le dossier est recréé s'il n'existe pas.
    """

    rejected_folder = Path(rejected_folder)

    rejected_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    deleted = 0

    for item in rejected_folder.iterdir():

        try:

            if item.is_file() or item.is_symlink():

                item.unlink()
                deleted += 1

            elif item.is_dir():

                shutil.rmtree(item)
                deleted += 1

        except Exception:
            pass

    return deleted

def extract_target_name(filename):

    name = Path(filename).stem

    match = re.search(
        r"Light_([^_]+)",
        name
    )

    if match:
        return match.group(1)

    return None
