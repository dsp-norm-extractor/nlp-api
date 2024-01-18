# frame_processing.py

import torch
from frames import *
import uuid

def process_sentence(sentence, tokenizer, loaded_model,act_tokenizer,act_model, use_model, demo_pred):

    # predict label of sentence 
    inputs = tokenizer(sentence, return_tensors='pt')
    inputs = {key: value.to(loaded_model.device) for key, value in inputs.items()}
    outputs = loaded_model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1).item()

    print("Sentence:", sentence)
    print("Prediction:", predictions)


    flint_format = create_empty_flint_format()

    #build act - fact - duty frame according to sentece prediction
    if(use_model == 1):
        if (predictions == 2):
            fact_frame = create_empty_fact_frame()
            flint_format["facts"].append(fact_frame)
        if(predictions == 0):
            #create act frame
            act_frame = create_empty_act_frame()
            flint_format["acts"].append(act_frame)
            act_frame["id"] = uuid.uuid4() #build frame id

            # predict sub-labels for acts
            tokens = act_tokenizer.tokenize(act_tokenizer.decode(act_tokenizer.encode(sentence)))
            inputs = act_tokenizer.encode(sentence, return_tensors="pt").to(act_model.device)
            outputs = act_model(inputs)[0]
            predictions_act = torch.argmax(outputs, dim=2) 
            cls_index = tokens.index('[CLS]')
            sep_index = tokens.index('[SEP]')
            predictions_act[0,cls_index] = -100
            predictions_act[0,sep_index] = -100

            precondition_buffer = ""
            creating_fact_buffer = ""
            #build act frame according to predictions
            for i, element in enumerate(predictions_act.flatten()):
                #print(element.item())
                
                if(element.item() == 1):
                    act_frame["action"] += tokens[i] + " "
                    act_frame["act"] += tokens[i] + " "
                if(element.item() == 2):
                    act_frame["actor"] += tokens[i] + " "
                if(element.item() == 3):
                    act_frame["object"] += tokens[i] + " "
                if(element.item() == 4):
                    act_frame["recipient"] += tokens[i] + " "
                if(element.item() == 5):
                    precondition_buffer += tokens[i] + " "
                if(element.item() == 6):
                    creating_fact_buffer += tokens[i] + " "            
                
            
            if(precondition_buffer != ""):
                fact_frame = create_empty_fact_frame()
                new_id = uuid.uuid4()
                fact_frame["id"] = new_id
                fact_frame["fact"] = precondition_buffer
                flint_format["facts"].append(fact_frame)
                act_frame["preconditions"].append(new_id)   
            
            if(creating_fact_buffer != ""):
                fact_frame = create_empty_fact_frame()
                new_id = uuid.uuid4()
                fact_frame["id"] = new_id
                fact_frame["fact"] = creating_fact_buffer
                flint_format["facts"].append(fact_frame)
                act_frame["create"].append(new_id)   

            # print(inputs)
            #print("tokens",tokens[3])
            # print("pred",predictions_act)


        if(predictions == 1):
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
