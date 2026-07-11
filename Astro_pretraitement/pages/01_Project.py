import streamlit as st
from pathlib import Path

from core.config import load_config, save_config
from core.reject import (
    clear_trash_folder,
    check_trash_folder,
    extract_target_name
)

from ui.theme import load_theme
from ui.sidebar import show_sidebar



# ==========================
# Configuration Streamlit
# ==========================

st.set_page_config(
    page_title="Projet Astro",
    page_icon="📁",
    layout="wide"
)



# ==========================
# Workflow
# ==========================

if "workflow_step" not in st.session_state:

    st.session_state.workflow_step = 1



# ==========================
# Thème + Sidebar
# ==========================

load_theme()

show_sidebar()



# ==========================
# Titre
# ==========================

st.title(
    "📁 Configuration du projet"
)



# ==========================
# Chargement configuration
# ==========================

config = load_config()


lights_current = config.get(
    "lights_folder",
    ""
)


rejected_current = config.get(
    "rejected_folder",
    ""
)


siril_current = config.get(
    "siril_path",
    r"C:\Program Files\Siril\bin\siril-cli.exe"
)



# =====================================================
# Zone configuration
# =====================================================

left, right = st.columns(
    [1, 3]
)



with left:

    st.subheader(
        "📂 Dossiers"
    )


    lights_folder = st.text_input(
        "📷 Dossier des Lights",
        value=lights_current
    )


    rejected_folder = st.text_input(
        "🗑️ Dossier des rejets",
        value=rejected_current
    )


    st.divider()


    st.subheader(
        "🔭 Siril"
    )


    siril_path = st.text_input(
        "⚙️ Exécutable Siril CLI",
        value=siril_current
    )



# =====================================================
# Vérification Siril
# =====================================================

siril_file = Path(
    siril_path
)


if siril_file.exists():

    if "siril-cli" in siril_file.name.lower():

        st.success(
            "✅ Siril CLI détecté"
        )

    else:

        st.warning(
            "⚠️ Utilisez siril-cli.exe et non siril.exe"
        )

else:

    st.error(
        "❌ Siril CLI introuvable"
    )



# =====================================================
# Contrôle Lights_trash
# =====================================================

if lights_folder:


    lights_path = Path(
        lights_folder
    )


    trash_folder = (
        lights_path.parent
        /
        "Lights_trash"
    )


    if check_trash_folder(
        trash_folder
    ):


        files = list(
            trash_folder.glob("*")
        )


        st.divider()


        st.subheader(
            "🧹 Vérification Lights_trash"
        )



        # ---------------------------------
        # Objet courant
        # ---------------------------------

        current_target = None


        light_files = list(
            lights_path.glob("*.fit")
        )


        if light_files:

            current_target = extract_target_name(
                light_files[0].name
            )



        # ---------------------------------
        # Objets dans trash
        # ---------------------------------

        trash_targets = {}


        for file in files:

            target = extract_target_name(
                file.name
            )


            if target:

                trash_targets[target] = (
                    trash_targets.get(target, 0)
                    +
                    1
                )



        st.warning(
            f"""
⚠️ Le dossier **Lights_trash** contient 
**{len(files)} fichier(s)** :

`{trash_folder}`
"""
        )



        # ---------------------------------
        # Analyse intelligente
        # ---------------------------------

        if current_target:


            st.info(
                f"📷 Objet du projet actuel : **{current_target}**"
            )


            if current_target in trash_targets:

                st.error(
                    f"""
⚠️ ATTENTION !

Le dossier Lights_trash contient aussi :
**{current_target}**

Cela peut correspondre à la session actuelle.
Vérification recommandée avant suppression.
"""
                )

            else:

                if trash_targets:

                    st.success(
                        "✅ Aucun conflit détecté avec le projet actuel."
                    )


        # ---------------------------------
        # Résumé objets trash
        # ---------------------------------

        if trash_targets:

            with st.expander(
                "🔎 Objets détectés dans Lights_trash"
            ):

                for target, count in sorted(
                    trash_targets.items()
                ):

                    st.write(
                        f"📷 **{target}** : {count} fichier(s)"
                    )



        # ---------------------------------
        # Liste fichiers
        # ---------------------------------

        with st.expander(
            "📋 Voir quelques fichiers"
        ):

            for file in files[:20]:

                st.write(
                    f"📷 {file.name}"
                )


            if len(files) > 20:

                st.caption(
                    f"... et {len(files)-20} autres fichiers"
                )



        # ---------------------------------
        # Suppression
        # ---------------------------------

        if st.button(
            "🗑️ Vider Lights_trash"
        ):

            st.session_state.confirm_trash_delete = True



        if st.session_state.get(
            "confirm_trash_delete",
            False
        ):


            st.error(
                "⚠️ Suppression définitive des images du dossier Lights_trash."
            )


            c1, c2 = st.columns(2)



            with c1:

                if st.button(
                    "✅ Confirmer"
                ):

                    deleted = clear_trash_folder(
                        trash_folder
                    )


                    st.session_state.confirm_trash_delete = False


                    st.success(
                        f"✅ {deleted} fichier(s) supprimé(s)"
                    )


                    st.rerun()



            with c2:

                if st.button(
                    "❌ Annuler"
                ):

                    st.session_state.confirm_trash_delete = False

                    st.rerun()



# =====================================================
# Sauvegarde
# =====================================================

st.divider()


configuration_ok = False



col1, col2, col3 = st.columns(
    [2,1,2]
)



with col2:


    if st.button(
        "💾 Sauvegarder",
        use_container_width=True
    ):


        lights_path = Path(
            lights_folder
        )


        rejected_path = Path(
            rejected_folder
        )


        siril_file = Path(
            siril_path
        )



        if not lights_path.exists():

            st.error(
                "❌ Dossier Lights inexistant"
            )


        elif not siril_file.exists():

            st.error(
                "❌ Siril CLI introuvable"
            )


        elif "siril-cli" not in siril_file.name.lower():

            st.error(
                "❌ Mauvais exécutable Siril"
            )


        else:


            rejected_path.mkdir(
                parents=True,
                exist_ok=True
            )


            config["lights_folder"] = lights_folder

            config["rejected_folder"] = rejected_folder

            config["siril_path"] = siril_path


            save_config(
                config
            )


            st.session_state.lights_folder = lights_folder

            st.session_state.rejected_folder = rejected_folder

            st.session_state.siril_path = siril_path


            configuration_ok = True


            st.success(
                "✅ Configuration sauvegardée"
            )


            st.session_state.workflow_step = 2


            st.switch_page(
                "pages/02_Preview.py"
            )