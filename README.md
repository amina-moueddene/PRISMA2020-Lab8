# Lab 8 : Extraire les données et évaluer la qualité des études (PRISMA 2020)

**Sujet de la revue systématique :** *Machine learning and remote sensing for disease and stress detection in olive* (22 études incluses).

---

## 1. Lien entre Research Questions (RQ) et Variables d'Extraction

Les variables extraites dans la grille (`data/fulltext_extraction_22_studies.csv`) découlent directement des questions de recherche fixées dans le protocole :

* **RQ1 (Cibles et références terrain) :** `target` (Maladie/Pathogène/Stress : *Xylella fastidiosa*, *Verticillium dahliae*, maladies foliaires, stress hydrique/sécheresse), `task` (classification, régression, segmentation), `evaluation_unit` (arbre, pixel, parcelle) et `reference_data` (qPCR, potentiel hydrique à la chambre de Scholander, sévérité visuelle).
* **RQ2 (Plateformes et capteurs) :** `platform` (Satellite, UAV, Aéroporté), `sensor` (Multispectral, Hyperspectral, Thermique, RGB, SAR), `modality`, `resolution` et `fusion`.
* **RQ3 (Méthodes d'IA) :** `ai_family` (Machine Learning classique vs Deep Learning), `algorithms` (SVM, Random Forest, XGBoost, LDA, CNN, ResNet, YOLO, etc.) et `baseline`.
* **RQ4 (Performance et rigueur de validation) :** `metrics` (valeurs brutes et normalisées : OA, R², Recall, Precision, F1, κ, RMSE), `validation_design`, `transfer_test`, `early_detection` et niveau de validation standardisé (`validation_level` : échelle V0–V4).
* **RQ5 (Déploiement et reproductibilité) :** `deployment`, `explainability`, `data_code_availability` et niveau de maturité opérationnelle (`deployment_level` : échelle DRL1–DRL5).

---

## 2. Grille d'Extraction (Défi 1 — Échantillon de 5 études réelles)

L'ensemble des 22 études extraites est fourni dans `data/fulltext_extraction_22_studies.csv`. Le tableau ci-dessous présente 5 études représentatives du corpus :

| ID | Record | Étude (Année) | Plateforme (Capteur) | Cible (Référence) | Méthode (Modèle) | Validation (Niveau) | Résultats (Bruts → Normalisés) | Limitations / Fuites potentielles |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | 6 | Zarco-Tejada et al. (2018) | Aéroporté (HS + TIR) | *Xylella fastidiosa* (Inspection >7000 arbres + qPCR sur 157 arbres) | ML Classique (SVM RBF, Stochastic Gradient Boosting) | **V3** (Leave-one-out CV sur 2 années) | `OA: 80.9%, κ: 0.61` → `OA=0.809, Kappa=0.61` | Pas de test de transfert explicite train-année / test-année. |
| **S02** | 33 | Ksibi et al. (2022) | UAV (RGB) | Maladies foliaires (*Aculus olearius*, œil de paon — labels visuels) | Deep Learning (MobiRes-Net : ResNet50 + MobileNet) | **V2** (Split aléatoire 80/20 d'images) | `Accuracy: 97.08%` → `OA=0.971` | Split aléatoire d'images (risque de fuite spatiale/augmentation), pas de validation labo. |
| **S03** | 43 | Mamalis et al. (2023) | UAV (RGB) | *Verticillium dahliae* (Labels visuels) | Deep Learning (YOLOv5) | **V3** (Split 60/20/20 stratifié par parcelle) | Radar chart uniquement (`fitness: 0.65`) → `Non rapporté numériquement` | Aucune valeur numérique exacte (Precision/Recall/mAP) reportée dans le texte ou en tableau. |
| **S04** | 65 | D'Addabbo et al. (2025) | Aéroporté (HS + TIR) | *Xylella fastidiosa* (qPCR) | ML Classique (SVM) | **V4** (Leave-K-out CV + test inter-zones Gorgognolo → Polignano) | `OA interne ≥74%; externe OA 92.3%, Recall 10%, FP 18.2%` → `Recall_ext=0.10` | Effondrement du rappel (10 %) lors du transfert inter-zones, masqué par une OA élevée due au déséquilibre des classes. |
| **S05** | 93 | Martínez-Ruedas et al. (2026) | Satellite (PlanetScope + météo) | Stress hydrique (Potentiel hydrique de tige) | ML Classique (XGBoost) | **V4** (Split 80/20 + hold-out spatial par zone + hold-out saisonnier) | `R²: 0.84 (aléatoire), 0.837 (zone), 0.817 (saison), RMSE: 0.28 MPa` | Performances dépendantes de l'intégration de variables météorologiques auxiliaires. |

---

## 3. Normalisation des Termes et des Métriques

Afin de permettre l'agrégation comparative sans altérer la traçabilité des sources, les valeurs originales sont conservées et doublées de colonnes normalisées (`scripts/normalize_and_qa.py`) :

* **Plateformes :** `drone`, `uas`, `multirotor`, `unmanned aerial` $ightarrow$ `UAV` ; `aircraft`, `manned` $ightarrow$ `Airborne`.
* **Cibles :** `water status`, `stem water potential`, `drought` $ightarrow$ `Water stress / Drought`.
* **Familles d'algorithmes :** `CNN`, `ResNet50`, `MobileNet`, `YOLOv5`, `encoder-decoder` $ightarrow$ `Deep learning` ; `SVM`, `Random forest`, `XGBoost`, `LDA`, `QDA`, `Gaussian process` $ightarrow$ `Classical ML`.
* **Métriques (brutes vs normalisées) :** Conversion des pourcentages en proportions dans $[0, 1]$ (ex. `OA 80.9%` $ightarrow$ `0.809`) et harmonisation des synonymes (`Overall Accuracy` / `Correct rate` $ightarrow$ `OA` ; `Sensitivity` / `TPR` $ightarrow$ `Recall`).
* **Niveaux de validation (`validation_level`) :**
  * `V0` : Aucune métrique quantitative (évaluation qualitative uniquement).
  * `V1` : Protocole de découpage (split) non décrit.
  * `V2` : Découpage aléatoire ou validation croisée interne sur un même site/campagne.
  * `V3` : Données multi-sites ou multi-saisons sans test de transfert indépendant explicite.
  * `V4` : Test de transfert indépendant explicite (spatial inter-sites ou temporel inter-années).

---

## 4. Application de la Grille de Quality Assessment (Défi 2)

La qualité méthodologique des 22 études a été évaluée selon **10 critères (`Q1`–`Q10`)** notés sur une échelle de 0 à 2 (`0` = Non, `1` = Partiel, `2` = Oui), soit un score total sur **20 points** (`data/quality_assessment_Q1-Q10.csv`).

* **Score médian global (22 études) :** **10,5 / 20** (étendue : 4/20 à 18/20).
* **Comparaison par famille d'IA :** Les études en **Machine Learning classique** obtiennent une médiane de **12,0 / 20** contre **8,5 / 20** pour le **Deep Learning**, en raison d'une meilleure rigueur sur la vérité terrain biologique (qPCR / chambre à pression) et sur les tests d'indépendance spatiale/temporelle.

### Justification détaillée sur l'échantillon (Haute qualité vs Moyenne / Faible)

1. **S05 — Martínez-Ruedas et al. (2026) | Score : 18/20 (Haute qualité)**
   * *Points forts :* Objectifs explicites (`Q1=2`), représentativité multi-saisons et multi-zones (`Q2=2`), mesure physiologique directe du potentiel hydrique (`Q3=2`), protocole sans fuite avec hold-out spatial et temporel (`Q5=2`, `Q8=2`), métriques complètes (`Q6=2`, `Q7=2`).
   * *Points perdus :* Partage partiel du code/données (`Q9=1`) et discussion partielle des limites (`Q10=1`).
2. **S01 — Zarco-Tejada et al. (2018) | Score : 16/20 (Haute qualité)**
   * *Points forts :* Large échantillon terrain (>7000 arbres) et confirmation moléculaire par qPCR (`Q2=2`, `Q3=2`), traits biophysiques explicables par inversion de transfert radiatif (`Q4=2`), comparaison de baselines (`Q7=2`) et scripts R publics sur GitHub (`Q9=2`).
   * *Points perdus :* Absence de hold-out strict inter-années (`Q5=1`, `Q8=1`) et absence de section dédiée aux limites (`Q10=0`).
3. **S04 — D'Addabbo et al. (2025) | Score : 14/20 (Haute qualité)**
   * *Points forts :* Confirmation moléculaire qPCR (`Q3=2`), prétraitement complet (`Q4=2`), indépendance train/test stricte (`Q5=2`) et évaluation explicite du transfert inter-zones (`Q8=2`).
   * *Points perdus :* Absence de comparaison avec d'autres familles de modèles (`Q7=0`) et absence de partage de code/données (`Q9=0`).
4. **S03 — Mamalis et al. (2023) | Score : 12/20 (Qualité moyenne)**
   * *Points forts :* Stratification par parcelle (`Q2=1`, `Q5=1`, `Q8=1`) et architecture YOLOv5 bien documentée (`Q4=2`).
   * *Points perdus :* Vérité terrain uniquement visuelle sans confirmation PCR du *Verticillium* (`Q3=0`) et résultats présentés uniquement sous forme de graphique radar sans valeurs tabulaires (`Q6` pénalisé sur la précision des métriques).
5. **S02 — Ksibi et al. (2022) | Score : 9/20 (Qualité faible)**
   * *Points forts :* Objectifs clairs (`Q1=2`) et comparaison entre architectures CNN (`Q7=2`).
   * *Points perdus :* Faible représentativité terrain (`Q2=0`), absence de protocole de diagnostic biologique/laboratoire (`Q3=0`), split aléatoire 80/20 sujet aux fuites de données (`Q5=1`, `Q8=0`) et absence d'analyse des limites (`Q10=0`).

---

## 5. Questions de Vérification

### Q1. Pourquoi est-il important de lier les variables d'extraction aux Research Questions (RQ) ? Que se passe-t-il si vous extrayez des données non pertinentes ?
Lier chaque variable d'extraction à une RQ garantit que la grille sert exclusivement à répondre aux objectifs scientifiques définis dans le protocole PRISMA. Si l'on extrait des données non pertinentes :
1. On alourdit inutilement la grille et le temps de lecture du texte intégral ;
2. On augmente le taux d'erreur humaine et de valeurs manquantes (`NR`) ;
3. On introduit du bruit analytique et des comparaisons hors-périmètre qui nuisent à la clarté de la synthèse.

### Q2. Expliquez la différence entre une métrique « brute » et une métrique « normalisée ». Donnez un exemple concret.
* **Métrique brute :** Valeur, unité et intitulé exacts tels que rapportés par les auteurs dans l'article d'origine. Elle assure l'auditabilité et la traçabilité.
* **Métrique normalisée :** Valeur convertie dans une unité commune (proportion dans $[0, 1]$) et sous un nom standardisé afin de permettre l'agrégation et la comparaison entre études.
* *Exemple concret tiré du corpus :* Dans **Zarco-Tejada et al. (2018)** (`S01`), la métrique brute est rapportée sous la forme `Overall Accuracy = 80.9%` et dans **Ksibi et al. (2022)** (`S02`) sous la forme `Accuracy = 97.08%`. Après normalisation, les deux sont harmonisées sous la variable canonique `OA` avec les valeurs numériques `0.809` et `0.971`.

### Q3. Pourquoi le score de qualité ne doit-il pas être utilisé mécaniquement pour exclure des études ?
Un score de qualité faible reflète souvent un manque de transparence rédactionnelle (ex. code non publié ou protocole de split peu détaillé) plutôt qu'une invalidité scientifique des observations terrain. Exclure des études sur la base d'un seuil arbitraire introduirait un **biais de sélection** et réduirait la couverture du domaine (notamment sur les approches récentes en Deep Learning). Conformément aux recommandations **PRISMA 2020** et à l'approche **GRADE**, les scores QA sont utilisés pour **pondérer la certitude des preuves**, interpréter les écarts de performance (ex. l'inflation artificielle des métriques en validation V2 par rapport à V4) et réaliser des analyses de sensibilité.
