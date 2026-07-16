# ==========================================================
# Astro IA
# Client Ollama
# Analyse astrophotographique
# ==========================================================


import json
from pathlib import Path

import ollama



# ==========================================================
# CACHE DOCUMENTATION
# ==========================================================


_KNOWLEDGE_CACHE = {}



# ==========================================================
# CHARGEMENT DOCUMENT
# ==========================================================


def load_document(filename):

    """
    Charge un document Markdown Astro IA.
    """

    if filename in _KNOWLEDGE_CACHE:

        return _KNOWLEDGE_CACHE[filename]



    knowledge_dir = (

        Path(__file__)
        .resolve()
        .parents[1]
        /
        "knowledge"

    )


    file = knowledge_dir / filename



    if not file.exists():

        return f"""
DOCUMENT ABSENT :

{filename}
"""



    try:

        text = file.read_text(

            encoding="utf-8"

        )


        _KNOWLEDGE_CACHE[filename] = text


        return text



    except Exception as e:


        return f"""
ERREUR LECTURE :

{filename}

{e}
"""



# ==========================================================
# CHARGEMENT BASE CONNAISSANCES
# ==========================================================


def load_ai_knowledge(

    workflow=None,

    camera=None

):


    documents = []



    documents.append(

        """

==================================================
INTERDICTIONS ASTRO IA
DOCUMENT PRIORITAIRE ABSOLU
==================================================

"""

        +
        load_document(

            "interdictions.md"

        )

    )



    documents.append(

        """

==================================================
REGLES RAPPORT ASTRO IA
==================================================

"""

        +
        load_document(

            "regle_rapport.md"

        )

    )



    documents.append(

        """

==================================================
WORKFLOW GENERAL SIRIL
==================================================

"""

        +
        load_document(

            "workflow_siril.md"

        )

    )



    if workflow == "SHO":


        documents.append(

            """

==================================================
WORKFLOW SHO
==================================================

"""

            +
            load_document(

                "workflow_sho.md"

            )

        )



    elif workflow == "LRGB":


        documents.append(

            """

==================================================
WORKFLOW LRGB
==================================================

"""

            +
            load_document(

                "workflow_lrgb.md"

            )

        )



    documents.append(

        """

==================================================
WORKFLOW GIMP
==================================================

"""

        +
        load_document(

            "workflow_gimp.md"

        )

    )



    if camera:


        if "ASI2600" in camera.upper():


            documents.append(

                """

==================================================
CAMERA ASI2600MM PRO
==================================================

"""

                +
                load_document(

                    "asi2600mm.md"

                )

            )



    knowledge = "\n\n".join(

        documents

    )



    return knowledge[:50000]



# ==========================================================
# APPEL OLLAMA QWEN
# ==========================================================


def ask_ollama(

    model,

    acquisition,

    fov,

    simbad_data,

    workflow=None,

    vision_result=None

):


    # ------------------------------------------------------
    # SECURISATION
    # ------------------------------------------------------


    if not isinstance(

        acquisition,

        dict

    ):

        acquisition = {}



    if not isinstance(

        simbad_data,

        dict

    ):

        simbad_data = {}



    if not vision_result:


        vision_result = (

            "Aucune observation visuelle disponible."

        )



    # ------------------------------------------------------
    # CONTEXTE COMPLET
    # ------------------------------------------------------


    context = {


        "DONNEES_FITS":

            acquisition,


        "CHAMP_OPTIQUE_CALCULE":

            fov,


        "SIMBAD":

            simbad_data.get(

                "simbad",

                "Information non disponible avec les données fournies."

            ),



        "CATALOGUE_SIRIL":

            simbad_data.get(

                "objects",

                []

            ),



        "WORKFLOW":

            workflow or "Non défini",



        "OBSERVATION_VISUELLE_LLAVA":

            vision_result

    }



    knowledge = load_ai_knowledge(

        workflow,

        acquisition.get(

            "camera",

            ""

        )

    )



    # ------------------------------------------------------
    # PROMPT QWEN
    # ------------------------------------------------------


    prompt = f"""

Tu es Astro IA.

Assistant spécialisé en astrophotographie amateur.



Tu travailles uniquement avec :

- Siril
- GIMP
- caméras astronomiques
- télescopes amateurs



==================================================
HIERARCHIE ABSOLUE
==================================================


Respecter cet ordre :


1 - interdictions.md

2 - regle_rapport.md

3 - Documentation Astro IA

4 - Données FITS

5 - Calculs optiques

6 - Catalogue Siril

7 - Observation LLaVA



Une source inférieure ne peut jamais
remplacer une source supérieure.



==================================================
DOCUMENTATION ASTRO IA
==================================================


{knowledge}



==================================================
REGLES LLaVA
==================================================


LLaVA est uniquement un observateur visuel.


Il peut décrire :

- structures visibles
- gradients apparents
- couleurs visibles
- défauts visuels évidents


Il ne peut jamais fournir :

- FWHM
- HFR
- seeing
- suivi
- dérive
- tilt
- bruit scientifique
- mesure photométrique


Toute information LLaVA doit commencer par :


"Observation visuelle uniquement."



==================================================
DONNEES DISPONIBLES
==================================================


{json.dumps(context, indent=4, ensure_ascii=False)}



==================================================
FORMAT DU RAPPORT
==================================================


# 1 Données mesurées


Uniquement :

- FITS
- FOV
- catalogue Siril



# 2 Analyse technique


Uniquement les conclusions démontrables.



# 3 Observation visuelle


Utiliser uniquement LLaVA.


Commencer par :

"Observation visuelle uniquement."



# 4 Conseils traitement


Uniquement :

- Siril
- GIMP



# 5 Limites de l'analyse


Indiquer :

- mesures impossibles
- informations absentes



==================================================


INTERDICTION ABSOLUE :


Ne jamais inventer.


Ne jamais supposer la nature d'un objet
depuis son nom.


Ne jamais transformer :

- observation visuelle
- conseil
- hypothèse

en mesure scientifique.



Si une information manque :


"Information non disponible avec les données fournies."


Si une mesure est impossible :


"Non évaluable avec les données disponibles."



Répond uniquement en français.

Markdown obligatoire.

"""



    response = ollama.chat(

        model=model,


        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ],


        options={

            "temperature":0.05,

            "num_ctx":8192

        }

    )


    return response["message"]["content"]