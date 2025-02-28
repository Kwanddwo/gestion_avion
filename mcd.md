### **Gestion des avions**
[GDF graphique](https://lucid.app/lucidchart/c8cb7626-89e6-4ff8-bb54-253da5e9c9ed/edit?viewport_loc=-222%2C-1136%2C4858%2C2096%2C0_0&invitationId=inv_d1414001-bfe3-4d20-a25e-5551a47f8e4c)
[MCD graphique](https://lucid.app/lucidchart/42662a37-ddb1-40c9-9f54-fc8262fb4091/edit?viewport_loc=26%2C-426%2C3612%2C1559%2C0_0&invitationId=inv_8a89b89b-8c19-4986-831b-5c7490f19732)
#### **Entités**

- **AVION**

    - **NUMAV** : Numéro d'immatriculation (clé primaire)
    - **TYPAV** : Type de l'avion (exemple : B747, A300)
    - **DATMS** : Date de mise en service
    - **NBHDDREV** : Nombre d'heures de vol depuis la dernière révision REVISION
    - **DATDREV** : Date de la denière révision
    - **NBRHVOL** : Nombre d'heures de vol totale
    
- **REVISION**

    - **IDREV** : Identifiant unique de la révision (clé primaire)
    - **NUMAV** : Référence vers l'avion (clé étrangère)
    - **DATREV** : Date de la révision
    - **NBHREV** : Nombre total d’heures de vol au moment de la révision (statique)
    - **TEXTE** : Rapport de révision (anomalies constatées, réparations effectuées, organes changés)
### **Associations**

- **Faire Révision**
    - **Entre** : **AVION** et **REVISION**
    - **Cardinalités** :
        - **AVION** : (0, N) - Un avion peut avoir plusieurs révisions.
        - **REVISION** : (1, 1) - Une révision est liée à un seul avion.

### **Contraintes Métier :**

- Les attributs `TYPAV` et `DATMS` de l’entité **AVION** ne peuvent pas être modifiés après leur enregistrement initial.
- la date `DATDREV` est changez au date actuelle a chaque révision enregistrée
- Le conteur `NBHDDREV`est remis a zéro a chaque révision
- Une révision est obligatoire si :
    - La dernière révision remonte à plus de 6 mois ou 1000h.
- Il est interdit de retirer un avion si celui-ci est en vol.

### **Gestion des personnels**

#### **Entités**

- **PERSONNEL**
    
    - **NUMEMP** : Numéro d'employé (clé primaire)
    - **NOM** : Nom de l'employé
    - **PRENOM** : Prénom de l'employé
    - **TEL** : Numéro de téléphone
    - **ADRESSE** : Adresse
    - **SAL** : Salaire
    - **FONCTION** : Fonction de l'employé (exemple : mécanicien, pilote, steward)
    - **DATEMB** : Date d'embauche
- **PERSONNEL_NAVIGANT** _(Sous-type de PERSONNEL, car les informations supplémentaires concernent uniquement ce type de personnel)_
    
    - **NUMEMP** : Référence vers **PERSONNEL** (clé primaire, clé étrangère)
    - **NBMHV** : Nombre d'heures de vol du mois en cours (dynamique, mis à jour après chaque vol)
    - **NBTHV** : Nombre total d'heures de vol (cumulé pour la durée de l'emploi)

#### **Associations**

- **Navigont**
    - **Entre** : **PERSONNEL** et **NAVIGANT**
    - **Cardinalités** :
        - **PERSONNEL** : (0, 1) - un personnel navigant peut exister, mais ce n’est pas obligatoire
        - **NAVIGANT** : (1, 1) - est un obligatoire un personnel


### **Gestion des vols et Catalogue des vols**

#### **Entités**

- **VOL**
    
    - **NUMVOL** : Numéro de vol (clé primaire).
    - **VILDEP** : Ville de départ.
    - **VILARR** : Ville d'arrivée.
    - **HDEP** : Heure de départ.
    - **DURVOL** : Durée du vol.
    
- **PROGRAMMATION_VOL**
    
    - **IDPROG** : Identifiant unique de la programmation (clé primaire).
    - **NUMVOL** : Référence vers **VOL** (clé étrangère).
    - **JVOL** : Jour de la semaine où le vol est programmé (exemple : lundi, mardi...).
- **ESCALE**
    
    - **IDESCALE** : Identifiant unique de l'escale (clé primaire).
    - **NUMVOL** : Référence vers **VOL** (clé étrangère).
    - **NOORD** : Numéro d'ordre de l'escale (indique la séquence des escales dans l'itinéraire).
    - **VILESC** : Ville de l'escale.
    - **HARRESC** : Heure d'arrivée à l'escale.
    - **DURESC** : Durée de l'escale.

### **Associations et Cardinalités**

- **Programer**
    - **Entre**: VOL et PROGRAMMATION_VOL
    - **Cardinalités** 
        - **VOL** : (1, 1)  (un vol doit être référencé au moins une fois).
        - **PROGRAMMATION_VOL** : (0, N)  (un vol peut être programmé plusieurs fois ou ne pas être programmé du tout).

- **Escaler**
    - **Entre**: VOL et ESCALE
    - **Cardinalités** 
        - **VOL** : (1, 1)  (un vol doit être référencé au moins une fois).
        - **ESCALE** : (0, N) (un vol peut avoir aucune ou plusieurs escales)



### **Relations Entre Les Differents Gestions**

#### **VOL_NAVIGANT**
- **Entre** : VOL _NAVIGANT
- **Cardinalités** :
    - **VOL** : (1, N) (un vol peut avoir plusieurs personnels navigants)
    - **PERSONNELNAVIGANT** : (1, N) (un personnel navigant peut être affecté à plusieurs vols)

#### **VOL_AVION**

- **Entre** : VOL et AVION
- **Cardinalités** :
    - **VOL** : (1, 1) (un vol doit avoir un avion spécifique)
    - **AVION** : (1, N) (un avion peut être affecté à plusieurs vols)
