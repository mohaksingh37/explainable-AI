# 🏛️ Explainable AI for Legal Case Outcome Prediction

An Explainable Artificial Intelligence (XAI) based web application that predicts the possible outcome of a simulated legal case and explains **why the machine-learning model made that prediction**.

The project combines **Machine Learning, Flask, Random Forest, and Explainable AI techniques** to provide both a prediction and an understandable explanation of the factors influencing that prediction.

> **Important:** This project is an academic/demo prototype. It does not provide real legal advice or determine actual guilt or innocence. The model is trained using synthetically generated case data.

---

## 📌 Table of Contents

* [Project Overview](#-project-overview)
* [Objectives](#-objectives)
* [Key Features](#-key-features)
* [How the Project Works](#-how-the-project-works)
* [System Architecture](#-system-architecture)
* [Machine Learning Model](#-machine-learning-model)
* [Input Features](#-input-features)
* [Explainable AI](#-explainable-ai)
* [Project Structure](#-project-structure)
* [Technologies Used](#-technologies-used)
* [Installation](#-installation)
* [Running the Project](#-running-the-project)
* [Using the Application](#-using-the-application)
* [API](#-api)
* [Example Workflow](#-example-workflow)
* [Limitations](#-limitations)
* [Future Scope](#-future-scope)
* [Disclaimer](#-disclaimer)

---

# 📖 Project Overview

Legal decisions can involve many different factors, making it difficult to understand how a prediction system reaches a particular result.

This project demonstrates how **Explainable AI (XAI)** can be used with a machine-learning model to predict a simulated legal case outcome while also providing explanations for the prediction.

The system accepts information about a case such as:

* Evidence strength
* Number of witnesses
* Previous criminal record
* Legal representation
* Crime severity
* Evidence tampering
* Defendant cooperation
* Jurisdiction strictness
* Media coverage
* Time to trial

The data is processed and passed to a **Random Forest Classifier containing 200 decision trees**.

The model produces:

1. Predicted outcome
2. Prediction confidence
3. Outcome probabilities
4. Local feature explanations
5. Global feature importance
6. Tree voting information
7. Natural-language explanation

---

# 🎯 Objectives

The main objectives of the project are:

### 1. Legal Case Prediction

Develop a machine-learning system capable of predicting a simulated legal case outcome.

### 2. Explainability

Make the prediction understandable instead of treating the machine-learning model as a black box.

### 3. Feature Analysis

Identify which case features have the greatest influence on predictions.

### 4. Visualisation

Present predictions and explanations through an interactive web interface.

### 5. Educational Demonstration

Demonstrate how machine learning and Explainable AI can be applied to a legal-domain use case.

---

# ⭐ Key Features

## 🤖 Machine Learning Prediction

The application uses a **Random Forest Classifier** with 200 decision trees.

The model predicts between:

* **Acquitted**
* **Convicted**

---

## 📊 Prediction Probability

The application provides probabilities for both possible outcomes.

Example:

```text
Acquitted: 25%
Convicted: 75%
```

The outcome with the higher probability becomes the predicted result.

---

## 🔍 LIME Explanation

The application provides a local explanation showing which features influenced the prediction for the specific case being analyzed.

The approach works by changing/perturbing input features and observing how the model's prediction changes.

---

## 🧠 SHAP-Style Explanation

The project provides a SHAP-style feature contribution analysis.

The system changes individual features and compares the resulting prediction with the original prediction to estimate the contribution of each feature.

---

## 🌎 Global Feature Importance

Random Forest provides feature importance values that show which features are generally influential across the trained model.

For example:

```text
Evidence Strength       0.31
Crime Severity          0.19
Witness Count           0.14
Prior Criminal Record   0.11
...
```

---

## 🌳 Random Forest Tree Voting

The application can inspect the individual decision trees in the Random Forest and count their votes.

Example:

```text
Total Trees:       200
Convicted Votes:   156
Acquitted Votes:    44
```

This helps demonstrate how the ensemble arrives at its prediction.

---

# 🔄 How the Project Works

The complete workflow is:

```text
                ┌──────────────────┐
                │       USER       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Enter Case Data  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Flask Backend    │
                │     app.py       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Data Processing  │
                │ Pandas + Scaler  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Random Forest    │
                │   200 Trees      │
                └────────┬─────────┘
                         │
              ┌──────────┼───────────┐
              │          │           │
              ▼          ▼           ▼
           Prediction   LIME      SHAP-style
              │          │           │
              └──────────┼───────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Feature          │
                │ Importance       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Tree Voting      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Final Result     │
                │ + Explanation    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Web Interface    │
                └──────────────────┘
```

---

# 🏗️ System Architecture

The application consists of three main layers.

## 1. Frontend

The frontend provides the user interface.

Technologies:

* HTML
* CSS
* JavaScript
* Chart.js

The user enters case information and receives the prediction and explanation.

---

## 2. Backend

The backend is implemented using **Flask**.

The backend:

* Receives case information
* Converts input into a DataFrame
* Sends the data to the ML model
* Generates explanations
* Returns the result to the frontend

The primary API endpoint is:

```text
POST /predict
```

---

## 3. Machine Learning Layer

The ML layer contains the `LegalPredictionModel`.

It is responsible for:

* Dataset generation
* Data preprocessing
* Model training
* Prediction
* Probability calculation
* Feature importance
* LIME-style explanation
* SHAP-style explanation
* Tree voting

---

# 🤖 Machine Learning Model

The project uses:

```text
Random Forest Classifier
```

with:

```text
Number of Trees:       200
Maximum Tree Depth:    8
Minimum Split Samples: 5
Random State:          42
```

### Why Random Forest?

Random Forest is an ensemble learning method that combines multiple decision trees.

Instead of depending on one decision tree:

```text
             Random Forest
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Tree 1     Tree 2     Tree 3
        │          │          │
        └──────────┼──────────┘
                   │
             ...200 Trees...
                   │
                   ▼
             Majority Vote
                   │
                   ▼
              Prediction
```

This also allows the project to demonstrate tree-level voting and global feature importance.

---

# 📋 Input Features

The model uses 10 features.

| Feature                 | Description                                          | Range / Values |
| ----------------------- | ---------------------------------------------------- | -------------- |
| Evidence Strength       | Strength of evidence supporting the case             | 0–10           |
| Witness Count           | Number of witnesses                                  | 0–10           |
| Prior Criminal Record   | Whether there is a prior record                      | 0–1            |
| Legal Representation    | Type of legal representation                         | 0–2            |
| Crime Severity          | Severity of alleged crime                            | 1–5            |
| Evidence Tampering      | Whether evidence tampering occurred                  | 0–1            |
| Defendant Cooperation   | Level of cooperation                                 | 0–10           |
| Jurisdiction Strictness | Strictness of jurisdiction                           | 1–5            |
| Media Coverage          | Whether the case receives significant media coverage | 0–1            |
| Time to Trial           | Expected time until trial                            | 1–36 months    |

---

# 🔬 Dataset

The current project uses **synthetically generated data**.

The model generates approximately:

```text
1000 simulated cases
```

Each case contains the 10 features described above.

The generated data is then divided into training and testing sets.

```text
1000 Cases
    │
    ├───────────────┐
    │               │
    ▼               ▼
Training Data    Testing Data
    │               │
    ▼               ▼
80%              20%
    │
    ▼
Random Forest
    │
    ▼
Evaluation
```

Using synthetic data makes the project suitable for demonstrating the machine-learning and XAI workflow without using private or sensitive court records.

---

# 🧠 Explainable AI

A major objective of this project is not only to make a prediction but also to explain it.

The project provides four major explanation mechanisms.

---

## 1. LIME

### Local Explanation

LIME focuses on the **individual case**.

Conceptually:

```text
Original Case
     │
     ▼
Modify Features
     │
     ▼
Run Model Again
     │
     ▼
Compare Predictions
     │
     ▼
Identify Important Features
```

This helps answer:

> "Why did the model make this prediction for this particular case?"

---

## 2. SHAP-Style Explanation

The project uses an approximate SHAP-style feature ablation approach.

The basic process is:

```text
Original Prediction
       │
       ▼
Change One Feature
       │
       ▼
Predict Again
       │
       ▼
Compare Results
       │
       ▼
Calculate Contribution
```

This helps estimate how individual features affect the model's prediction.

---

## 3. Global Feature Importance

Global importance looks at the model as a whole.

It answers:

> "Which features are generally important to the Random Forest model?"

The Random Forest's built-in feature importance values are used for this analysis.

---

## 4. Tree Voting

Each decision tree in the Random Forest produces a prediction.

For example:

```text
Tree 1  → Convicted
Tree 2  → Acquitted
Tree 3  → Convicted
Tree 4  → Convicted
...
Tree 200 → Acquitted
```

The votes are counted to understand the ensemble's decision.

---

# 📁 Project Structure

```text
explainable-ai/
│
├── app.py
│
├── requirements.txt
│
├── models/
│   ├── __init__.py
│   └── legal_model.py
│
├── data/
│   ├── __init__.py
│   └── case_database.py
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── js/
        └── main.js
```

### File Description

| File               | Purpose                                    |
| ------------------ | ------------------------------------------ |
| `app.py`           | Main Flask application and API routes      |
| `legal_model.py`   | Machine-learning model and XAI logic       |
| `case_database.py` | Feature descriptions and sample cases      |
| `index.html`       | Main web interface                         |
| `style.css`        | Frontend styling                           |
| `main.js`          | Frontend interaction and API communication |
| `requirements.txt` | Required Python packages                   |

---

# 🛠️ Technologies Used

### Programming Language

* Python
* JavaScript
* HTML
* CSS

### Machine Learning

* Scikit-learn
* Random Forest
* StandardScaler

### Data Processing

* NumPy
* Pandas

### Backend

* Flask

### Visualisation

* Chart.js

### Explainable AI

* LIME-style local explanation
* SHAP-style feature contribution
* Random Forest feature importance
* Decision-tree voting

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

Move into the project directory:

```bash
cd explainable-ai
```

---

## 2. Create a Virtual Environment

### macOS/Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is not available, install the required packages manually:

```bash
python -m pip install numpy pandas scikit-learn flask matplotlib lime shap
```

---

# ▶️ Running the Project

After activating the virtual environment:

```bash
python app.py
```

The Flask application should start on the local development server.

Open:

```text
http://127.0.0.1:5000
```

in your web browser.

---

# 🖥️ Using the Application

### Step 1

Open the application in your browser.

### Step 2

Enter the legal case details.

For example:

```text
Evidence Strength:        8
Witness Count:            6
Prior Criminal Record:   Yes
Legal Representation:    Private Attorney
Crime Severity:           4
Evidence Tampering:      No
Defendant Cooperation:    4
Jurisdiction Strictness:  4
Media Coverage:           Yes
Time to Trial:            12 months
```

### Step 3

Click:

```text
Analyze Case
```

### Step 4

The frontend sends the information to:

```text
POST /predict
```

### Step 5

The backend processes the data and sends it to the Random Forest model.

### Step 6

The system generates:

* Prediction
* Confidence
* Probabilities
* LIME explanation
* SHAP-style explanation
* Global feature importance
* Tree votes
* Natural-language explanation

### Step 7

The results are displayed on the dashboard.

---

# 🔌 API

## Predict Case

### Endpoint

```text
POST /predict
```

### Request

Example:

```json
{
  "case_name": "Example Case",
  "features": {
    "evidence_strength": 8,
    "witness_count": 6,
    "prior_criminal_record": 1,
    "legal_representation": 2,
    "crime_severity": 4,
    "evidence_tampering": 0,
    "defendant_cooperation": 4,
    "jurisdiction_strictness": 4,
    "case_media_coverage": 1,
    "time_to_trial_months": 12
  }
}
```

### Response

The API returns information containing:

```json
{
  "success": true,
  "result": {
    "prediction": "Convicted",
    "confidence": 80,
    "probabilities": {
      "Acquitted": 20,
      "Convicted": 80
    }
  }
}
```

The complete project also returns explanation information such as feature importance, LIME-style results, SHAP-style values and tree-voting information.

---

# 🔄 Complete Execution Flow

```text
User
 │
 ▼
Web Interface
 │
 ▼
Enter 10 Case Features
 │
 ▼
JavaScript
 │
 ▼
POST /predict
 │
 ▼
Flask Backend
 │
 ▼
Pandas DataFrame
 │
 ▼
StandardScaler
 │
 ▼
Random Forest
 │
 ▼
200 Decision Trees
 │
 ├───────────────┐
 │               │
 ▼               ▼
Prediction     Probability
 │
 ▼
Explainability Layer
 │
 ├── LIME
 ├── SHAP-style
 ├── Feature Importance
 └── Tree Voting
 │
 ▼
Final Result
 │
 ▼
Frontend Dashboard
```

---

# 📊 Example Output

A typical result can contain:

```text
------------------------------------
        CASE PREDICTION
------------------------------------

Prediction:
CONVICTED

Confidence:
80%

Probabilities:

Acquitted     20%
Convicted     80%

------------------------------------
        EXPLANATION
------------------------------------

LIME:
Important factors for this case

SHAP-style:
Feature contribution analysis

Global Importance:
Most important features overall

Tree Votes:
Convicted: 160
Acquitted: 40
Total: 200
------------------------------------
```

---

# ⚠️ Limitations

This project has several important limitations.

### 1. Synthetic Dataset

The current model is trained using synthetically generated cases rather than a verified real-world legal dataset.

Therefore, its predictions should not be interpreted as real-world legal predictions.

### 2. Simplified Legal Features

Real legal cases involve many complex factors that cannot be completely represented using only ten numerical/categorical features.

### 3. Demonstration Model

The project is designed primarily as an academic and technical demonstration of machine learning and Explainable AI.

### 4. No Legal Authority

The prediction does not represent the decision of a court, lawyer, judge, or legal authority.

### 5. XAI Approximation

The SHAP component is implemented as a SHAP-style/feature-ablation explanation rather than a complete SHAP implementation.

---

# 🚀 Future Scope

The project can be extended in several ways.

## 1. Real Legal Dataset

Replace the synthetic dataset with a carefully curated and legally appropriate dataset of historical cases.

## 2. Advanced Machine Learning

Additional models could be compared:

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost
* Neural Networks

## 3. Better Explainability

The system could integrate full XAI libraries and compare multiple explanation techniques.

## 4. NLP Integration

Natural Language Processing could be added to analyze:

* Case descriptions
* Court judgments
* Legal documents
* Evidence descriptions

## 5. Document Upload

Users could upload a legal document and extract relevant features automatically.

## 6. Model Comparison

The application could compare several machine-learning algorithms and show which performs best.

## 7. Bias and Fairness Analysis

The system could include fairness metrics to identify potential bias in legal prediction systems.

## 8. Database Integration

A database could store simulated cases, predictions and explanation results.

## 9. Authentication

User accounts and role-based access could be added for a more complete application.

---

# 🎓 Academic Significance

This project demonstrates the integration of multiple concepts:

```text
Machine Learning
       +
Data Processing
       +
Web Development
       +
Explainable AI
       +
Data Visualization
       =
Explainable Legal Prediction System
```

It demonstrates an important principle in modern AI:

> A prediction should not only be generated; users should also be able to understand the factors behind that prediction.

---

# 📌 Disclaimer

This application is intended **only for educational and research purposes**.

It is a machine-learning demonstration using simulated/synthetic case data. It must not be used to make decisions about actual defendants, legal cases, sentencing, bail, guilt, innocence, or other legal matters.

The predictions generated by this system are not legal advice and do not represent the opinion or decision of any court or legal professional.

---

# 👨‍💻 Project

**Project Name:** Explainable AI for Legal Case Outcome Prediction

**Domain:** Artificial Intelligence / Machine Learning / Explainable AI

**Application Type:** Web-based Machine Learning Application

**Backend:** Python + Flask

**Machine Learning:** Random Forest

**Explainability:** LIME-style, SHAP-style, Feature Importance, Tree Voting

**Dataset:** Synthetic/Simulated Legal Case Data
