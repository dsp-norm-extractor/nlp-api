# pip install fastapi uvicorn
from fastapi import FastAPI, HTTPException, Request
import pickle
from transformers import AutoModelForSequenceClassification
from transformers import pipeline
import torch
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    DistilBertForTokenClassification,
)
from frames import *
from typing import List
from frames_building import *
import random
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from db_helper import *
from db_format import *
from bson import json_util
from bson import ObjectId
from retraining_helper import *

mongo_client = None

app = FastAPI()

# import models
loaded_model = AutoModelForSequenceClassification.from_pretrained("my_model_v2")
loaded_tokenizer = AutoTokenizer.from_pretrained("my_model_v2")

act_model = DistilBertForTokenClassification.from_pretrained("act_model")
act_tokenizer = DistilBertTokenizer.from_pretrained("act_model")

duty_model = DistilBertForTokenClassification.from_pretrained("duty_model")
duty_tokenizer = DistilBertTokenizer.from_pretrained("duty_model")


# import pickle files code

# with open('sent_mod.pkl', 'rb') as file:
#     #loaded_model = torch.load(file,map_location=torch.device('cpu'))
#     print(torch.__version__)

# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# pickle_in = open("classifier.pkl","rb")
# classifier = pickle.load(pickle_in)


@app.get("/")
def read_root():
    return {
        "message": "This is an application that predicts frmames for normative sentences"
    }


@app.post("/predict_frame")
async def predict_frame(data: List[str]):
    result = []
    labels = ["A", "F", "D", "AF", "AD"]

    for sentence in data:
        random_index = random.randint(0, len(labels) - 1)
        processed_data = process_sentence(
            sentence,
            loaded_tokenizer,
            loaded_model,
            act_tokenizer,
            act_model,
            duty_tokenizer,
            duty_model,
            1,
            labels[random_index],
        )
        result.append(processed_data)

    return result


# @app.get("/save_test_frame")
# async def save_to_db():

#     act_frame = create_empty_act_frame()
#     fact_frame = create_empty_fact_frame()
#     duty_frame = create_empty_duty_frame()

#     flint_format = create_empty_flint_format()
#     flint_format['acts'].append(act_frame)
#     flint_format['facts'].append(fact_frame)
#     flint_format['duties'].append(duty_frame)
#     insert_document(mongo_client,"normative_games","frames",flint_format)
#     return("saved")


@app.get("/save_test_frame")
async def save_to_db():
    db_format = create_empty_db_format()

    db_format["game"] = "monopoly"

    act_frame = create_empty_act_frame()
    fact_frame = create_empty_fact_frame()
    duty_frame = create_empty_duty_frame()

    flint_format = create_empty_flint_format()
    flint_format["acts"].append(act_frame)
    flint_format["facts"].append(fact_frame)
    flint_format["duties"].append(duty_frame)

    flint_format["sentence"] = "example"

    db_format["sentences"].append(flint_format)
    insert_document(mongo_client, "normative_games", "frames", db_format)
    return "saved"


@app.post("/save_data")
async def save_data(data: List[dict]):
    for game_data in data:
        game_name = game_data.get("game")
        details = game_data.get("details", [])

        db_format = create_empty_db_format()

        db_format["game"] = game_name
        db_format["for_training"] = 0

        for detail in details:
            sentence = detail.get("sentence")
            frames = detail.get("frames", {})

            # Extract relevant information from frames dictionary
            acts = frames.get("acts", [])
            facts = frames.get("facts", [])
            duties = frames.get("duties", [])

            # Process the extracted information as needed
            # Add your custom logic here based on the extracted data

            print(f"Sentence: {sentence}")
            print(f"Acts: {acts}")
            print(f"Facts: {facts}")
            print(f"Duties: {duties}")
            print("\n")

            act_frame = create_empty_act_frame()
            fact_frame = create_empty_fact_frame()
            duty_frame = create_empty_duty_frame()

            flint_format = create_empty_flint_format()
            flint_format["acts"] = acts
            flint_format["facts"] = facts
            flint_format["duties"] = duties

            flint_format["sentence"] = sentence

            db_format["details"].append(flint_format)

        insert_document(mongo_client, "normative_games", "frames", db_format)

    return data


@app.get("/get_frames")
async def get_frames():
    data = get_data(mongo_client, "normative_games", "frames")

    documents = [dict(document, _id=str(document["_id"])) for document in data]

    return {"data": documents}


@app.get("/retrain_model")
async def retrain_model():
    data = get_data(mongo_client,"normative_games","frames")
    
    do_model_retraining(data)

    return {"data": "model is retrained with accuracy x"}  


@app.get("/get_game_details")
async def get_game_details(game_name: str):
    try:
        data = get_data(
            mongo_client,
            "normative_games",
            "frames",
            {"game": {"$regex": game_name, "$options": "i"}},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Convert cursor to list and then check if it's empty
    documents = list(data)
    if not documents:  # This checks for both None and empty list
        raise HTTPException(status_code=404, detail=f"Game '{game_name}' not found")

    documents = [dict(document, _id=str(document["_id"])) for document in documents]

    return {"data": documents}




    


if __name__ == "__main__":
    import uvicorn

    mongo_client = connect_to_mongo()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
