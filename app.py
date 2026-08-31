"""
Explainable AI for Legal Case Outcome Prediction
================================================
A 3rd Year AIML Engineering Project demonstrating:
- Random Forest Classification
- LIME Explanations
- SHAP Values
- Feature Importance Analysis
- Interactive Case Analysis
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

from models.legal_model import LegalPredictionModel
from data.case_database import SAMPLE_CASES, FEATURE_DESCRIPTIONS

app = Flask(__name__)

# Initialize and train the model on startup
model = LegalPredictionModel()
model.train()

@app.route('/')
def index():
    return render_template('index.html',
                           sample_cases=SAMPLE_CASES,
                           feature_descriptions=FEATURE_DESCRIPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data.get('features', {})
        case_name = data.get('case_name', 'Custom Case')

        # Convert to DataFrame
        input_df = pd.DataFrame([features])

        # Get prediction and explanations
        result = model.predict_with_explanation(input_df, case_name)

        return jsonify({'success': True, 'result': result})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/sample_case/<int:case_id>')
def sample_case(case_id):
    if 0 <= case_id < len(SAMPLE_CASES):
        return jsonify({'success': True, 'case': SAMPLE_CASES[case_id]})
    return jsonify({'success': False, 'error': 'Case not found'})

@app.route('/model_info')
def model_info():
    info = model.get_model_info()
    return jsonify(info)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  XAI Legal Case Outcome Predictor")
    print("  AIML Engineering Project - 3rd Year")
    print("="*60)
    print("  Open your browser at: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(debug=True)
