#pip install fastapi uvicorn
from fastapi import FastAPI
import pickle
from transformers import AutoModelForSequenceClassification
from transformers import pipeline
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from frames import *



app = FastAPI()

with open('my_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# pickle_in = open("classifier.pkl","rb")
# classifier = pickle.load(pickle_in)

@app.get("/")
def read_root():
    return {"message": "This is an application that predicts frmames for normative sentences"}

@app.post("/predict_frame")
def predict_frame(data: str):

    print(data)
    #inputs = tokenizer(data, return_tensors='pt')
    #inputs = {key: value.to(loaded_model.device) for key, value in inputs.items()}
    #outputs = loaded_model(**inputs)
    #predictions = torch.argmax(outputs.logits, dim=1).item()
    #print("Prediction:", prediction)

    # Create instances of each frame
    flint_format = create_empty_flint_format()
    act_frame = create_empty_act_frame()
    fact_frame = create_empty_fact_frame()
    duty_frame = create_empty_duty_frame()

    flint_format["acts"].append(act_frame)
    flint_format["facts"].append(fact_frame)
    flint_format["duties"].append(duty_frame)

    return {"sentence": data, "frames": flint_format}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")