# Lab 8 : Extraire les données et évaluer la qualité des études

## 1. Lien entre Research Questions (RQ) et Variables d'Extraction

Les variables extraites découlent directement des questions de recherche fixées dans le protocole (22 études incluses) :
*   **RQ1 (Cibles et références) :** Maladie/Pathogène/Stress (ex: *Xylella fastidiosa*, *Verticillium dahliae*, stress hydrique) ; Variable de référence (qPCR, potentiel hydrique, labels visuels).
*   **RQ2 (Plateformes et capteurs) :** Plateforme (Satellite, UAV, Aéroporté) ; Capteur (Multispectral, Hyperspectral, Thermique, RGB).
*   **RQ3 (Méthodes IA) :** Famille d'algorithme (Machine Learning classique, Deep Learning) ; Modèle spécifique.
*   **RQ4 (Performance et validation) :** Métrique principale (OA, $R^2$, Recall) ; Niveau de validation (échelle V0-V5 détaillée dans le protocole).
*   **RQ5 (Déploiement) :** Niveau de maturité de déploiement (échelle DRL1-DRL5).

## 2. Grille d'Extraction (Échantillon de 5 études réelles)

| ID | Année | Plateforme (Capteur) | Cible (Référence) | Méthode (Modèle) | Validation (Niveau) | Résultats | Limitations (Fuites potentielles) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S01 | 2018 | Aéroporté (HS + TIR) | *Xylella* (qPCR partiel) | ML (SVM, Boosting) | V3 (CV, 2 années) | OA: 80.9%, $\kappa$: 0.61 | 1 groupe de recherche, pas de validation externe stricte. |
| S02 | 2022 | UAV (RGB) | Maladies foliaires (Images) | DL (MobiRes-Net) | V2 (Split 80/20 aléatoire) | Accuracy: 97.1% | Split d'images aléatoire (fuite par augmentation), pas de réf labo. |
| S03 | 2023 | UAV (RGB) | *Verticillium* (Images) | DL (YOLOv5) | V3 (Split 60/20/20 spatial) | Radar chart (pas de valeur) | Aucune métrique textuelle/tabulaire reportée. |
| S04 | 2025 | Aéroporté (HS + TIR) | *Xylella* (qPCR) | ML (SVM) | V4 (Test inter-zones) | OA interne: $\ge 74\%$, Recall test externe: 10% | Chute massive du rappel au transfert inter-zones, masquée par l'OA due au déséquilibre des classes. |
| S05 | 2026 | Satellite (PlanetScope) | Potentiel hydrique (Chambre) | ML (XGBoost) | V4 (Hold-out saisons/zones) | $R^2$: 0.84 (aléatoire), 0.82 (transfert) | Modèle validé uniquement avec ajout de variables météorologiques. |

## 3. Normalisation des Termes Utilisés

Afin d'assurer la comparabilité pour la synthèse :
*   **Plateforme :** `drone`, `uas`, `unmanned aerial` $\rightarrow$ `UAV` ; `aircraft` $\rightarrow$ `Aéroporté`.
*   **Cible :** `water status`, `drought` $\rightarrow$ `Stress hydrique/sécheresse`.
*   **Algorithmes :** `CNN`, `ResNet`, `YOLO` $\rightarrow$ `Deep Learning` ; `SVM`, `RF`, `Gaussian process` $\rightarrow$ `ML Classique`.
*   **Validation :** Conversion des descriptions textuelles en niveaux stricts (V0 = pas de métrique ; V1 = split non décrit ; V2 = split aléatoire/CV interne ; V3 = multi-sites/saisons sans transfert ; V4 = test de transfert explicite).

## 4. Application de la Grille de Quality Assessment (QA)

La qualité a été évaluée via 10 critères (Q1-Q10) notés de 0 à 2. La médiane sur le corpus (22 études) est de 10,5/20. Justification sur l'échantillon extrait :

*   **S05 (Martínez-Ruedas 2026) - Score : 18/20 (Haute qualité).** Justification : Représentativité élevée (Q2=2), référence physiologique directe (Q3=2), test d'indépendance avec validation croisée spatiale et temporelle (Q5=2, Q8=2).
*   **S01 (Zarco-Tejada 2018) - Score : 16/20 (Haute qualité).** Justification : Objectifs clairs (Q1=2), confirmation qPCR (Q3=2) et partage du code source (Q9=2). Perte de points due à l'absence de test d'indépendance strict sur données non vues (Q5=1).
*   **S03 (Mamalis 2023) - Score : 12/20 (Qualité moyenne).** Justification : Bonne représentativité terrain (Q2=1), mais référence faible basée sur de la seule annotation visuelle sans validation labo (Q3=0).
*   **S02 (Ksibi 2022) - Score : 9/20 (Qualité faible).** Justification : Absence de représentativité terrain (Q2=0), annotations d'images sans protocole (Q3=0) et validation sur un simple split aléatoire sujet aux fuites de données (Q5=1).

**Synthèse des scores de qualité :** L'évaluation révèle que les scores de qualité sont généralement plus élevés pour les études utilisant le ML classique (médiane 12) par rapport au DL (médiane 8.5), principalement parce que les études DL du corpus souffrent d'une vérité terrain faible (pas de qPCR/mesure physio) et d'un manque de tests de transfert spatial/temporel.
