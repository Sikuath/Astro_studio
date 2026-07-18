from pathlib import Path
from astropy.io import fits


def update_final_header(
        rgb_file,
        workdir
):

    rgb_file = Path(rgb_file)
    workdir = Path(workdir)


    if not rgb_file.exists():

        raise FileNotFoundError(
            rgb_file
        )


    hdr_values = {}


    layers = [
        "HA_linear.fit",
        "OIII_linear.fit",
        "SII_linear.fit"
    ]


    total_live = 0
    total_stack = 0


    for layer in layers:


        file = workdir / layer


        if not file.exists():
            continue


        hdr = fits.getheader(file)


        total_live += float(
            hdr.get(
                "LIVETIME",
                0
            )
        )


        total_stack += int(
            hdr.get(
                "STACKCNT",
                1
            )
        )


        if not hdr_values:

            for key in [
                "OBJECT",
                "DATE-OBS",
                "TELESCOP",
                "FOCALLEN",
                "INSTRUME",
                "GAIN",
                "OFFSET",
                "CCD-TEMP",
                "RA",
                "DEC",
                "OBJCTRA",
                "OBJCTDEC"
            ]:

                if key in hdr:
                    hdr_values[key] = hdr[key]



    with fits.open(
        rgb_file,
        mode="update"
    ) as hdul:


        header = hdul[0].header


        for key, value in hdr_values.items():

            header[key] = value



        header["STACKCNT"] = (
            total_stack,
            "Nombre poses combinees"
        )


        header["LIVETIME"] = (
            total_live,
            "Temps integration total secondes"
        )


        header["ASTROAPP"] = (
            "Astro Suite",
            "Logiciel traitement"
        )


        hdul.flush()