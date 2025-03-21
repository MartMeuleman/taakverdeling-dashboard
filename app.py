import streamlit as st
import pandas as pd

# Vaste medewerkerslijst
medewerkers = ['Vita', 'Natalia', 'Hanne', 'Roos', 'Andre', 'Yuliia', 'Romaniia', 'Lesiia', 'Julian', 'Brian',
               'Liv', 'Marie', 'Pien', 'Jaso', 'Mariia C', 'Emanuel', 'Robert', 'Natalio', 'Daphne',
               'Mart', 'Celeste', 'Myrthe', 'Daan', 'Deborah']

# Taken en hun totale duur in minuten
taken = {
    'Vloer dweilen': 120,
    'Glas schoonmaken': 15,
    'Tafels schoonmaken': 60,
    'Hoogstof (vensterbanken + lampen + de rest)': 30,
    'Werkbanken': 30,
    'Vloer achter (stofzuigen + schrobben + putjes)': 45,
    'Ovens schoonmaken': 5,
    'Schrobben vloer klantenrestaurant': 30,
    'Kleedjes stofzuigen': 10,
    'Baby stoelen schoonmaken': 10,
    'Magnetron schoonmaken': 5
}

st.title('🧼 Taakverdeling Schoonmaak Dashboard')
st.write("Selecteer aanwezige medewerkers en wijs per taak personen toe. Je krijgt per persoon te zien wat hun taken en totale werktijd zijn.")

# Selecteer aanwezigen
aanwezigen = st.multiselect('✅ Wie zijn er vanavond aanwezig?', medewerkers)

# Alleen verder als er mensen geselecteerd zijn
if aanwezigen:
    taak_toewijzing = {}
    st.subheader('📋 Taken toewijzen')

    for taak, duur in taken.items():
        toegewezen = st.multiselect(f'{taak} ({duur} min)', aanwezigen, key=taak)
        if toegewezen:
            taak_toewijzing[taak] = {'duur': duur, 'personen': toegewezen}

    if st.button('📊 Bekijk taakverdeling'):
        taak_data = []
        for taak, info in taak_toewijzing.items():
            duur = info['duur']
            mensen = info['personen']
            tijd_per_persoon = duur / len(mensen)
            for persoon in mensen:
                taak_data.append({
                    'Medewerker': persoon,
                    'Taak': taak,
                    'Tijd (min)': tijd_per_persoon
                })

        df = pd.DataFrame(taak_data)
        df_grouped = df.groupby('Medewerker').agg({
            'Taak': lambda x: ', '.join(x),
            'Tijd (min)': 'sum'
        }).reset_index()

        st.subheader('🧍‍♂️ Taakverdeling per persoon')
        st.dataframe(df_grouped)

        csv = df_grouped.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download als CSV", csv, "taakverdeling.csv", "text/csv")
else:
    st.info("Selecteer eerst welke medewerkers aanwezig zijn.")

