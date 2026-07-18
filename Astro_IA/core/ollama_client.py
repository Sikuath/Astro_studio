# ==========================================================
# Astro IA
# Client Ollama
#
# Analyse astrophotographique orientée traitement
#
# Gestion :
# - documentation Astro IA
# - contexte FITS
# - contexte céleste
# - vision LLaVA
# - appel Qwen
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
# BASE CONNAISSANCES ASTRO IA
# ==========================================================

def load_ai_knowledge(

    workflow=None,

    camera=None

):


    documents = []



    if workflow:

        workflow = workflow.upper()



    # ------------------------------------------------------
    # REGLES GENERALES
    # ------------------------------------------------------

    documents.append(

        load_document(

            "interdictions.md"

        )

    )



    documents.append(

        load_document(

            "regle_rapport.md"

        )

    )



    documents.append(

        load_document(

            "defauts_visuels.md"

        )

    )



    documents.append(

        load_document(

            "workflow_traitement_complet.md"

        )

    )



    documents.append(

        load_document(

            "workflow_siril.md"

        )

    )



    documents.append(

        load_document(

            "workflow_gimp.md"

        )

    )



    # ------------------------------------------------------
    # WORKFLOW SPECIALISE
    # ------------------------------------------------------

    if workflow:


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



    # ------------------------------------------------------
    # CAMERA
    # ------------------------------------------------------

    if camera:


        if "ASI2600" in camera.upper():


            documents.append(

                load_document(

                    "asi2600mm.md"

                )

            )



    return "\n\n".join(

        documents

    )[:60000]



# ==========================================================
# APPEL OLLAMA
# ==========================================================

def ask_ollama(
    model,
    acquisition,
    fov,
    simbad_data,
    workflow=None,
    vision_result=None,
    pipeline_stage="postprocess",
    astro_context=None
):


    """
    Génère un rapport Astro IA.


    Paramètres :

    acquisition :
        données FITS


    fov :
        calcul optique


    simbad_data :
        catalogue astronomique


    vision_result :
        analyse LLaVA


    astro_context :
        contexte céleste calculé
        depuis astro_context.py


    """



    if not isinstance(acquisition, dict):

        acquisition = {}



    if not isinstance(simbad_data, dict):

        simbad_data = {}



    if not isinstance(astro_context, dict):

        astro_context = {}



    if not vision_result:


        vision_result = (

            "Aucune observation visuelle disponible."

        )



    # ======================================================
    # CONTEXTE MODELE
    # ======================================================

    context = {


        "DONNEES_ACQUISITION":

            acquisition,


        "CHAMP_OPTIIQUE":

            fov,


        "CATALOGUE_SIRIL":

            simbad_data.get(

                "objects",

                []

            ),


        "CONTEXTE_CELESTE":

            astro_context or {},


        "TYPE_WORKFLOW":

            workflow or "Non défini",


        "ETAT_PIPELINE":

            pipeline_stage,


        "OBSERVATION_LLAVA":

            vision_result

    }



    knowledge = load_ai_knowledge(

        workflow,

        acquisition.get(

            "camera",

            ""

        )

    )
    # ======================================================
    # PROMPT ASTRO IA
    # ======================================================

    prompt = """

Tu es un module d'inspection visuelle pour astrophotographie.

Ta mission est uniquement de décrire les caractéristiques
visuelles présentes dans une image.

Tu analyses une prévisualisation d'image.
Tu fournis un rapport d'observation visuelle destiné
à un logiciel de traitement d'image.


Tu dois décrire uniquement :

- luminosité du fond
- variations du fond
- couleurs visibles
- aspect des étoiles
- structures lumineuses ou sombres visibles
- défauts visuels apparents


Tu ne dois pas chercher à donner un nom
ou une classification astronomique.


Ne fais aucune mesure scientifique.

Ne donne jamais :

- FWHM
- HFR
- SNR
- seeing
- excentricité mesurée
- qualité optique
- suivi mesuré


==================================================
FORMAT DE REPONSE
==================================================


1 - FOND DE CIEL

Décrire :
- homogénéité
- variations de luminosité
- variations de couleur


2 - ETOILES

Décrire :
- densité apparente
- étoiles ponctuelles ou non
- saturation visible
- halos visibles


3 - STRUCTURES VISIBLES

Décrire uniquement les formes visibles :

Exemples :

"zone diffuse visible"
"zone sombre visible"
"filament apparent"

Ne pas donner d'identification.


4 - COULEURS

Décrire uniquement les couleurs visibles :

- dominante bleue
- dominante rouge
- dominante verte
- variation de couleur


5 - DEFAUTS VISIBLES

Rechercher uniquement :

- variation du fond
- halos
- artefacts
- étoiles allongées
- saturation
- texture granuleuse

6 - RESUME

Faire un résumé de quelques lignes.


Règle principale :

Tu es un observateur visuel.

Tu décris ce que tu vois dans l'image.
Tu ne complètes pas avec des connaissances externes.

Réponds uniquement en français.

"""


    # ======================================================
    # DEBUG PROMPT
    # ======================================================

    print("==============================")
    print("PROMPT QWEN")
    print(
        "Taille caractères :",
        len(prompt)
    )
    print(
        "Nombre mots :",
        len(prompt.split())
    )
    print("==============================")



    # ======================================================
    # APPEL OLLAMA
    # ======================================================

    response = ollama.chat(

        model=model,


        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ],


        options={


            "temperature": 0.10,


            "num_ctx": 8192,


            "num_predict": 1500


        }

    )



    return response["message"]["content"]