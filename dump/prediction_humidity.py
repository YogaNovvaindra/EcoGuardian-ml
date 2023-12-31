from flask import Flask, request, jsonify
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Inisialisasi Firebase
cred = credentials.Certificate('C:/Users/songc/Downloads/version1/knupolije1-firebase-adminsdk-yschq-279d47284b.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://knupolije1-default-rtdb.firebaseio.com'
})

def add_data_to_aidata_in_firebase(y1_pred_plus, y2_pred_plus):
    aidata_ref = db.reference('/aidata')
    
    try:
        current_data = {}
        current_data['y1_pred_plus'] = y1_pred_plus.tolist()
        current_data['y2_pred_plus'] = y2_pred_plus.tolist()
        
        aidata_ref.update(current_data)
        print('Data added to /aidata in Firebase.')
        
    except Exception as e:
        print('Error adding data to /aidata:', e)

@app.route('/postjson', methods=['POST'])
def post_json():
    try:
        data = request.json  

        x_values = data.get('x', [])
        hum1_values = data.get('hum1', [])
        hum2_values = data.get('hum2', [])
        
        if x_values and hum1_values and hum2_values:
           
            X = np.array(x_values).reshape(-1, 1)
            y1 = np.array(hum1_values)
            y2 = np.array(hum2_values)

            # Gaussian Process Regression 
            kernel = RBF()  # Radial basis function (RBF)
            gp_model = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

   
            tree_model = DecisionTreeRegressor(max_depth=5)

         
            ensemble_model = VotingRegressor(estimators=[('gp', gp_model), ('tree', tree_model)])

 
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ensemble_model.fit(X, y1)  

            y1_pred = ensemble_model.predict(X)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ensemble_model.fit(X, y2)  

            y2_pred = ensemble_model.predict(X)

            last_x_value = x_values[-1]
            last_x_plus = last_x_value + 15

            y1_pred_plus = ensemble_model.predict([[last_x_plus]])
            y2_pred_plus = ensemble_model.predict([[last_x_plus]])

            add_data_to_aidata_in_firebase(y1_pred_plus, y2_pred_plus)

            result = {
                "y1_pred": y1_pred.tolist(),
                "y2_pred": y2_pred.tolist()
            }
            return jsonify(result)

        else:
            return jsonify({"error": "Invalid JSON data"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)