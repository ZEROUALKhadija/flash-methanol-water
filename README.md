# Simulation d’un séparateur flash binaire Méthanol–Eau avec Python

## 1. Présentation du projet

Ce projet consiste à développer un programme Python permettant de simuler la séparation d’un mélange binaire méthanol–eau dans un séparateur flash à l’équilibre liquide-vapeur.

L’objectif est de déterminer les débits et les compositions des phases liquide et vapeur à la sortie du séparateur, puis de comparer les résultats obtenus avec ceux du simulateur de procédés **DWSIM**.

Le projet met en œuvre des méthodes de thermodynamique des mélanges, des calculs d’équilibre liquide-vapeur et une résolution numérique de l’équation de Rachford–Rice.

## 2. Données du procédé

| Paramètre | Valeur |
|---|---:|
| Mélange étudié | Méthanol–Eau |
| Débit molaire d’alimentation | 50 mol/h |
| Fraction molaire de méthanol | 0,40 |
| Fraction molaire d’eau | 0,60 |
| Température d’alimentation | 25 °C |
| Température du séparateur | 80 °C |
| Pression de fonctionnement | 1 atm (101,325 kPa) |

Le mélange est chauffé jusqu’à 80 °C, puis envoyé dans un séparateur flash où les phases liquide et vapeur sont séparées.

## 3. Modèle thermodynamique

Le calcul de l’équilibre liquide-vapeur repose sur les éléments suivants :

- **Modèle NRTL (Non-Random Two-Liquid)** : prise en compte de la non-idéalité de la phase liquide.
- **Équation d’Antoine** : estimation des pressions de vapeur saturante des composants purs.
- **Constantes d’équilibre \(K_i\)** : calculées à partir des coefficients d’activité et des pressions de vapeur saturante, sous l’hypothèse d’une phase vapeur idéale.

La relation utilisée est :

\[
K_i=\frac{\gamma_i P_i^{sat}}{P}
\]

où \(\gamma_i\) est le coefficient d’activité du composant \(i\), \(P_i^{sat}\) sa pression de vapeur saturante et \(P\) la pression totale.

**Remarque :** les résultats dépendent des paramètres d’interaction NRTL utilisés et des hypothèses thermodynamiques retenues.

## 4. Méthode de calcul

La simulation suit les principales étapes suivantes :

1. Initialisation des données d’alimentation et des conditions opératoires.
2. Calcul des pressions de vapeur saturante à l’aide de l’équation d’Antoine.
3. Estimation des coefficients d’activité avec le modèle NRTL.
4. Calcul des constantes d’équilibre liquide-vapeur \(K_i\).
5. Résolution numérique de l’équation de Rachford–Rice pour déterminer la fraction vaporisée.
6. Calcul des compositions molaires des phases liquide et vapeur.
7. Détermination des débits molaires des deux phases et vérification du bilan matière.
8. Génération des résultats et des graphiques.

L’équation de Rachford–Rice est :

\[
\sum_i\frac{z_i(K_i-1)}
{1+\beta(K_i-1)}=0
\]

où \(z_i\) représente la fraction molaire du composant \(i\) dans l’alimentation et \(\beta\) la fraction molaire vaporisée.

Les débits des phases sont calculés par :

\[
V=\beta F
\]

\[
L=(1-\beta)F
\]

avec \(F\) le débit molaire total, \(V\) le débit de vapeur et \(L\) le débit de liquide.

## 5. Technologies utilisées

- **Python** : développement et calculs numériques.
- **NumPy** : opérations numériques et calcul matriciel.
- **Matplotlib** : génération des graphiques.
- **DWSIM** : simulation de référence et comparaison des résultats.

## 6. Structure du projet

```text
flash-methanol-water/
│
├── main.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── thermodynamics.py
│   ├── rachford_rice.py
│   ├── energy_balance.py
│   └── plots.py
│
└── results/
    ├── resultats.txt
    ├── data/
    └── figures/
```

- `main.py` : lancement de la simulation.
- `thermodynamics.py` : propriétés thermodynamiques et modèle NRTL.
- `rachford_rice.py` : résolution de l’équilibre flash et calcul des débits et compositions.
- `energy_balance.py` : calcul thermique implémenté dans le projet.
- `plots.py` : génération des graphiques.
- `results/` : fichiers de résultats et figures générées.

## 7. Installation et exécution

### Prérequis

- Python 3.10 ou version compatible avec les dépendances du projet.
- pip.

### Installation

Cloner le dépôt :

```bash
git clone <URL_DU_DEPOT>
cd flash-methanol-water
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer la simulation :

```bash
python main.py
```

Les résultats sont ensuite enregistrés dans le dossier `results/`, selon la configuration du programme.

## 8. Validation et comparaison avec DWSIM

Les résultats de la simulation Python sont comparés à ceux obtenus avec DWSIM dans les mêmes conditions opératoires.

La comparaison porte notamment sur :

- la fraction vaporisée ;
- les débits molaires des phases liquide et vapeur ;
- les compositions molaires à l’équilibre ;
- la cohérence du bilan matière.

Les premiers résultats obtenus avec le modèle NRTL sont proches de ceux de DWSIM. Les éventuels écarts peuvent dépendre des paramètres thermodynamiques, des méthodes de calcul et des hypothèses utilisées dans chaque simulateur.

## 9. Limites du modèle

La précision de la simulation dépend des paramètres d’interaction NRTL et de la validité des hypothèses adoptées. Le bilan énergétique doit également être interprété selon les calculs effectivement implémentés dans `energy_balance.py` : un calcul de chauffage sensible ne constitue pas, à lui seul, un bilan enthalpique complet de l’équilibre flash.

## 10. Objectifs pédagogiques

Ce projet permet de mettre en pratique :

- la thermodynamique des équilibres liquide-vapeur ;
- la modélisation et la simulation des procédés ;
- les méthodes numériques appliquées au génie chimique ;
- la programmation scientifique avec Python ;
- la validation de modèles par comparaison avec un simulateur de procédés.

---

**Projet académique — Génie des procédés et ingénierie chimique**
