# COMPAGNIE AÉRIENNE

## Objectifs
- **Gestion des avions**
- **Gestion des personnels**
- **Gestion des vols**

---

## 1. Gestion des Avions

### Attributs des Avions
- **Avion**: `NUMAV`, `TYPEAV`, `DATMS`, `DATDERREV`
- Les avions doivent être révisés tous les **6 mois** ou toutes les **1000 heures de vol**. Sinon, ils sont interdits de vol.

### Révisions
- **Révision**: `rapport` (TEXTE), `DATREV`
  - Lorsqu'une révision est enregistrée, le champ `DATDERREV` de l'avion correspondant doit être mis à jour.

### Contraintes
- **Création et suppression** des avions sont autorisées.
- **Modification interdite** pour les champs: `TYPEAV` et `DATMS`.

---

## 2. Gestion des Personnels

### Attributs des Personnels
- **Personnel**: Deux catégories:
  1. **Navigants**
  2. **Non-navigants**
- Champs communs:
  - `NUMEMP` (ID), `NOM`, `PRENOM`, `NTEL`, `ADRESSE` (CO), `SALAIRE`, `FONCTION`, `DATEMB`

### Personnels Navigants
- **Nombre d’heures de vol**:
  - Heures de vol du **mois en cours**.
  - **Totalité des heures de vol** (`NBTHV`).
- Ces données sont:
  - Initialisées manuellement à l’embauche.
  - Mises à jour automatiquement après chaque vol.

---

## 3. Gestion des Vols

### Catalogue des Vols
- Diffusion d'un **catalogue sémainier des vols**.

### Attributs des Vols
- **Vol**:
  - `NUMVOL` (ID), `VILDEP`, `VILARR`, `HEUREDEP`, `DURVOL`.
- Un même numéro de vol:
  - Peut être programmé sur plusieurs jours de la semaine (`JVOL`).
  - Ne peut être programmé qu’une seule fois par jour.

### Escales
- **Attributs des escales**:
  - `VILESC`, `HEUREARRESC`, `DUREESC`, `NOORD` (Nombre ordinal, décrivant l'ordre des escales).

---

## Tâches à Réaliser

### 1. Analyse & Conception
#### Phases:
1. **MCD**: DD, GDF, et MCD (DONE)
2. **MLD**: Modèle logique des données
3. **MCT**: Modèle conceptuel des traitements
4. **MOT**: Modèle opérationnel des traitements
5. **Requétes utiles**

---

### 2. Implémentation

#### 2.1. Base de Données
- Création des models (DONE)
  
#### 2.2. Backend
- **Django**:
  - Connexion avec MySQL (DONE)
  - **Opérations CRUD**:
    - Première étape: Base de données ➡ Backend (Done by ORM)
    - Deuxième étape: Backend ➡ Frontend (Views)
  - Implémentation des **traitements (MOT)** dans les **views**.
  - Sécurité:
    - Gestion des comptes admin (enregistrement, connexion, `@login_required`).

#### 2.3. Frontend
- Templates: **HTML** + **Jinja**
- Styling: **Bootstrap**, **CSS**, et **JavaScript**.
