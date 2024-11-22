import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from creation_table import Cours,Coachs, engine 
import time
import pandas as pd



def recup_cours():

    with Session(engine) as session:
        id_des_Cours= session.exec(select(Cours)).all()
        dict_cours = [dict(cours) for cours in id_des_Cours]
        return dict_cours
    
def recup_le_coach(specialite_cours):
    with Session(engine) as session:
        coach_cours = session.exec(select(Coachs.id).where(Coachs.specialite == specialite_cours)).one()
        return coach_cours
    
def supprimer_cours(id_cours):
    with Session(engine) as session:
        statement = select(Cours).where(Cours.id == str(id_cours))
        results = session.exec(statement)
        cours_suprr = results.one()
        session.delete(cours_suprr)
        session.commit()

def nouveau_cours(specialite_new_cours,coach_spe, mois, jours,heure, annee = 2024):

    with Session(engine) as session:
        new_cours = Cours(nom_cours = f"cours de {specialite_new_cours} le {jours} / {mois} à {heure} heure",
                         
                          horaire = datetime.datetime(annee, mois, jours, heure),
                          capacite_max= 8,
                          coach_id= coach_spe)
        session.add(new_cours)
        session.commit()

def recup_dernier_cours():
    with Session(engine) as session:
        dernier_cours = session.exec(select(Cours).order_by(Cours.id.desc()).limit(1)).one()
        return dict(dernier_cours)


if 'cours_state' not in st.session_state:
    table_cours = recup_cours()
    st.session_state['cours_state'] = pd.DataFrame(table_cours)



with st.form('manipuler les cours', clear_on_submit= True):

    st.title('LA TABLE cours')
    table_cours = st.session_state.cours_state
    st.table(table_cours)



    selection_cours = st.selectbox(
    f"quel cours veux tu supprimer ?",table_cours['nom_cours'])

    supprimer_ligne = st.form_submit_button('Supprimer le cours')


    st.divider()

    colonne1,colonne2,colonne3 = st.columns(3)

    with colonne1:
        specialite_cours = st.selectbox('ajouter une spécialité', ["Yoga", "Pump", "Pilates", "Musculation", "Boxe"] )

    with colonne2:
        heure_cours = st.selectbox('quelle heure?', [heure for heure in range(9,17)])

    with colonne3:
        jour_cours = st.selectbox('quelle jour?', [jour for jour in range(1,30)])
        
        

    ajouter_un_cours = st.form_submit_button('ajouter cours')
        



    if supprimer_ligne:

        table_cours_ligne = table_cours[table_cours['nom_cours'] == str(selection_cours)]
        print(table_cours_ligne)
        cours_id_suppr = table_cours_ligne['id'].iloc[0]
        print(cours_id_suppr)
        table_cours = table_cours[table_cours['nom_cours'] != str(selection_cours)]

        
        supprimer_cours(cours_id_suppr)
        st.session_state.cours_state = table_cours[table_cours['nom_cours'] != selection_cours]
        st.success(f'{selection_cours} à été supprimé')
        time.sleep(1)
        st.rerun()

    if ajouter_un_cours:

        nouvel_horaire = datetime.datetime(2024, 12 , jour_cours, heure_cours)


        if (table_cours.loc[:,'horaire'] == nouvel_horaire).any():

            st.error('La plage horaire est déjà prise, veuillez saisir un nouvel horaire')
            time.sleep(2)
            st.rerun()

        else:
            id_du_coach = recup_le_coach(specialite_cours)
            nouveau_cours(specialite_cours, id_du_coach,12,jour_cours,heure_cours )
            new_cours = recup_dernier_cours()
            new_cours = pd.DataFrame([new_cours])
            st.session_state.cours_state = pd.concat([st.session_state.cours_state, new_cours], ignore_index=True)
            
            
            st.success(f'nouvelle heure de souffrance ajoutée, que le sort vous soit favorable!!')
            time.sleep(2)
            st.rerun()