from astropy.io import fits



def get_fits_metadata(path):

    metadata = {}


    try:

        with fits.open(path) as hdul:

            header = hdul[0].header


            keys = {

                "Objet": "OBJECT",

                "Filtre": "FILTER",

                "Temps pose": "EXPTIME",

                "Gain": "GAIN",

                "Température": "CCD-TEMP",

                "Binning": "XBINNING",

                "Caméra": "INSTRUME",

                "Date": "DATE-OBS",

                "Télescope": "TELESCOP",

            }


            for name, key in keys.items():

                if key in header:

                    metadata[name] = header[key]


    except Exception as e:

        metadata["Erreur"] = str(e)


    return metadata