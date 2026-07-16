# ==========================================================
# Astro IA
# Client Ollama Vision
# Analyse image astrophotographique
# ==========================================================


from pathlib import Path
import tempfile

import ollama
from astropy.io import fits
import numpy as np
from PIL import Image



# ==========================================================
# CREATION PREVIEW PNG POUR VISION
# ==========================================================


def create_vision_preview(

    fits_path,

    size=1024

):

    """
    Convertit un FITS en PNG léger
    destiné à LLaVA Vision.

    Le fichier temporaire est créé
    dans x_temp.
    """



    fits_path = Path(
        fits_path
    ).resolve()



    if not fits_path.exists():

        return None



    # dossier temporaire Astro IA

    temp_dir = (

        fits_path.parents[1]

        /

        "x_temp"

    )


    temp_dir.mkdir(

        exist_ok=True

    )



    output = (

        temp_dir

        /

        f"{fits_path.stem}_vision.png"

    )



    try:


        # lecture FITS

        with fits.open(

            fits_path

        ) as hdul:


            data = hdul[0].data



        if data is None:

            return None



        # nettoyage

        data = np.nan_to_num(

            data

        )



        # normalisation percentile

        p_low = np.percentile(

            data,

            1

        )


        p_high = np.percentile(

            data,

            99

        )



        data = np.clip(

            data,

            p_low,

            p_high

        )



        data = (

            (data - p_low)

            /

            (p_high - p_low)

            *

            255

        )



        data = data.astype(

            np.uint8

        )



        image = Image.fromarray(

            data

        )



        # redimensionnement

        image.thumbnail(

            (

                size,

                size

            )

        )



        image.save(

            output,

            format="PNG"

        )



        return output



    except Exception as e:


        print(

            f"Erreur création preview vision : {e}"

        )


        return None





# ==========================================================
# ANALYSE IMAGE AVEC LLAVA
# ==========================================================


def analyse_image(

    image_path,

    model="llava:7b"

):


    """
    Analyse visuelle d'une image
    astrophotographique avec Ollama Vision.

    LLaVA reçoit uniquement une preview PNG.

    Il ne réalise aucune mesure scientifique.
    """



    image_path = Path(

        image_path

    ).resolve()



    if not image_path.exists():

        return (

            "Image non disponible."

        )



    # ------------------------------------------------------
    # CREATION IMAGE LEGERE
    # ------------------------------------------------------


    preview = create_vision_preview(

        image_path

    )



    if preview is None:


        return (

            "Impossible de créer une image de visualisation."

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
- bruit réel
- saturation quantitative


Tu fournis uniquement une observation visuelle.


Tu peux décrire :

- structures visibles
- répartition apparente du signal
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

                    "role": "user",

                    "content": prompt,


                    "images":[

                        str(preview)

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