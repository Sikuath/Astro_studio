# ==========================================================
# SIMBAD CLIENT
# Astro IA
# ==========================================================

from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u



# ==========================================================
# CONFIGURATION SIMBAD
# ==========================================================

custom = Simbad()

custom.add_votable_fields(
    "otype",
    "ra(d)",
    "dec(d)"
)

# ==========================================================
# RECHERCHE PAR NOM
# ==========================================================

def query_object(object_name):
    """
    Recherche un objet SIMBAD par son nom FITS.
    """

    if not object_name:
        return None


    try:

        result = custom.query_object(
            object_name
        )


        if result is None:
            return None



        # récupération robuste des colonnes

        name_col = "MAIN_ID"

        type_col = "OTYPE"

        ra_col = "RA_d"

        dec_col = "DEC_d"



        return {

            "name":
                str(
                    result[name_col][0]
                ).strip(),


            "type":
                str(
                    result[type_col][0]
                ),


            "ra":
                float(
                    result[ra_col][0]
                ),


            "dec":
                float(
                    result[dec_col][0]
                )

        }



    except Exception as e:

        print(
            "Erreur SIMBAD objet :",
            e
        )

        return None




# ==========================================================
# DISTANCE ANGULAIRE
# ==========================================================

def angular_distance(
    ra1,
    dec1,
    ra2,
    dec2
):
    """
    Distance angulaire en degrés.
    """

    c1 = SkyCoord(
        ra1,
        dec1,
        unit="deg"
    )


    c2 = SkyCoord(
        ra2,
        dec2,
        unit="deg"
    )


    return (
        c1.separation(c2)
        .degree
    )



# ==========================================================
# OBJETS DU CHAMP
# ==========================================================

def query_field(
    ra,
    dec,
    radius_arcmin
):
    """
    Recherche les objets présents
    dans le champ photographié.
    """

    objects = []


    try:

        coord = SkyCoord(

            ra,

            dec,

            unit="deg"

        )


        result = custom.query_region(

            coord,

            radius=

            radius_arcmin
            *
            u.arcmin

        )



        if result is None:

            return []



        for row in result:


            try:


                objects.append(

                    {

                        "name":

                            str(
                                row["MAIN_ID"]
                            ).strip(),


                        "type":

                            str(
                                row["OTYPE"]
                            )

                    }

                )


            except Exception:

                continue



    except Exception as e:


        print(

            "Erreur SIMBAD champ :",

            e

        )


    return objects



# ==========================================================
# IDENTIFICATION COMPLETE
# ==========================================================

def identify_target(
    object_name,
    ra,
    dec,
    radius_arcmin
):
    """
    Identification complète.

    Retour toujours identique :

    confirmed
    main_object
    angular_error_deg
    field_objects
    """



    result = {


        "confirmed":

            False,


        "object_name":

            object_name,


        "main_object":

            None,


        "distance_from_center_deg":

            None,


        "field_objects":

            []

    }



    # ======================================================
    # Recherche objet FITS
    # ======================================================


    simbad_object = query_object(

        object_name

    )



    if simbad_object:


        result["main_object"] = simbad_object



        if ra is not None and dec is not None:



            distance = angular_distance(

                ra,

                dec,

                simbad_object["ra"],

                simbad_object["dec"]

            )



            result["distance_from_center_deg"] = round(

                distance,

                4

            )

          
            # confirmation si l'objet est dans le champ

            field_radius_deg = radius_arcmin / 60


            if distance <= field_radius_deg:

                result["confirmed"] = True

        else:

            result["confirmed"] = True




    # ======================================================
    # Recherche champ
    # ======================================================


    if ra is not None and dec is not None:


        result["field_objects"] = query_field(

            ra,

            dec,

            radius_arcmin

        )



    return result