import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load Data
train = pd.read_csv('TrainOnMe_orig.csv')

X = train.drop(columns=['species', 'ancestral_code'])
y = train['species']

# 2. Perform the Split (80% Training, 20% Validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.4, random_state=42)

# 3. Setup Pipeline
cat_cols = ['dance_style', 'symmetry_flag']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), cat_cols)
    ], remainder='passthrough'
)

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', HistGradientBoostingClassifier(
        random_state=42, 
        learning_rate=0.05, 
        max_iter=100, 
        max_leaf_nodes=50
    ))
])

# 4. Train the model ONLY on the 80% split
model.fit(X_train, y_train)

# 5. Predict and compare scores
train_preds = model.predict(X_train)
val_preds = model.predict(X_val)

print(f"Training Accuracy:   {accuracy_score(y_train, train_preds) * 100:.2f}%")
print(f"Validation Accuracy: {accuracy_score(y_val, val_preds) * 100:.2f}%")
