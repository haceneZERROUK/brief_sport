from sqlmodel import Field, SQLModel, create_engine, Relationship, Session
from typing import Optional
import datetime
from sqlalchemy import ForeignKey



class Cartes_acces(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    numero_unique: int | None

    # Relation avec Membres, avec le back_populates
    membres: list['Membres'] = Relationship(back_populates="carte_acces")


    # Étend la définition existante de cette table si nécessaire
    __table_args__ = {"extend_existing": True}

class Membres(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    nom : str 
    email : str
    carte_acces_id: Optional[int]= Field(default = None, foreign_key = 'cartes_acces.id')
        # Relation avec Cartes_acces, avec le back_populates
    carte_acces: "Cartes_acces" = Relationship(back_populates="membres")


    # Étend la définition existante de cette table si nécessaire
    __table_args__ = {"extend_existing": True}



class Coachs(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    nom_coach : str
    specialite : str

    #cours: list['Cours'] = Relationship(back_populates="cours")

    # Étend la définition existante de cette table si nécessaire
    __table_args__ = {"extend_existing": True}

class Cours(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    nom_cours : str
    horaire : datetime.datetime = Field(default= None)
    capacite_max : int

    coach_id: Optional[int]= Field(default = None, foreign_key= 'coachs.id')
    # coach: "Coachs" = Relationship(back_populates="cours")

    # inscription : list['Inscription'] = Relationship(back_populates= 'inscription')

    # Étend la définition existante de cette table si nécessaire
    __table_args__ = {"extend_existing": True}


class Inscription(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    date_inscription : datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    membre_id: Optional[int]= Field(default = None, foreign_key= 'membres.id')
    # membre: "Membres" = Relationship(back_populates="inscription")

    cours_id : Optional[int]= Field(default = None, foreign_key= 'cours.id')
    # Cours: "Cours" = Relationship(back_populates="inscription")

    # Étend la définition existante de cette table si nécessaire
    __table_args__ = {"extend_existing": True}

sqlite_file_name = "database.db"  


sqlite_url = f"sqlite:///{sqlite_file_name}" 

engine = create_engine(sqlite_url, echo=True)  




def create_db_and_tables():  


    SQLModel.metadata.create_all(engine)  



# More code here later 👈

if __name__ == "__main__":  


    create_db_and_tables() 