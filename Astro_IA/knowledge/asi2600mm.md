# ZWO ASI2600MM Pro


## Identification


Caméra :

ZWO ASI2600MM Pro


Type :

Caméra astronomique monochrome refroidie CMOS


Constructeur :

ZWO


Utilisation :

Astrophotographie ciel profond.


---

# Caractéristiques principales


## Capteur


Type :

Sony IMX571 monochrome


Format :

APS-C


Résolution :

6248 × 4176 pixels


Nombre de pixels :

26 mégapixels


Taille pixel :

3,76 µm


Taille capteur approximative :

23,5 × 15,7 mm



---

# Refroidissement


La caméra possède un refroidissement régulé.


Objectifs :

- réduire le courant thermique
- stabiliser le bruit
- permettre l'utilisation de bibliothèques de darks


La température du capteur doit être indiquée par le FITS.


Ne jamais remplacer une température mesurée par une valeur théorique.


---

# Gain


Le gain dépend du réglage d'acquisition.


La valeur utilisée doit toujours provenir du header FITS.


Ne jamais supposer :

- gain optimal
- gain utilisé
- gain recommandé


---

# Offset


L'offset dépend du logiciel d'acquisition.


La valeur doit provenir du FITS si disponible.


---

# Bruit et dynamique


La caméra possède :

- faible bruit de lecture
- grande dynamique
- mémoire tampon


Cependant :

La qualité réelle d'une image dépend aussi de :

- ciel
- temps de pose
- filtre
- traitement
- calibration


Ne jamais conclure sur la qualité d'une image uniquement avec le modèle de caméra.



---

# Calibration


Pour cette caméra utiliser de préférence des masters correspondant aux conditions d'acquisition.


Les darks doivent correspondre :

- température proche
- gain identique
- durée de pose identique


Les flats doivent corriger :

- poussières
- vignettage
- défauts optiques


Les bias peuvent être utilisés selon le workflow choisi.



---

# Filtres


La caméra étant monochrome, elle nécessite des filtres.


Exemples :


## LRGB

Utilisation :

- Luminance
- Rouge
- Vert
- Bleu


Objectifs :

- couleurs naturelles
- galaxies
- amas


---

## Bande étroite


Filtres :

- Ha
- OIII
- SII


Utilisation :

- nébuleuses en émission


---

# Calcul échantillonnage


L'échantillonnage dépend de :

- focale
- taille pixel


Formule :

échantillonnage (arcsec/pixel) =
206,265 × taille pixel (µm) / focale (mm)


Pour une ASI2600MM Pro :

pixel = 3,76 µm



---

# Analyse astrophotographique


Avec uniquement le modèle de caméra il est impossible de déterminer :

- qualité des étoiles
- FWHM
- HFR
- suivi
- mise au point
- tilt
- bruit réel


Ces paramètres nécessitent :

- image
- analyse Siril
- mesures dédiées



---

# Règles Astro IA


Si le FITS indique :

ZWO ASI2600MM Pro


L'IA peut rappeler :

- caméra monochrome refroidie
- pixels 3,76 µm
- capteur APS-C


Mais elle doit toujours utiliser en priorité :

- gain FITS
- température FITS
- temps de pose FITS


---

# Matériel associé possible


La caméra peut être utilisée avec :

- lunette astronomique
- Newton
- télescope corrigé
- filtres LRGB
- filtres SHO


Le choix optique ne doit jamais être déduit uniquement du modèle caméra.