# Nlp api

This is an api that predicts the aplicable frames for a sentence

## Installation

### 1. Install dependencies

```bash
pip install tensorflow fastapi uvicorn
```

### 2. Run project

```bash
python3 main.py
```

### Usecase : Sent a list

```bash
["example sentece 1", "example sentece 2"]
```

### Response Structure

```bash
[
    {
        "sentence": "example sentece 1",
        "frames": {
            "acts": [
                {
                    "act": "",
                    "actor": "",
                    "action": "",
                    "object": "",
                    "recipient": "",
                    "preconditions": {
                        "expression": "LITERAL",
                        "operand": true
                    },
                    "create": [],
                    "terminate": [],
                    "sources": [],
                    "explanation": ""
                }
            ],
            "facts": [
                {
                    "fact": "",
                    "function": [],
                    "sources": [],
                    "explanation": ""
                }
            ],
            "duties": [
                {
                    "duty": "",
                    "duty holder": "",
                    "claimant": "",
                    "terminating act": [],
                    "creating act": [],
                    "enforcing act": "",
                    "sources": []
                }
            ]
        }
    },
    {
        "sentence": "example sentece 2",
        "frames": {
            "acts": [
                {
                    "act": "",
                    "actor": "",
                    "action": "",
                    "object": "",
                    "recipient": "",
                    "preconditions": {
                        "expression": "LITERAL",
                        "operand": true
                    },
                    "create": [],
                    "terminate": [],
                    "sources": [],
                    "explanation": ""
                }
            ],
            "facts": [
                {
                    "fact": "",
                    "function": [],
                    "sources": [],
                    "explanation": ""
                }
            ],
            "duties": [
                {
                    "duty": "",
                    "duty holder": "",
                    "claimant": "",
                    "terminating act": [],
                    "creating act": [],
                    "enforcing act": "",
                    "sources": []
                }
            ]
        }
    }
]
```
