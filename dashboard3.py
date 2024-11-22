#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st

# Charger les données Excel
fichier = r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_mois.xlsx"  # Changez pour le fichier voulu
df = pd.read_excel(fichier)

# Vérifier les colonnes du fichier
st.write("Colonnes du fichier chargé :", df.columns)

# Titre et description
st.title("Dashboard des Comptages")
st.markdown("""
Ce dashboard présente les répétitions par différents regroupements (jour, semaine, mois, trimestre, année).
Utilisez les filtres pour explorer les données.
""")

# Sélecteur de regroupement
option = st.selectbox(
    "Choisissez le regroupement pour visualiser les données :",
    ["Jour", "Semaine", "Mois", "Trimestre", "Année", "Total"]
)

# Charger les données correspondantes
fichiers_groupes = {
    "Jour": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_jour.xlsx",
    "Semaine": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_semaine.xlsx",
    "Mois": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_mois.xlsx",
    "Trimestre": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_trimestre.xlsx",
    "Année": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_par_annee.xlsx",
    "Total": r"C:\Users\rhamm\Desktop\Projet Mounir Extraction\resultat_total.xlsx"
}

# Charger le fichier correspondant au regroupement sélectionné
df_grouped = pd.read_excel(fichiers_groupes[option])

# Afficher les noms de colonnes pour vérifier leur présence
st.write("Colonnes du fichier sélectionné :", df_grouped.columns)

# Filtre par "Prénom et Nom" si la colonne existe
if "Prénom et nom" in df_grouped.columns:
    noms_selectionnes = st.multiselect(
        "Filtrer par Prénom et Nom",
        options=df_grouped["Prénom et nom"].unique(),
        default=df_grouped["Prénom et nom"].unique()
    )
    df_grouped = df_grouped[df_grouped["Prénom et nom"].isin(noms_selectionnes)]
else:
    st.warning("La colonne 'Prénom et nom' n'est pas présente dans les données.")

# Afficher un tableau interactif
st.dataframe(df_grouped)

# Ajouter un graphique si ce n'est pas l'option "Total"
if option != "Total":  # Les totaux n'ont pas besoin de graphique temporel
    st.bar_chart(df_grouped.set_index(df_grouped.columns[1])["Repetitions_" + option])

# Téléchargement des données
st.markdown("### Télécharger les données :")
st.download_button(
    label="Télécharger ce tableau",
    data=df_grouped.to_csv(index=False).encode('utf-8'),
    file_name=f"resultat_{option.lower()}.csv",
    mime="text/csv"
)

