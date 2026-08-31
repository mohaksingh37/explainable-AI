"""
Legal Prediction Model
======================
Random Forest model with LIME and SHAP-style feature importance explanations
for legal case outcome prediction.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json


# ─── Feature definitions ────────────────────────────────────────────────────
FEATURES = [
    'evidence_strength',        # 0-10
    'witness_count',            # 0-10
    'prior_criminal_record',    # 0/1
    'legal_representation',     # 0=None, 1=Public Defender, 2=Private Attorney
    'crime_severity',           # 1-5
    'evidence_tampering',       # 0/1
    'defendant_cooperation',    # 0-10
    'jurisdiction_strictness',  # 1-5
    'case_media_coverage',      # 0/1
    'time_to_trial_months',     # months
]

FEATURE_RANGES = {
    'evidence_strength':       (0, 10),
    'witness_count':           (0, 10),
    'prior_criminal_record':   (0, 1),
    'legal_representation':    (0, 2),
    'crime_severity':          (1, 5),
    'evidence_tampering':      (0, 1),
    'defendant_cooperation':   (0, 10),
    'jurisdiction_strictness': (1, 5),
    'case_media_coverage':     (0, 1),
    'time_to_trial_months':    (1, 36),
}

OUTCOMES = ['Acquitted', 'Convicted']


class LegalPredictionModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_split=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.trained = False
        self.feature_importances_ = None
        self.accuracy = None
        self.X_train = None

    # ─── Synthetic dataset ───────────────────────────────────────────────────
    def _generate_dataset(self, n_samples=1000):
        np.random.seed(42)

        data = []
        for _ in range(n_samples):
            ev   = np.random.uniform(0, 10)
            wc   = np.random.randint(0, 11)
            pcr  = np.random.binomial(1, 0.35)
            lr   = np.random.choice([0, 1, 2], p=[0.1, 0.4, 0.5])
            cs   = np.random.randint(1, 6)
            et   = np.random.binomial(1, 0.15)
            dc   = np.random.uniform(0, 10)
            js   = np.random.randint(1, 6)
            mc   = np.random.binomial(1, 0.25)
            ttm  = np.random.randint(1, 37)

            # Decision logic (domain-knowledge driven)
            score = 0
            score += ev * 1.5           # Strong evidence → conviction
            score += wc * 0.8
            score -= dc * 0.7           # Cooperation → acquittal
            score += pcr * 3.0
            score += cs * 1.2
            score += et * 4.0
            score -= lr * 1.5           # Better lawyer → acquittal
            score += js * 0.5
            score += mc * 0.3
            score += ttm * 0.05

            # Probabilistic outcome
            prob = 1 / (1 + np.exp(-(score - 18) / 4))
            label = int(np.random.random() < prob)

            data.append([ev, wc, pcr, lr, cs, et, dc, js, mc, ttm, label])

        df = pd.DataFrame(data, columns=FEATURES + ['outcome'])
        return df

    # ─── Training ────────────────────────────────────────────────────────────
    def train(self):
        df = self._generate_dataset()
        X = df[FEATURES]
        y = df['outcome']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.X_train = X_train

        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s  = self.scaler.transform(X_test)

        self.model.fit(X_train_s, y_train)

        preds = self.model.predict(X_test_s)
        self.accuracy = accuracy_score(y_test, preds)
        self.feature_importances_ = dict(
            zip(FEATURES, self.model.feature_importances_)
        )
        self.trained = True
        print(f"[Model] Trained successfully | Accuracy: {self.accuracy:.2%}")

    # ─── LIME-style local explanation ────────────────────────────────────────
    def _lime_explanation(self, instance_df, n_samples=500, n_top=6):
        """
        Lightweight LIME: perturb features around the instance,
        fit a linear model, return coefficients as local importances.
        """
        from sklearn.linear_model import Ridge

        instance = instance_df.values[0]
        rng = np.random.RandomState(0)

        # Perturb in scaled space
        instance_scaled = self.scaler.transform(instance_df)[0]
        perturbations = rng.normal(0, 0.15, (n_samples, len(FEATURES)))
        perturbed = instance_scaled + perturbations

        # Weights: exponential kernel
        distances = np.sqrt((perturbations**2).sum(axis=1))
        kernel_width = 0.75
        weights = np.exp(-(distances**2) / (2 * kernel_width**2))

        # Predict on perturbed samples
        probs = self.model.predict_proba(perturbed)[:, 1]

        # Fit linear surrogate
        surrogate = Ridge(alpha=1.0)
        surrogate.fit(perturbed, probs, sample_weight=weights)

        coefs = dict(zip(FEATURES, surrogate.coef_))

        # Top features sorted by absolute coefficient
        top = sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)[:n_top]
        return [{'feature': k, 'coefficient': round(float(v), 4)} for k, v in top]

    # ─── SHAP-style permutation importance ───────────────────────────────────
    def _shap_explanation(self, instance_df):
        """
        Approximated SHAP using feature ablation / marginal contributions.
        """
        instance_scaled = self.scaler.transform(instance_df)
        baseline_prob = self.model.predict_proba(instance_scaled)[0][1]

        # Mean of training set as reference
        train_mean = self.scaler.transform(self.X_train).mean(axis=0)

        shap_values = {}
        for i, feat in enumerate(FEATURES):
            ablated = instance_scaled.copy()
            ablated[0, i] = train_mean[i]   # replace with baseline
            ablated_prob = self.model.predict_proba(ablated)[0][1]
            shap_values[feat] = round(float(baseline_prob - ablated_prob), 4)

        return shap_values

    # ─── Decision path ───────────────────────────────────────────────────────
    def _decision_path_summary(self, instance_df):
        """Return top decision trees' voting summary."""
        instance_scaled = self.scaler.transform(instance_df)
        tree_preds = [t.predict(instance_scaled)[0]
                      for t in self.model.estimators_]
        votes_conv = sum(tree_preds)
        votes_acqu = len(tree_preds) - votes_conv
        return {
            'total_trees': len(tree_preds),
            'votes_convicted': int(votes_conv),
            'votes_acquitted': int(votes_acqu),
        }

    # ─── Main prediction + explanation ───────────────────────────────────────
    def predict_with_explanation(self, input_df, case_name='Case'):
        if not self.trained:
            raise RuntimeError("Model not trained yet.")

        input_scaled = self.scaler.transform(input_df)
        proba = self.model.predict_proba(input_scaled)[0]
        pred_idx = int(np.argmax(proba))
        prediction = OUTCOMES[pred_idx]
        confidence = float(proba[pred_idx])

        # Global feature importances (sorted)
        global_imp = sorted(
            self.feature_importances_.items(),
            key=lambda x: x[1], reverse=True
        )

        # Local explanations
        lime_exp  = self._lime_explanation(input_df)
        shap_vals = self._shap_explanation(input_df)
        vote_info = self._decision_path_summary(input_df)

        # Natural language explanation
        top_lime  = lime_exp[0]
        top_feat  = top_lime['feature'].replace('_', ' ')
        direction = "increasing" if top_lime['coefficient'] > 0 else "decreasing"
        nl_explanation = (
            f"The model predicts <strong>{prediction}</strong> with "
            f"<strong>{confidence:.1%} confidence</strong>. "
            f"The most influential factor is <em>{top_feat}</em>, which is "
            f"{direction} the likelihood of conviction. "
            f"{vote_info['votes_convicted']} out of "
            f"{vote_info['total_trees']} decision trees voted for conviction."
        )

        return {
            'case_name': case_name,
            'prediction': prediction,
            'confidence': round(confidence * 100, 2),
            'probabilities': {
                'Acquitted': round(float(proba[0]) * 100, 2),
                'Convicted':  round(float(proba[1]) * 100, 2),
            },
            'global_feature_importance': [
                {'feature': k, 'importance': round(float(v), 4)}
                for k, v in global_imp
            ],
            'lime_explanation': lime_exp,
            'shap_values': [
                {'feature': k, 'value': v}
                for k, v in sorted(shap_vals.items(),
                                   key=lambda x: abs(x[1]), reverse=True)
            ],
            'vote_info': vote_info,
            'nl_explanation': nl_explanation,
            'input_features': input_df.iloc[0].to_dict(),
        }

    def get_model_info(self):
        return {
            'model_type': 'Random Forest Classifier',
            'n_estimators': self.model.n_estimators,
            'max_depth': self.model.max_depth,
            'accuracy': round(self.accuracy * 100, 2) if self.accuracy else None,
            'features': FEATURES,
            'outcomes': OUTCOMES,
            'feature_ranges': FEATURE_RANGES,
        }
