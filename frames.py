def create_empty_flint_format() -> dict:
    flint_format = {
        "sentence":"",
        "acts": [],
        "facts": [],
        "duties": []
    }
    return flint_format

def create_empty_act_frame() -> dict:
    act_frame = {
        "id":"",
        "act": "",
        "actor": "",
        "action": "",
        "object": "",
        "recipient": "",
        # "preconditions": {
        #     "expression": "LITERAL",
        #     "operand": True
        # },
        "preconditions": [],
        "create": [],
        "terminate": [],
        "sources": [],
        # with validFrom, validTo, citation juriconnect and text
        "explanation": ""
    }
    return act_frame

def create_empty_fact_frame() -> dict:
    fact_frame = {
        "id":"",
        "fact": "",
        "function": [],
        "sources": [],  # with validFrom, validTo, citation juriconnect and text
        "explanation": ""
    }
    return fact_frame

def create_empty_duty_frame() -> dict:
    duty_frame = {
        "id":"",
        "duty": "",
        "duty holder": "",
        "claimant": "",
        "terminating act": [],
        "creating act": [],
        "enforcing act": "",
        "sources": [],
    }
    return duty_frame
