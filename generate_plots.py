import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load Data
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Ensure Output Dir
import os
os.makedirs("plots", exist_ok=True)

# 1. Scatter plot of Flight Number vs. Launch Site (Slide 18)
plt.figure(figsize=(10,6))
sns.scatterplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df)
plt.title("Flight Number vs. Launch Site")
plt.savefig("plots/flight_vs_launchsite.png", bbox_inches='tight')
plt.close()

# 2. Scatter plot of Payload vs. Launch Site (Slide 19)
plt.figure(figsize=(10,6))
sns.scatterplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df)
plt.title("Payload vs. Launch Site")
plt.savefig("plots/payload_vs_launchsite.png", bbox_inches='tight')
plt.close()

# 3. Bar chart for success rate of each orbit type (Slide 20)
plt.figure(figsize=(10,6))
success_rate = df.groupby('Orbit')['Class'].mean().reset_index()
sns.barplot(x="Orbit", y="Class", data=success_rate)
plt.title("Success Rate vs. Orbit Type")
plt.savefig("plots/success_vs_orbit.png", bbox_inches='tight')
plt.close()

# 4. Scatter point of Flight number vs. Orbit type (Slide 21)
plt.figure(figsize=(10,6))
sns.scatterplot(y="Orbit", x="FlightNumber", hue="Class", data=df)
plt.title("Flight Number vs. Orbit Type")
plt.savefig("plots/flight_vs_orbit.png", bbox_inches='tight')
plt.close()

# 5. Scatter point of payload vs. orbit type (Slide 22)
plt.figure(figsize=(10,6))
sns.scatterplot(y="Orbit", x="PayloadMass", hue="Class", data=df)
plt.title("Payload vs. Orbit Type")
plt.savefig("plots/payload_vs_orbit.png", bbox_inches='tight')
plt.close()

# 6. Line chart of yearly average success rate (Slide 23)
def Extract_year(date):
    return date.split("-")[0]
df['Year'] = df['Date'].apply(Extract_year)
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
plt.figure(figsize=(10,6))
sns.lineplot(x="Year", y="Class", data=yearly_success)
plt.title("Launch Success Yearly Trend")
plt.savefig("plots/yearly_success_trend.png", bbox_inches='tight')
plt.close()

print("EDA plots generated.")

# ML Data
X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')
Y = df['Class'].to_numpy()

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn import preprocessing

transform = preprocessing.StandardScaler()
X_scaled = transform.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# Models
logreg_cv = GridSearchCV(LogisticRegression(), {'C':[0.01,0.1,1], 'penalty':['l2'], 'solver':['lbfgs']}, cv=10).fit(X_train, Y_train)
svm_cv = GridSearchCV(SVC(), {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'), 'C': np.logspace(-3, 3, 5), 'gamma':np.logspace(-3, 3, 5)}, cv=10).fit(X_train, Y_train)
tree_cv = GridSearchCV(DecisionTreeClassifier(), {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random'], 'max_depth': [2*n for n in range(1,10)], 'max_features': ['sqrt'], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}, cv=10).fit(X_train, Y_train)
knn_cv = GridSearchCV(KNeighborsClassifier(), {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1,2]}, cv=10).fit(X_train, Y_train)

accuracies = {
    'Logistic Regression': logreg_cv.score(X_test, Y_test),
    'SVM': svm_cv.score(X_test, Y_test),
    'Decision Tree': tree_cv.score(X_test, Y_test),
    'KNN': knn_cv.score(X_test, Y_test)
}

# 7. Classification Accuracy (Slide 43)
plt.figure(figsize=(10,6))
sns.barplot(x=list(accuracies.keys()), y=list(accuracies.values()))
plt.title("Classification Accuracy")
plt.ylabel("Accuracy")
plt.savefig("plots/classification_accuracy.png", bbox_inches='tight')
plt.close()

# 8. Confusion Matrix (Slide 44)
def plot_confusion_matrix(y,y_predict):
    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])

plt.figure(figsize=(8,6))
plot_confusion_matrix(Y_test, tree_cv.predict(X_test))
plt.savefig("plots/confusion_matrix.png", bbox_inches='tight')
plt.close()

print("ML plots generated.")
