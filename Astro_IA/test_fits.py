from core.fits_reader import read_fits_header


result = read_fits_header(
    r"C:\Users\yoye_\Pictures\Astrophoto\RGB_final.fit"
)


for key,value in result.items():

    print(
        f"{key:12} : {value}"
    )