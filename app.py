import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import os

st.set_page_config(page_title="PDF vers Excel", layout="centered")

st.title("📄 Convertisseur PDF → Excel")
st.write("Glisse ton **fichier PDF** ici. Les tableaux seront extraits et enregistrés dans un fichier Excel téléchargeable.")

uploaded_file = st.file_uploader("Dépose ton PDF ici", type="pdf")

if uploaded_file is not None:
    pdf_name = os.path.splitext(uploaded_file.name)[0]  # Nom de base sans extension

    with pdfplumber.open(uploaded_file) as pdf:
        all_rows = []
        for i, page in enumerate(pdf.pages):
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_rows.append(df)

    if all_rows:
        final_df = pd.concat(all_rows, ignore_index=True)

        # Enregistrer dans un buffer Excel
        output = BytesIO()
        final_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        excel_filename = f"{pdf_name}.xlsx"

        st.success("✅ Conversion réussie !")
        st.download_button(
            label="📥 Télécharger le fichier Excel",
            data=output,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Aucun tableau détecté dans le fichier PDF.")
