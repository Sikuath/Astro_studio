from astropy.io import fits

for f in [
    r"C:\Users\yoye_\Pictures\Astrophoto\Traitement\RGB_final.fit",
    r"C:\Users\yoye_\Pictures\Astrophoto\Traitement\RVBSiril.fit",
]:
    data = fits.getdata(f)
    print(f)
    print("shape :", data.shape)
    print("dtype :", data.dtype)
    print()