# brief_sport

Documentation de la Base de Données - Salle de Sport
1. Cartes d'Accès (Cartes_acces)

La table Cartes d'Accès contient les informations relatives aux cartes d'accès des membres. Chaque carte est associée à un membre et permet d'identifier l'abonnement et la validité de l'accès à la salle.
Structure de la table
Champ	Type	Description
id	INT	Identifiant unique de la carte d'accès (clé primaire)
numero_unique	INT	Numéro unique de la carte d'accès
Relations

    Membres : Un membre peut avoir une carte d'accès. La relation est définie par le champ membres qui se connecte avec la table Membres.

Exemple de modèle

class Cartes_acces(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    numero_unique: int | None

    membres: List['Membres'] = Relationship(back_populates="carte_acces")

2. Membres (Membres)

La table Membres contient les informations sur les membres de la salle de sport, y compris leurs coordonnées personnelles et leur carte d'accès.
Structure de la table
Champ	Type	Description
id	INT	Identifiant unique du membre (clé primaire)
nom	VARCHAR(100)	Nom du membre
email	VARCHAR(100)	Adresse email du membre
carte_acces_id	INT	Clé étrangère vers Cartes_acces.id
Relations

    Cartes d'Accès : Chaque membre peut être lié à une carte d'accès via le champ carte_acces.
    Inscriptions : Chaque membre peut s'inscrire à plusieurs cours via la table Inscriptions.

Exemple de modèle

class Membres(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom: str
    email: str

    carte_acces_id: Optional[int] = Field(default=None, foreign_key='cartes_acces.id')
    carte_acces: Optional['Cartes_acces'] = Relationship(back_populates="membres")

    inscriptions: List['Inscription'] = Relationship(back_populates="membre")

3. Coachs (Coachs)

La table Coachs contient les informations sur les coachs de la salle de sport, y compris leur spécialité et leurs cours.
Structure de la table
Champ	Type	Description
id	INT	Identifiant unique du coach (clé primaire)
nom_coach	VARCHAR(100)	Nom du coach
specialite	VARCHAR(100)	Spécialité du coach (ex: yoga, musculation)
Relations

    Cours : Chaque coach peut animer plusieurs cours, liés à la table Cours.

Exemple de modèle

class Coachs(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom_coach: str
    specialite: str

    cours: List['Cours'] = Relationship(back_populates="coach")

4. Cours (Cours)

La table Cours contient les informations sur les différents cours proposés par la salle de sport, y compris les horaires, la capacité et le coach qui les anime.
Structure de la table
Champ	Type	Description
id	INT	Identifiant unique du cours (clé primaire)
nom_cours	VARCHAR(100)	Nom du cours
horaire	DATETIME	Date et heure du cours
capacite_max	INT	Capacité maximale du cours
coach_id	INT	Clé étrangère vers Coachs.id
Relations

    Coach : Chaque cours est animé par un coach, lié via le champ coach.
    Inscriptions : Un cours peut avoir plusieurs inscriptions de membres, liées via la table Inscriptions.

Exemple de modèle

class Cours(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom_cours: str
    horaire: datetime.datetime = Field(default=None)
    capacite_max: int

    coach_id: Optional[int] = Field(default=None, foreign_key='coachs.id')
    coach: Optional['Coachs'] = Relationship(back_populates="cours")

    inscriptions: List['Inscription'] = Relationship(back_populates="cours")

5. Inscriptions (Inscription)

La table Inscriptions enregistre les inscriptions des membres aux différents cours. Chaque inscription lie un membre à un cours à une date spécifique.
Structure de la table
Champ	Type	Description
id	INT	Identifiant unique de l'inscription (clé primaire)
date_inscription	DATETIME	Date et heure de l'inscription
membre_id	INT	Clé étrangère vers Membres.id
cours_id	INT	Clé étrangère vers Cours.id
Relations

    Membre : Chaque inscription est liée à un membre, via la clé étrangère membre_id.
    Cours : Chaque inscription est liée à un cours, via la clé étrangère cours_id.

Exemple de modèle

class Inscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date_inscription: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    membre_id: Optional[int] = Field(default=None, foreign_key='membres.id')
    membre: Optional['Membres'] = Relationship(back_populates="inscriptions")

    cours_id: Optional[int] = Field(default=None, foreign_key='cours.id')
    cours: Optional['Cours'] = Relationship(back_populates="inscriptions")

Diagramme des Relations

Voici un diagramme simple représentant les relations entre les entités de la base de données :

+--------------------+         +--------------------+         +------------------+
|    Membres         | 1     * |   Inscriptions     | *     1 |      Cours       |
+--------------------+         +--------------------+         +------------------+
| id                 |         | id                 |         | id               |
| nom                |         | date_inscription   |         | nom_cours        |
| email              |         | membre_id (FK)     |         | horaire          |
| carte_acces_id (FK)|         | cours_id (FK)      |         | capacite_max     |
+--------------------+         +--------------------+         +------------------+
         |                            |                               |
         |                            |                               |
         |                            |                               |
         |                            |                               |
         v                            v                               v
+--------------------+         +------------------+
|   Cartes_acces     | 1     * |      Coachs      |
+--------------------+         +------------------+
| id                 |         | id               |
| numero_unique      |         | nom_coach        |
+--------------------+         | specialite       |
                               +------------------+

Conclusion

Cette structure de base de données permet une gestion complète d'une salle de sport. Les relations entre les membres, les cours, les coachs, et les inscriptions sont clairement définies et permettent une gestion fluide des opérations.
