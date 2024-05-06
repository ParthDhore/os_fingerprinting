import os
import shutil
import time
import pickle
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
minrows=10000
def get_db():
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            database='osfingerprint',
            user='root',
            password='1234'
        )

        # Define your SQL query
        query = "SELECT * FROM fingerprints"  # Replace 'your_table_name' with your actual table name

        # Execute the query and fetch the results
        df = pd.read_sql(query, connection)

        # Close the connection
        connection.close()
        return df

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
    
def backup_model(model_file, backup_dir, performance):
    """Backup the existing model file."""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"model_backup_{timestamp}.pkl")
    shutil.copy(model_file, backup_file)
    print(f"Model backup created: {backup_file}")

    file_path=f"model_backups\\performance_report{timestamp}.txt"
    with open(file_path, 'w') as file:
        file.write(str(performance))

def replace_model(new_model_file, model_file, backup_dir, performance):
    """Replace the existing model file with the new one."""
    # Backup the current model file first
    backup_model(model_file, backup_dir, performance)
    # Replace the model file
    while True:
        try:
            shutil.move('model_update\\random_forest_model2.pkl', 'models\\random_forest_model.pkl')
            # os.remove('model_update\\random_forest_model.pkl')
            print(f"Model replaced with: {new_model_file}")
            break
        except PermissionError:
            print("Waiting for file lock to be released...")
            time.sleep(1)

def train_model():
    per={}
    df=get_db()
    df.to_csv('utils\\test.csv', index=False)
    # if df.shape[0] < minrows:
    #     return
    df.drop(['id'], axis=1, inplace=True)
    lalen=len(df['os'].unique())
    valcnt=df['os'].value_counts().to_dict()
    
    X=df.drop(['os'], axis=1)
    y=df['os']
    X_train, X_test, y_train, y_test = train_test_split( X, y, random_state=104, test_size=0.15, shuffle=True)
    
    model=RandomForestClassifier(n_estimators=30)
    model=model.fit(X_train,y_train)
    pred=model.predict(X_test)
    acc=accuracy_score(y_test,pred)
    pres=precision_score(y_test,pred,average='micro')
    rec=recall_score(y_test,pred,average='micro')
    f1=f1_score(y_test,pred,average='micro')
    per['lable_len']=lalen
    per['value_counts']=valcnt
    per['accuracy']=acc
    per['presicion(micro-averaged)']=pres
    per['recall(micro-averaged)']=rec
    per['f1score(micro-averaged)']=f1


    with open('model_update\\random_forest_model2.pkl', 'wb') as f:
        pickle.dump(model, f)

    replace_model('model_update\\random_forest_model2.pkl', 'models\\random_forest_model.pkl', 'model_backups', per)


train_model()
