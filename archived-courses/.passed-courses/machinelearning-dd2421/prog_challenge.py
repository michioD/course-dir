import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

TrainingData = pd.read_csv('TrainOnMe_orig.csv')
evaluation = pd.read_csv('EvaluateOnMe.csv')
evaluationGT = pd.read_csv('EvluationGT.csv')
# x = train

x = TrainingData.drop(columns=["species", "ancestral_code"])
# with open('blah.txt', 'w') as f:
#     for col in x.columns:
#         f.write(f"{col}\n")
y = TrainingData["species"]

XEval = evaluation.drop(columns=["ancestral_code"])
# TODO handle the Nan valus in the data
# def remove_nan_values(x)



categorical_columns = ['dance_style', 'symmetry_flag']
numerical_columns = [col for col in x.columns if col not in categorical_columns]
# print(numerical_columns)
categorical_transformer = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
preprocessor = ColumnTransformer(transformers=[('num', SimpleImputer(strategy='median'), numerical_columns), ('cat', categorical_transformer, categorical_columns)])



# random_forest = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=67)
random_forest = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=67)


model = Pipeline(steps=[('preprocessor', preprocessor),('classifier', random_forest)])

# x_train_split, x_test_split, y_train_split, y_test_split = train_test_split(x, y, test_size=0.3, shuffle=True)
# test_predictions = model.predict(x_test_split)
# accuracy = accuracy_score(y_test_split, test_predictions)
# print(accuracy)
accuracies = []
for i in range(1):
    x_TrainSplit, x_TestSplit, y_TrainSplit, y_TestSplit = train_test_split(x, y, test_size=0.3, shuffle=True)
    model.fit(x_TrainSplit, y_TrainSplit)
    TestPred = model.predict(x_TestSplit)
    accuracy = accuracy_score(y_TestSplit, TestPred)
    accuracies.append(accuracy)

average_accuracy = sum(accuracies) /len(accuracies)
std_accuracy = pd.Series(accuracies).std()
print("test accuracy:",average_accuracy)
model.fit(x,y)
predictions = model.predict(XEval)



with open('predictions.txt', 'w') as f:
    for label in predictions:
        f.write(f"{label}\n")
