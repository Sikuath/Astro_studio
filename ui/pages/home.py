import streamlit as st

def show_home():

    st.title("🔭 Astro Studio")

    st.write(
        """
        Bienvenue dans Astro Studio.

        Cette application permet de gérer et traiter vos images astrophotographiques
        via Siril et un pipeline personnalisé.
        """
    )

    st.markdown("---")

    st.subheader("🚀 Workflow")

    st.markdown("""
    1. Configurer le projet (onglet Projet)
    2. Charger les données
    3. Lancer le traitement souhaité
    4. Visualiser les résultats
    5. Exporter les données
    6. Continuer sous Siril                        
    """)

    st.info("Commence par l'onglet Projet pour initialiser ton dossier de travail.")