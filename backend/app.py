from flask import Flask
from flask import request
from flask import jsonify

from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
app = Flask(__name__)
CORS(app)

IMG_SIZE = 128
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
print("Loading Model...")

model = tf.keras.models.load_model("models/deepfake_model.h5")
print("Model Loaded Successfully")

def predict_image(path):
    img = cv2.imread(path)
    if img is None:
        raise Exception("Cannot Read Image")

    img = cv2.resize(img,(IMG_SIZE,IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img,axis=0)
    pred = model.predict(img,verbose=0)[0][0]
    confidence = float(max(pred,1-pred) * 100)
    label = "REAL" if pred > 0.5 else "FAKE"
    return label,round(confidence,2)

@app.route("/")
def home():\
    return jsonify({
        "message":"Backend Running"
    })
    
@app.route("/predict",methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error":"No Image Uploaded"}),400
        file = request.files["image"]
        if file.filename=="":
            return jsonify({"error":"No File Selected"}),400
        filepath = os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
        file.save(filepath)
        print("Saved Image:",filepath)
        label,confidence = predict_image(filepath)
        print("Prediction:",label,", Confidence:",confidence)
        return jsonify({"prediction":str(label),"confidence":float(confidence)})
    
    except Exception as e:
        print("ERROR:",str(e))
        return jsonify({"error":str(e)}),500


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)