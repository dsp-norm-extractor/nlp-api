#pip install fastapi uvicorn
from fastapi import FastAPI, HTTPException, Request
import pickle
from transformers import AutoModelForSequenceClassification
from transformers import pipeline
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from frames import *
from typing import List
from frames_building import *
import random



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
async def predict_frame(data: List[str]):

    result = []
    labels = ["A","F","D","AF","AD"]

    for sentence in data:
        random_index = random.randint(0, len(labels) - 1)
        processed_data = process_sentence(sentence, tokenizer, loaded_model, 0, labels[random_index])
        result.append(processed_data)



    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")