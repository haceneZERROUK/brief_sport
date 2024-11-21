import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from creation_table import Membres,Coachs,engine, Cartes_acces, Inscription 

import pandas as pd



def recup_membres():

    with Session(engine) as session:
        id_des_membres= session.exec(select(Coachs)).all()
        dict_membre = [dict(membre) for membre in id_des_membres]
        return dict_membre

list_membres = recup_membres()

memb = pd.DataFrame(list_membres)

st.title('LA TABLE MEMBRE')
st.table(memb)