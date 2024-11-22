import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from creation_table import Coachs, engine 

import pandas as pd



def recup_coach():

    with Session(engine) as session:
        id_des_coachs= session.exec(select(Coachs)).all()
        dict_coach = [dict(coach) for coach in id_des_coachs]
        return dict_coach
    

    
def supprimer_coach(nom_coach):
    with Session(engine) as session:
        statement = select(Coachs).where(Coachs.nom_coach == str(nom_coach))
        results = session.exec(statement)
        coach_suprr = results.one()
        session.delete(coach_suprr)
        session.commit()

def nouveau_coach(nouveau_nom_coach, specialite_new_coach):

    with Session(engine) as session:
        new_coach = Coachs(nom_coach = nouveau_nom_coach, specialite= specialite_new_coach)
        session.add(new_coach)
        session.commit()

def recup_dernier_coach():
    with Session(engine) as session:
        dernier_coach = session.exec(select(Coachs).order_by(Coachs.id.desc()).limit(1)).one()
        return dict(dernier_coach)
# dico = recup_coach()
# list_coach = pd.DataFrame(dico)
if 'coach_state' not in st.session_state:
    table_coach = recup_coach()
    st.session_state['coach_state'] = pd.DataFrame(table_coach)



with st.form('manipuler les coach', clear_on_submit= True):

    st.title('LA TABLE coach')
    table_coach = st.session_state.coach_state
    st.table(table_coach)


    # colonne1,colonne2,colonne3, colonne4 = st.columns(4)
    # with colonne1, colonne2, colonne3:
    #     selection_coach = st.selectbox(
    # f"quel coach veux tu supprimer ?",table_coach['nom_coach'])
    # with colonne4:
    #     supprimer_ligne = st.form_submit_button('Supprimer le coach')

    selection_coach = st.selectbox(
    f"quel coach veux tu supprimer ?",table_coach['nom_coach'])

    supprimer_ligne = st.form_submit_button('Supprimer le coach')

    st.divider()

    colonne1,colonne2 = st.columns(2)

    with colonne1:
        ajout_nom_prenom = st.text_input('nom du nouveau coach')

    with colonne2:
        specialite_coach = st.selectbox('ajouter une spécialité', table_coach['specialite'] )
        
        
    # with colonne4:
    #     ajouter_un_coach = st.form_submit_button('ajouter coach')
    ajouter_un_coach = st.form_submit_button('ajouter coach')
        



    if supprimer_ligne:

        table_coach = table_coach[table_coach['nom_coach'] != str(selection_coach)]
        # st.write(st.session_state)
        
        supprimer_coach(selection_coach)

        st.session_state.coach_state = table_coach[table_coach['nom_coach'] != selection_coach]
        st.success(f'{selection_coach} à été supprimé')
        time.sleep(2)
        st.rerun()

    if ajouter_un_coach:

        nouveau_coach(ajout_nom_prenom, specialite_coach )
        new_coach = recup_dernier_coach()
        new_coach = pd.DataFrame([new_coach])
        st.session_state.coach_state = pd.concat([st.session_state.coach_state, new_coach], ignore_index=True)
        
        
        st.success(f'le nouveau sensei {ajout_nom_prenom} ajouté, bienvenu à lui!!')
        time.sleep(2)
        st.rerun()