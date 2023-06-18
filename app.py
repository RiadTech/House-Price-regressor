from flask import Flask, request, jsonify
from flasgger import Swagger
import pickle

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def hello():
  return "Hello World"

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint that returns the predicted price of a house based on its features.
    ---
    parameters:
      - name: bath
        in: formData
        type: number
        required: true
      - name: bhk
        in: formData
        type: integer
        required: true
      - name: sqft
        in: formData
        type: integer
        required: true
    responses:
      200:
        description: The predicted price of the house.
    """
    # Load the machine learning model
    model = pickle.load(open('regression.pkl', "rb"))

    # Get the values from the form
    bath = float(request.form['bath'])
    bhk = int(request.form['bhk'])
    sqft = int(request.form['sqft'])

    # Make a prediction
    prediction = model.predict([[bath, bhk, sqft]])

    # Return the prediction as JSON
    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()