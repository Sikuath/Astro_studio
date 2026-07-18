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


    unwanted = [

        "Observation visuelle uniquement.",

        "Bonjour, je suis un modèle d'IA spécialisé dans l'analyse visuelle des images astronomiques.",

        "Bonjour, je suis un modèle d'IA spécialisé dans l'analyse visuelle des images astronomiques.",

        "Je ne peux pas accéder aux métadonnées FITS ou aux informations d'acquisition de l'image, mais je peux vous aider à décrire ce que je vois dans l'image."

    ]


    for line in unwanted:

        text = text.replace(
            line,
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

Tu es un assistant d'observation visuelle pour astrophotographie.

Observe uniquement l'image fournie.

Ton rôle est de décrire ce qu'un humain pourrait remarquer
en regardant cette image.

Ne cherche pas à identifier l'objet.
Ne donne pas de nom astronomique.
Ne fais aucune mesure scientifique.

Décris uniquement :

1. Apparence générale
- image sombre ou lumineuse
- fond uniforme ou variable
- contraste général

2. Etoiles
- nombreuses ou peu nombreuses
- ponctuelles ou légèrement déformées
- étoiles brillantes dominantes ou non

3. Structures visibles
- zones lumineuses
- zones sombres
- extensions diffuses
- filaments visibles

Ne donne aucune explication physique.

4. Couleurs visibles
- dominante générale
- variations de couleurs visibles

5. Défauts apparents
Cherche uniquement les éléments suivants :

- gradient visible
- dominante de couleur visible
- saturation visible
- halo autour des étoiles
- artefact visible
- étoile allongée visible
- texture granuleuse visible

Pour chaque élément :

Si présent :
"Détecté : ..."

Si absent :
"Non observé : ..."

Ne jamais conclure sur la qualité globale de l'image.

Termine cette section par :

"Aucun autre défaut visuel évident."

==================================================
VOCABULAIRE AUTORISE
==================================================

Tu décris uniquement des apparences visuelles.

Utilise uniquement ces termes :

- étoile
- groupe d'étoiles
- zone lumineuse
- zone sombre
- structure diffuse
- extension diffuse
- filament apparent
- variation de luminosité
- variation de couleur
- fond de ciel
- halo
- artefact
- trace
- saturation
- texture granuleuse
- étoiles ponctuelles
- étoiles allongées


==================================================
VOCABULAIRE INTERDIT
==================================================

Ne jamais utiliser :

- galaxie
- nébuleuse
- amas stellaire
- trou noir
- poussière interstellaire
- gaz ionisé
- région d'émission
- formation stellaire
- matière sombre
- objet céleste
- type d'objet astronomique


Même si cela semble probable.

Une image peut uniquement être décrite,
jamais interprétée.

Si rien n'est visible écrire :
"Aucun défaut visuel évident."

Réponds sous forme de rapport court."

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