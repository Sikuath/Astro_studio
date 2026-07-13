from pathlib import Path
from astropy.io import fits


# ==========================================
# CONFIGURATION
# ==========================================

fits_file = Path(
    r"C:\Users\yoye_\Pictures\Astrophoto\Traitement\RGB_final.fit"
)


# ==========================================
# LECTURE HEADER
# ==========================================

if not fits_file.exists():

    print(
        f"Fichier introuvable : {fits_file}"
    )

    exit()



print("=" * 60)
print("HEADER FITS")
print(fits_file)
print("=" * 60)



with fits.open(fits_file) as hdul:

    header = hdul[0].header



    for key, value in header.items():

        print(
            f"{key:12} = {value}"
        )



print("=" * 60)
print("FIN HEADER")
print("=" * 60)