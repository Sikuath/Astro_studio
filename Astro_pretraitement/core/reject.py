from pathlib import Path
import shutil


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