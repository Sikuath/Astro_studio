# ==========================================================
# Astro IA
# Client Ollama Vision
# Analyse image astrophotographique LLaVA
# ==========================================================


from pathlib import Path

import ollama



# ==========================================================
# NETTOYAGE REPONSE LLAVA
# ==========================================================

def clean_vision_result(text):

    if not text:

        return text


    text = text.replace(

        "Observation visuelle uniquement.\n",

        ""

    )


    return text.strip()





# ==========================================================
# ANALYSE IMAGE AVEC LLAVA
# ==========================================================

def analyse_image(

    image_path,

    model="llava:7b"

):


    """
    Analyse visuelle d'une image PNG
    préparée pour Ollama Vision.

    Observation uniquement.

    Aucune mesure scientifique :
    FWHM, HFR, seeing, suivi,
    bruit, photométrie ou résolution.
    """



    image_path = Path(

        image_path

    ).resolve()



    if not image_path.exists():

        return (

            "Image non disponible."

        )



    # ======================================================
    # PROMPT VISION
    # ======================================================


    prompt = """

Tu es Astro IA Vision.

Tu analyses uniquement une prévisualisation
étirée d'une image astrophotographique.

Tu n'as accès qu'à l'image.

Tu ne connais pas :

- objet
- coordonnées
- caméra
- focale
- acquisition


Ton rôle est uniquement une observation
visuelle.


Commence obligatoirement par :

Observation visuelle uniquement.



==================================================
1 - FOND DE CIEL
==================================================

Décris :

- homogénéité du fond
- gradients lumineux visibles
- zones claires ou sombres
- variations du fond


==================================================
2 - ETOILES
==================================================

Décris uniquement :

- densité apparente
- étoiles brillantes et faibles
- aspect général
- étoiles ponctuelles ou allongées


Interdiction :

Ne jamais donner :

- FWHM
- HFR
- seeing
- excentricité
- suivi
- résolution
- bruit mesuré
- photométrie


==================================================
3 - STRUCTURES ASTRONOMIQUES
==================================================

Recherche uniquement :

- amas apparent
- nébulosités
- extensions faibles
- zones sombres
- poussières apparentes


Si rien n'est clairement visible :

"Aucune structure clairement identifiable
sur cette prévisualisation."


==================================================
4 - DEFAUTS VISUELS
==================================================

Signale uniquement :

- gradients
- dominante couleur
- saturation
- artefacts
- traces


==================================================
REGLES ABSOLUES
==================================================

Tu ne réalises aucune mesure scientifique.

Tu ne détermines jamais :

- qualité acquisition
- mise au point
- seeing
- suivi
- calibration


Tu ne dois jamais identifier
un objet astronomique.


Si une information n'est pas visible :

"Non déterminable visuellement."


Réponds uniquement en français.

"""



    try:


        response = ollama.chat(

            model=model,


            messages=[

                {

                    "role": "user",

                    "content": prompt,


                    "images": [

                        str(image_path)

                    ]

                }

            ],


            options={

                "temperature":0.1,

                "num_ctx":4096

            }

        )



        result = response["message"]["content"]



        result = clean_vision_result(

            result

        )



        print(
            "=============================="
        )

        print(
            "DEBUG REPONSE LLAVA"
        )

        print(
            result
        )

        print(
            "=============================="
        )



        return result



    except Exception as e:


        return (

            f"Erreur analyse vision : {e}"

        )