# ==========================================================
# Astro IA
# Knowledge Loader
# Chargement documentation astrophotographique
# ==========================================================

from pathlib import Path


# dossier documentation

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"



# ==========================================================
# CHARGEMENT FICHIER
# ==========================================================

def load_document(filename):

    path = KNOWLEDGE_DIR / filename


    if not path.exists():

        return (
            "Information non disponible "
            "avec les données fournies."
        )


    return path.read_text(
        encoding="utf-8"
    )



# ==========================================================
# SELECTION DOCUMENTS
# ==========================================================

def get_relevant_knowledge(
    workflow=None,
    camera=None
):


    documents = []



    # règles générales

    documents.append(
        load_document(
            "regles_astro.md"
        )
    )



    # Siril toujours présent

    documents.append(
        load_document(
            "workflow_siril.md"
        )
    )



    # workflow spécifique

    if workflow == "SHO":

        documents.append(
            load_document(
                "workflow_sho.md"
            )
        )


    elif workflow == "LRGB":

        documents.append(
            load_document(
                "workflow_lrgb.md"
            )
        )



    # GIMP

    documents.append(
        load_document(
            "workflow_gimp.md"
        )
    )



    # caméra

    if camera:

        if "ASI2600" in camera:

            documents.append(
                load_document(
                    "asi2600mm.md"
                )
            )



    return "\n\n".join(
        documents
    )