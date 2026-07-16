# Workflow SHO Siril + GIMP


## Objectif

Produire une image en palette SHO à partir des couches :

- SII
- Ha
- OIII


La priorité est de conserver :

- le signal réel
- la dynamique
- les détails faibles
- une séparation correcte des couches


---

# Identification des couches


Avant traitement vérifier :

- SII présent
- Ha présent
- OIII présent


Chaque couche doit être traitée séparément avant assemblage.


---

# Prétraitement Siril


## Calibration


Appliquer pour chaque couche :

- darks adaptés
- flats adaptés
- bias si utilisé


Les masters doivent correspondre :

- à la caméra
- au gain
- à la température
- au temps de pose


---

# Alignement


Aligner les trois couches :

- SII
- Ha
- OIII


Objectif :

obtenir une superposition parfaite des étoiles.


Un mauvais alignement provoque :

- étoiles colorées
- détails dédoublés
- halos artificiels


---

# Empilement


Pour chaque couche :

- normaliser
- empiler
- appliquer rejet pixels


Objectif :

améliorer le rapport signal/bruit.


---

# Traitement individuel des couches


## Ha


Le Ha contient souvent :

- les structures principales
- les filaments
- les zones d'émission fortes


Traitement :

- extraction gradient
- ajustement dynamique
- réduction bruit contrôlée


---

## OIII


L'OIII contient souvent :

- les zones bleues/vertes
- les extensions faibles


Attention :

L'OIII est souvent plus faible que le Ha.


Éviter :

- amplification excessive
- création de faux détails


---

## SII


Le SII contient :

- structures rouges profondes
- détails faibles


Nécessite souvent :

- réduction bruit
- traitement doux


---

# Composition SHO


Correspondance classique :

SII → Rouge

Ha → Vert

OIII → Bleu


Cette composition peut être modifiée selon l'objectif esthétique.


---

# Création de luminance


Options possibles :


## Ha comme luminance


Avantage :

- détails élevés


Inconvénient :

- risque de dominante monochrome


---

## Luminance synthétique


Créer une luminance à partir de :

- SII
- Ha
- OIII


Avec pondération adaptée.


Objectif :

conserver les détails sans favoriser une seule couche.


---

# Traitement Siril final


Effectuer :

- extraction gradient
- calibration photométrique si adaptée
- ajustement histogramme
- réduction bruit
- amélioration contraste


La déconvolution doit être utilisée uniquement si les étoiles et le signal le permettent.


---

# Passage GIMP


Objectifs :

- équilibre esthétique
- contraste
- gestion des couleurs


Utiliser :

- masques
- courbes
- niveaux
- balance couleurs


---

# Règles importantes


Ne jamais :

- créer du signal absent
- saturer fortement une couche faible
- augmenter le bruit pour faire apparaître des détails artificiels


Une zone absente dans une couche reste une zone absente.


---

# Philosophie SHO


Une bonne image SHO doit conserver :

- information scientifique
- lisibilité
- équilibre esthétique


La couleur sert à révéler les structures, pas à masquer le manque de signal.