def create_empty_flint_format() -> dict:
    flint_format = {
        "acts": [],
        "facts": [],
        "duties": []
    }
    return flint_format

def create_empty_act_frame() -> dict:
    act_frame = {
        "act": "",
        "actor": "",
        "action": "",
        "object": "",
        "recipient": "",
        "preconditions": {
            "expression": "LITERAL",
            "operand": True
        },
        "create": [],
        "terminate": [],
        "sources": [],
        # with validFrom, validTo, citation juriconnect and text
        "explanation": ""
    }
    return act_frame

def create_empty_fact_frame() -> dict:
    fact_frame = {
        "fact": "",
        "function": [],
        "sources": [],  # with validFrom, validTo, citation juriconnect and text
        "explanation": ""
    }
    return fact_frame

def create_empty_duty_frame() -> dict:
    duty_frame = {
        "duty": "",
        "duty holder": "",
        "claimant": "",
        "terminating act": [],
        "creating act": [],
        "enforcing act": "",
        "sources": [],
    }
    return duty_frame
