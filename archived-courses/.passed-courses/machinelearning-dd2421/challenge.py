import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, QuantileTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression

# ===========================
# 1. Load data
# ===========================
df = pd.read_csv("TrainOnMe_orig.csv")

# ===========================
# 2. Features & target
# ===========================
X = df.drop(columns=["species", "ancestral_code"])
y = df["species"]

# Make sure categorical columns are strings
X["symmetry_flag"] = X["symmetry_flag"].astype(str)
X["dance_style"] = X["dance_style"].astype(str)

# ===========================
# 3. Train/test split (70/30 stratified)
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# ===========================
# 4. Column groups
# ===========================
categorical_cols = ["dance_style", "symmetry_flag"]
numeric_cols = [col for col in X.columns if col not in categorical_cols]

# ===========================
# 5. Preprocessing (Quantile + Scale = huge boost on this data)
# ===========================
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("quantile", QuantileTransformer(n_quantiles=300, output_distribution="normal", random_state=42)),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_cols),
    ("cat", categorical_pipeline, categorical_cols)
])

# ===========================
# 6. Strong tuned models
# ===========================
models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=500, max_features=0.7, min_samples_leaf=2,
        random_state=42, n_jobs=-1
    ),
    "HistGradientBoosting": HistGradientBoostingClassifier(
        learning_rate=0.05, max_iter=500, max_leaf_nodes=64,
        min_samples_leaf=5, l2_regularization=1.0, early_stopping=True,
        validation_fraction=0.1, random_state=42, max_bins=255
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=400, learning_rate=0.03, max_depth=5,
        min_samples_leaf=2, subsample=0.9, max_features=0.8, random_state=42
    ),
    "Logistic Regression": LogisticRegression(
        max_iter=5000, C=0.1, solver='saga', penalty='elasticnet',
        l1_ratio=0.5, random_state=42
    )
}

# ===========================
# 7. Evaluate individual models
# ===========================
results = {}
print("=== Individual Models ===")
for name, model in models.items():
    pipe = Pipeline([("preprocessor", preprocessor), ("clf", model)])
    pipe.fit(X_train, y_train)
    acc = accuracy_score(y_test, pipe.predict(X_test))
    results[name] = acc
    print(f"{name:25} → {acc*100:6.2f}%")

# ===========================
# 8. Stacking Ensemble (the winner)
# ===========================
print("\n=== Training Stacking Ensemble ===")

estimators = [
    ('gb',  models["Gradient Boosting"]),
    ('hgb', models["HistGradientBoosting"]),
    ('rf',  models["Random Forest"])
]

stack = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(max_iter=2000, C=1.0, random_state=42),
    cv=5,
    n_jobs=-1,
    passthrough=True
)

stack_pipe = Pipeline([("preprocessor", preprocessor), ("stack", stack)])
stack_pipe.fit(X_train, y_train)
stack_acc = accuracy_score(y_test, stack_pipe.predict(X_test))
print(f"Stacking Ensemble      → {stack_acc*100:6.2f}%")

# ===========================
# 9. Summary
# ===========================
best_single = max(results, key=results.get)
print("\n" + "="*65)
print(f"BEST SINGLE MODEL     : {best_single} @ {results[best_single]*100:.2f}%")
print(f"STACKING ENSEMBLE     : {stack_acc*100:.2f}%   ← usually the top performer")
print("="*65)

# Save the best model for the real test set
import joblib
joblib.dump(stack_pipe, "best_model_pipeline.pkl")
print("\nBest pipeline saved → best_model_pipeline.pkl")
