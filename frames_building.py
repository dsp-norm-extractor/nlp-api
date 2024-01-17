# frame_processing.py

import torch
from frames import *

def process_sentence(sentence, tokenizer, loaded_model, use_model, demo_pred):

    # predict label of sentence 
    inputs = tokenizer(sentence, return_tensors='pt')
    inputs = {key: value.to(loaded_model.device) for key, value in inputs.items()}
    outputs = loaded_model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1).item()

    print("Sentence:", sentence)
    print("Prediction:", predictions)

    #if pred = 0 then its a Fact
    #if pred = 1 then its an Act
    #if pred = 2 then its a Duty

    flint_format = create_empty_flint_format()

    if(use_model == 1):
        if (predictions == 0):
            fact_frame = create_empty_fact_frame()
            flint_format["facts"].append(fact_frame)
        
        if(predictions == 1):
            act_frame = create_empty_act_frame()
            flint_format["acts"].append(act_frame)
        if(predictions == 2):
            duty_frame = create_empty_duty_frame()
            flint_format["duties"].append(duty_frame)
    else: # DEMO
        if(demo_pred == "F"):
            fact_frame = create_empty_fact_frame()
            #fact_frame["fact"] = None
            flint_format["facts"].append(fact_frame)
        if(demo_pred == "A"):
            act_frame = create_empty_act_frame()
            flint_format["acts"].append(act_frame)
        if(demo_pred == "D"):
            duty_frame = create_empty_duty_frame()
            flint_format["duties"].append(duty_frame)
        if(demo_pred == "AF"):
            act_frame = create_empty_act_frame()
            flint_format["acts"].append(act_frame)
            fact_frame = create_empty_fact_frame()
            flint_format["facts"].append(fact_frame)
        if(demo_pred == "AD"):
            act_frame = create_empty_act_frame()
            flint_format["acts"].append(act_frame)
            duty_frame = create_empty_duty_frame()
            flint_format["duties"].append(duty_frame)

    return {"sentence": sentence, "frames": flint_format}
