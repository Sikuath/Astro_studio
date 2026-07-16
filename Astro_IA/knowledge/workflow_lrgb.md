# Workflow LRGB Siril


## Objectif

Produire une image couleur naturelle à partir des couches :

- Luminance
- Rouge
- Vert
- Bleu


---

# Préparation


Créer les séquences :

- L
- R
- G
- B


Vérifier :

- calibration correcte
- darks adaptés
- flats disponibles


---

# Prétraitement Siril


Ordre recommandé :


1. Calibration

Appliquer :

- dark
- flat
- bias si utilisé


Objectif :

supprimer :

- signal thermique
- poussières
- défauts capteur


---

2. Alignement


Aligner chaque couche.


Contrôler :

- étoiles correctement superposées


---

3. Empilement


Utiliser :

- rejet des pixels aberrants
- normalisation


Objectif :

augmenter le rapport signal/bruit.


---

# Traitement Luminance


La luminance apporte :

- détails
- résolution
- contraste


Étapes :

- extraction gradient
- calibration photométrique
- déconvolution si adaptée
- réduction bruit


---

# Traitement RGB


Objectif :

obtenir une couleur équilibrée.


Étapes :

- calibration couleur photométrique
- équilibrage des canaux
- correction dominante


---

# Assemblage


Combiner :

L + RGB


La luminance contrôle :

- détails
- contraste


Le RGB contrôle :

- couleurs


---

# Finition Siril


Effectuer :

- ajustement dynamique
- réduction bruit légère
- contrôle étoiles


---

# Finition GIMP


Utiliser :

- niveaux
- courbes
- masques
- contraste local
- ajustement couleurs


Éviter :

- saturation excessive
- écrasement des noirs
- halos artificiels