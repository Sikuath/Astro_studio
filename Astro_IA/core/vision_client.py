# ==========================================================
# Astro IA
# Client Ollama Vision
# Analyse image astrophotographique
# ==========================================================


from pathlib import Path

import ollama



# ==========================================================
# ANALYSE IMAGE AVEC LLAVA
# ==========================================================


def analyse_image(

    image_path,

    model="llava:7b"

):


    """
    Analyse visuelle d'une preview PNG
    avec Ollama Vision.

    L'image reçue doit déjà être
    préparée par vision_preview.py.

    LLaVA ne réalise aucune mesure scientifique.
    """



    image_path = Path(

        image_path

    ).resolve()



    if not image_path.exists():


        return (

            "Image non disponible."

        )



    prompt = """

Tu es Astro IA Vision.


Tu analyses uniquement l'apparence
visuelle de cette image astrophotographique.


IMPORTANT :

Tu ne mesures jamais :

- FWHM
- HFR
- seeing
- résolution
- dérive
- tilt
- bruit scientifique
- saturation quantitative


Tu fournis uniquement une observation visuelle.


Tu peux décrire :

- structures visibles
- nébulosités apparentes
- étoiles visibles
- gradients apparents
- défauts visuels évidents


Toute réponse doit commencer par :

"Observation visuelle uniquement."


Si une information est impossible à voir :

"Non déterminable visuellement."


Ne transforme jamais une observation
en mesure scientifique.


Répond en français.

"""



    try:


        response = ollama.chat(

            model=model,


            messages=[

                {

                    "role":"user",

                    "content":prompt,


                    "images":[

                        str(image_path)

                    ]

                }

            ],


            options={

                "temperature":0.1,

                "num_ctx":4096

            }

        )



        return response["message"]["content"]



    except Exception as e:


        return (

            f"Erreur analyse vision : {e}"

        )