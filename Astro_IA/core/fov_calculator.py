# ==========================================================
# Astro IA
# FOV Calculator
# ==========================================================

import math


# ==========================================================
# CALCUL CHAMP DE VISION ET ECHANTILLONNAGE
# ==========================================================

def calculate_fov(
    focal_length,
    pixel_size,
    sensor_width,
    sensor_height,
    aperture=None,
    pixel_width=None,
    pixel_height=None
):
    """
    Calcule les paramètres optiques d'une acquisition astro.

    Retourne :
    - champ de vision
    - échantillonnage
    - résolution théorique
    - rayon de recherche SIMBAD
    """

    # ======================================================
    # VERIFICATIONS
    # ======================================================

    if not focal_length:

        raise ValueError(
            "Focale manquante"
        )


    if not pixel_size:

        pixel_size = 3.76



    # ======================================================
    # CHAMP DE VISION
    # ======================================================

    fov_horizontal_deg = (

        2
        *
        math.degrees(

            math.atan(

                sensor_width
                /
                (2 * focal_length)

            )

        )

    )


    fov_vertical_deg = (

        2
        *
        math.degrees(

            math.atan(

                sensor_height
                /
                (2 * focal_length)

            )

        )

    )



    # ======================================================
    # DIAGONALE
    # ======================================================

    diagonal_sensor = math.sqrt(

        sensor_width ** 2
        +
        sensor_height ** 2

    )


    diagonal_fov_deg = (

        2
        *
        math.degrees(

            math.atan(

                diagonal_sensor
                /
                (2 * focal_length)

            )

        )

    )



    # ======================================================
    # ECHANTILLONNAGE
    # ======================================================

    sampling_arcsec_pixel = (

        206.265
        *
        pixel_size
        /
        focal_length

    )



    # ======================================================
    # RESOLUTION THEORIQUE
    # ======================================================

    resolution_arcsec = None


    if aperture:

        resolution_arcsec = (

            116
            /
            aperture

        )



    # ======================================================
    # CONVERSION ARC MINUTES
    # ======================================================

    fov_horizontal_arcmin = (

        fov_horizontal_deg
        *
        60

    )


    fov_vertical_arcmin = (

        fov_vertical_deg
        *
        60

    )


    diagonal_fov_arcmin = (

        diagonal_fov_deg
        *
        60

    )



    # ======================================================
    # RAYON SIMBAD
    #
    # On cherche sur la moitié du champ diagonal
    # avec marge de sécurité.
    #
    # Ceci permet de confirmer un objet FITS
    # même s'il n'est pas centré.
    # ======================================================


    search_radius_deg = (

        diagonal_fov_deg
        /
        2

    )


    # marge 20 %

    search_radius_deg *= 1.2



    search_radius_arcmin = (

        search_radius_deg
        *
        60

    )



    # ======================================================
    # RESULTAT
    # ======================================================

    return {


        # ------------------------------
        # Champ
        # ------------------------------

        "fov_horizontal_deg":

            round(
                fov_horizontal_deg,
                3
            ),


        "fov_vertical_deg":

            round(
                fov_vertical_deg,
                3
            ),


        "diagonal_fov_deg":

            round(
                diagonal_fov_deg,
                3
            ),



        "fov_horizontal_arcmin":

            round(
                fov_horizontal_arcmin,
                2
            ),


        "fov_vertical_arcmin":

            round(
                fov_vertical_arcmin,
                2
            ),


        "diagonal_fov_arcmin":

            round(
                diagonal_fov_arcmin,
                2
            ),



        # ------------------------------
        # Optique
        # ------------------------------

        "sampling_arcsec_pixel":

            round(
                sampling_arcsec_pixel,
                3
            ),


        "resolution_arcsec":

            round(
                resolution_arcsec,
                2
            )
            if resolution_arcsec
            else None,



        # ------------------------------
        # SIMBAD
        # ------------------------------

        "search_radius_deg":

            round(
                search_radius_deg,
                3
            ),


        "search_radius_arcmin":

            round(
                search_radius_arcmin,
                1
            )

    }