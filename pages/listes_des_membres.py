import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from creation_table import Membres, engine 

import pandas as pd



def recup_membres():

    with Session(engine) as session:
        id_des_membres= session.exec(select(Membres)).all()
        dict_membre = [dict(membre) for membre in id_des_membres]
        return dict_membre

def supprimer_membre(nom_membre):
    with Session(engine) as session:
        statement = select(Membres).where(Membres.nom == str(nom_membre))
        results = session.exec(statement)
        membre_suprr = results.one()
        session.delete(membre_suprr)
        session.commit()


# dico = recup_membres()
# list_membres = pd.DataFrame(dico)
if 'state' not in st.session_state:
    table_membres = recup_membres()
    st.session_state['state'] = pd.DataFrame(table_membres)



with st.form('manipuler les membres', clear_on_submit= True):

    st.title('LA TABLE MEMBRES')
    table_membres = st.session_state.state
    st.table(table_membres)


    colonne1,colonne2,colonne3, colonne4 = st.columns(4)
    with colonne1:
        selection_membre = st.selectbox(
    f"quel membre veux tu supprimer ?",table_membres['nom'])
    with colonne4:
        supprimer_ligne = st.form_submit_button('Supprimer le client')


    st.divider()

    colonne1,colonne2,colonne3, colonne4 = st.columns(4)

    with colonne1:
        ajout_nom_prenom = st.text_input('nom du nouveau membre')

    with colonne2:
        nouvel_email = st.text_input('ajouter un email')
        
        
    with colonne4:
        ajouter_un_membre = st.form_submit_button('ajouter membre')
        



    if supprimer_ligne:

        table_membres = table_membres[table_membres['nom'] != str(selection_membre)]
        # st.write(st.session_state)
        
        supprimer_membre(selection_membre)

        st.session_state.state = table_membres[table_membres['nom'] != selection_membre]
        st.success(f'{selection_membre} à été supprimé')
  
        st.rerun()

    if ajouter_un_membre:
        
        new_membre = Membres(id = len(st.session_state.state),nom = str(ajout_nom_prenom), email = str(nouvel_email))
        new_membre = dict(new_membre)
        new_membre = pd.DataFrame([new_membre], index=[0])
        st.session_state.state = pd.concat([st.session_state.state, new_membre], ignore_index=True)
        st.rerun()






# if __name__ == "__main__":
#     # print(selection_membre)
#     # print(table_membres)
#     new_membre = Membres(nom = str(ajout_nom_prenom), email = str(nouvel_email))
#     print(new_membre)
#     new_membre = dict(new_membre)
#     print(new_membre)
#     new_membre = pd.DataFrame(new_membre)
#     print(new_membre)

    # st.session_state.state = pd.concat([st.session_state.state, new_membre], ignore_index=True)