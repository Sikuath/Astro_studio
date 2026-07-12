# 🔭 Astro_studio

Astro_studio est une application de traitement d’images astrophotographiques développée avec **Python + Streamlit**.

Elle propose un workflow complet pour la recomposition d’images **SHO (SII / Hα / OIII)** et **LRGB (Luminance / Rouge / Vert / Bleu)**, avec une interface graphique simple orientée astrophotographie.

L’objectif est de proposer un environnement de travail clair, évolutif et adapté aussi bien à un usage personnel qu’à un contexte pédagogique en club astro.

---

# ✨ Fonctionnalités actuelles

## 📂 Gestion de projets

* Création et chargement de projets astrophotographiques
* Détection automatique du type de projet :

  * SHO
  * LRGB
* Gestion des chemins Siril CLI et Siril GUI

---

# 🌈 Workflow SHO

* Import des couches :

  * `SII.fit`
  * `HA.fit`
  * `OIII.fit`

* Prétraitement automatisé :

  * préparation des dossiers de travail
  * astrométrie
  * registration
  * génération des couches linéaires

* Recomposition SHO :

  * palettes prédéfinies
  * mode manuel
  * aperçu temps réel
  * réglage du stretch
  * zoom d’inspection

Palettes disponibles :

* Manual
* Hubble SHO
* HOO Boost
* HOO Natural
* Hα Rich
* OIII Rich
* Foraxx Pro
* Gold & Blue
* Teal & Orange

## 🎨 Configurations des palettes SHO

Les palettes sont définies par les coefficients de mélange :

| Palette | R : SII | R : Hα | G : Hα | G : OIII | B : OIII |
|---|---:|---:|---:|---:|---:|
| 🌌 Hubble SHO | 0.8 | 0.2 | 0.7 | 0.3 | 1.0 |
| 🔥 HOO Boost | 0.0 | 0.15 | 0.3 | 0.7 | 1.0 |
| 🌿 HOO Natural | 0.0 | 0.10 | 0.6 | 0.4 | 1.0 |
| ❤️ Hα Rich | 0.2 | 0.8 | 0.8 | 0.2 | 0.8 |
| 🔵 OIII Rich | 0.0 | 0.10 | 0.0 | 1.0 | 1.0 |
| 🟡 Foraxx Pro | 0.6 | 0.4 | 0.4 | 0.6 | 1.0 |
| 🌅 Gold & Blue | 1.0 | 0.0 | 0.5 | 0.5 | 1.0 |
| 🟠 Teal & Orange | 0.9 | 0.1 | 0.3 | 0.7 | 1.0 |

### Formule de recomposition

---

# 🌈 Workflow LRGB

Support de la recomposition classique :

* `L.fit`
* `R.fit`
* `G.fit`
* `B.fit`

Pipeline :

1. Préparation du projet
2. Astrométrie
3. Registration
4. Renommage automatique des couches
5. Préparation linéaire
6. Mix LRGB

La luminance est injectée dans les couches couleur tout en conservant un export FITS linéaire.

---

# 🔬 Traitement final

* Preview interactive
* Ajustement du stretch d'affichage
* Zoom d'inspection
* Export FITS linéaire
* Ouverture automatique dans Siril graphique

Les fichiers exportés conservent les données astrophotographiques sans stretch destructif.

---

# 🧪 Workflow utilisateur

1. Créer ou sélectionner un dossier projet

2. Ajouter les fichiers sources :

### Projet SHO

```
mon_projet/
├── SII.fit
├── HA.fit
└── OIII.fit
```

### Projet LRGB

```
mon_projet/
├── L.fit
├── R.fit
├── G.fit
└── B.fit
```

3. Lancer le prétraitement

4. Choisir la recomposition :

* SHO
* LRGB

5. Ajuster l’aperçu

6. Exporter la composition finale

7. Continuer le traitement dans Siril

---

# 📁 Structure du projet

```
Astro_suite/

├── Astro_studio/
│
│   ├── core/
│   │   ├── pipelines
│   │   ├── FITS handling
│   │   └── processing
│   │
│   ├── tools/
│   │   ├── SHO mixer
│   │   └── LRGB mixer
│   │
│   ├── ui/
│   │   └── Streamlit interface
│   │
│   └── scripts/
│       └── Siril scripts
│
└── Astro_pretraitement/
```

---

# 🚀 Installation (développement)

## 1. Cloner le projet

```bash
git clone https://github.com/Sikuath/Astro_suite.git
cd Astro_suite
```

## 2. Créer un environnement virtuel

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Lancer l'application

Windows :

```
Astro_studio.bat
```

ou manuellement :

```bash
streamlit run app.py
```

---

# 📦 Dépendances principales

* streamlit
* numpy
* scipy
* astropy
* pillow

---

# 💾 Export

Astro Suite génère des fichiers FITS :

## SHO

```
R.fit
G.fit
B.fit
RGB_final.fit
```

## LRGB

```
LRGB_R.fit
LRGB_G.fit
LRGB_B.fit
RGB_final.fit
```

Les fichiers restent en données linéaires afin de permettre une reprise complète du traitement dans Siril ou un autre logiciel.

---

# 📄 Licence

MIT License © 2026

© 2026 Sikuath
