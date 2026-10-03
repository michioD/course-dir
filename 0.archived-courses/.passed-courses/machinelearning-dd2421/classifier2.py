import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

train_df = pd.read_csv('TrainOnMe_orig.csv')
eval_df = pd.read_csv('EvaluateOnMe.csv')
x = train_df.drop(columns=['species', 'ancestral_code'])
y = train_df['species']
x_eval = eval_df.drop(columns=['ancestral_code'])

categorical_cols = ['dance_style', 'symmetry_flag'] #cols with categorical data
numerical_cols = [col for col in x.columns if col not in categorical_cols] #this makes the columns that are not categorical be treated as numerical for the pipeline



cat_transformer = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
# isnert the median in slots with NaN value 
preprocessor = ColumnTransformer(transformers=[('num', SimpleImputer(strategy='median'), numerical_cols), ('cat', cat_transformer, categorical_cols)])
random_forest = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
pipeline = Pipeline(steps=[('preprocessor', preprocessor),('classifier', random_forest)])





accuracies = []
for i in range(50):
    x_train_split, x_test_split, y_train_split, y_test_split = train_test_split(x, y, test_size=0.3,shuffle=True)
    pipeline.fit(x_train_split, y_train_split)
    test_predictions = pipeline.predict(x_test_split)
    accuracy = accuracy_score(y_test_split, test_predictions)
    accuracies.append(accuracy)

average_accuracy = sum(accuracies)/len(accuracies)
std_accuracy = pd.Series(accuracies).std()
print("test accuracy:", average_accuracy)


pipeline.fit(x, y) # using all the training data
final_predictions = pipeline.predict(x_eval) # prediciton for evaluation dataset
output_file = 'predictions.txt'
with open(output_file, 'w') as f:
    for label in final_predictions:
        f.write(f"{label}\n")
