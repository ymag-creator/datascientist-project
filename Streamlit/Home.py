import streamlit as st 
import stream2 
import page1 
import page2 

PAGES = { "Accueil": stream2,
          "Data Visualisations": page1, 
          "Prédictions": page2 } 

st.sidebar.title('Navigation') 
selection = st.sidebar.radio("Aller à", list(PAGES.keys())) 

page = PAGES[selection] 
page.main()