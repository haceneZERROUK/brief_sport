from creation_table import Membres, engine,Cartes_acces, Coachs, Cours, Inscription
from sqlmodel import Field, Session, SQLModel, create_engine, select
from faker import Faker
from random import choice, randint
import datetime

fake = Faker()

#region nb_membre

def nb_membre():
    
    with Session(engine) as session:
        new_carte = Cartes_acces(numero_unique = fake.random_int(0,1000))
        session.add(new_carte)
        session.commit()
        membre = Membres(nom=fake.name(), email=fake.email(),carte_acces_id= new_carte.id)
        session.add(membre)
        session.commit()

        

#region new_coach

def new_coach(spe_possible):
    

    with Session(engine) as session:
        
        specialite_coach = choice(spe_possible)
        coach = Coachs(nom_coach =fake.name(),specialite= specialite_coach)
        session.add(coach)
        session.commit()
    #spe_possible.remove(specialite_coach)

#region recup_membres
def recup_id_membres():
    with Session(engine) as session:
        id_des_membres= session.exec(select(Membres.id)).all()
        return id_des_membres
#region select_coach_id
def select_coach_id():
    with Session(engine) as session:
        id_des_coachs = session.exec(select(Coachs.id)).all()
        return id_des_coachs

#region recu_specialite

def recup_specialite(id_spe):

    with Session(engine) as session:
        specialite_coach = session.exec(select(Coachs.specialite).where(Coachs.id == id_spe)).first()
        return specialite_coach 
    
#region recup_cours_id  
    
def recup_cours_id():

    with Session(engine) as session:
        id_des_cours = session.exec(select(Cours.id)).all()
        return id_des_cours


#region recup_date_cours

def recup_date_cours(cours_id):
    with Session(engine) as session:
        date_cours = session.exec(select(Cours.horaire).where(Cours.id == cours_id)).first()
        return date_cours     

#region creation_cours

def creation_cours(nb_cours : int):

    horaire_utilise = []



    while len(horaire_utilise) <= nb_cours:
        id_coach_cours = choice(select_coach_id())
        specialite_cours = recup_specialite(id_coach_cours)
        horaire = datetime.datetime(2024, 12, randint(1, 31), randint(9, 17))

        if horaire in horaire_utilise:
            #horaire = datetime.datetime(2024, 12, randint(1, 31), randint(9, 17))
            continue
        
        else:
            horaire_utilise.append(horaire)
            
            capacite_max = 8

            new_cours = Cours(
                nom_cours=f"cours de {specialite_cours} le {horaire.day} / {horaire.month} à {horaire.hour}",
                horaire=horaire,
                capacite_max=capacite_max,
                coach_id=id_coach_cours
            )
            with Session(engine) as session:
                session.add(new_cours)
                session.commit()

#region remplir les cours


def remplir_les_cours():
    
    liste_membres = recup_id_membres()

    for membre in liste_membres:
        #date_inscri = datetime.datetime(2024, randint(11,12), randint(1, 31), randint(9, 17))

        nb_cours = 3

        for cours in range(nb_cours):
            id_du_cours = recup_cours_id()
            choisir_un_cours = choice(id_du_cours)
            date_cours = recup_date_cours(choisir_un_cours)

            date_inscri = datetime.datetime(3000, 12,1)

            while date_cours < date_inscri:
                date_inscri = datetime.datetime(2024, randint(11,12), randint(1, 30), randint(0, 23))
            
            new_inscription = Inscription(
            date_inscription= date_inscri,
            membre_id= membre,
            cours_id = choisir_un_cours,
            )
            with Session(engine) as session:
                session.add(new_inscription)
                session.commit()

            
#region main
def main(n):
    for i in range(n):
        nb_membre()

    spe_possible = ["Yoga", "Pump", "Pilates", "Musculation", "Boxe"] 

    for i in range(n//6):
        new_coach(spe_possible)




if __name__ == "__main__":  

    main(40)

    creation_cours(150)
    remplir_les_cours()


