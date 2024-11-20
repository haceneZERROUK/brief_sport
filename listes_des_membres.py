import streamlit as st
from sqlmodel import Field, Session, SQLModel, create_engine, select
from creation_table import Membres,Coachs,engine, Cartes_acces
import pandas as pd

def recup_membres():
    with Session(engine) as session:
        id_des_membres= session.exec(select(Membres)).all()
        for membre in id_des_membres:
            print(membre)

# memb = pd.DataFrame(recup_membres())

# st.dataframe(memb)


if __name__ == "__main__":
    print(recup_membres())