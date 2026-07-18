# ==========================================================
# Astro IA
# Détection automatique de l'optique utilisée
# ==========================================================


def detect_optic(focal_length):


    try:

        focal = float(focal_length)

    except Exception:

        return "Optique inconnue"



    # ------------------------------------------------------
    # Sky-Watcher Evolux 62ED
    # Focale nominale 400 mm
    # Avec réducteur éventuel ~300 mm
    # ------------------------------------------------------

    if 280 <= focal <= 450:


        return (
            "Lunette astronomique "
            "Sky-Watcher Evolux 62ED "
            "(62/400)"
        )



    # ------------------------------------------------------
    # Newton 200/1000
    # Avec correcteur de coma éventuel
    # ------------------------------------------------------

    if 850 <= focal <= 1050:


        return (
            "Télescope Newton "
            "200/1000"
        )



    # ------------------------------------------------------
    # Cas non reconnu
    # ------------------------------------------------------

    return (
        f"Optique inconnue "
        f"({focal:.0f} mm)"
    )