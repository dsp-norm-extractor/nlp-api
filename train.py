# import pandas as pd
# from datasets import Dataset, DatasetDict
# import torch
# from ipywidgets import IntProgress
# import ast
# import os
# from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer, PreTrainedModel
# import itertools
# from transformers import DataCollatorForTokenClassification
# from datasets import load_metric
# import numpy as np
# from sklearn.model_selection import train_test_split
# import string
# import csv
# import collections
# import tensorflow as tf
# from transformers import BertTokenizer, TFBertForSequenceClassification
# from transformers import AutoTokenizer
# from sklearn.preprocessing import LabelEncoder
# from transformers import DataCollatorWithPadding
# import evaluate
# import torch
# from torch.utils.data import Dataset
# from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
# from datasets import Dataset as HF_Dataset, DatasetDict


# def compute_metrics2(p):
#     predictions, labels = p
#     predictions = np.argmax(predictions, axis=2)

#     # Remove ignored index (special tokens)
#     true_predictions = [
#         [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
#         for prediction, label in zip(predictions, labels)
#     ]
#     true_labels = [
#         [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
#         for prediction, label in zip(predictions, labels)
#     ]

#     results = metric.compute(predictions=true_predictions, references=true_labels)
#     return {
#         "precision": results["overall_precision"],
#         "recall": results["overall_recall"],
#         "f1": results["overall_f1"],
#         "accuracy": results["overall_accuracy"],
#     }

# def tokenize_and_align_labels(examples, label_all_tokens = True):
#     tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

#     labels = []
#     for i, label in enumerate(examples["srl_tags"]):
#         word_ids = tokenized_inputs.word_ids(batch_index=i)
#         previous_word_idx = None
#         label_ids = []
#         for word_idx in word_ids:
#             # Special tokens have a word id that is None. We set the label to -100 so they are automatically
#             # ignored in the loss function.
#             if word_idx is None:
#                 label_ids.append(-100)
#             # We set the label for the first token of each word.
#             elif word_idx != previous_word_idx:
#                 label_ids.append(label[word_idx])
#             # For the other tokens in a word, we set the label to either the current label or -100, depending on
#             # the label_all_tokens flag.
#             else:
#                 label_ids.append(label[word_idx] if label_all_tokens else -100)
#             previous_word_idx = word_idx

#         labels.append(label_ids)

#     tokenized_inputs["labels"] = labels
#     return tokenized_inputs
    
# accuracy = evaluate.load("accuracy")
# def compute_metrics(eval_pred):
#     predictions, labels = eval_pred
#     predictions = np.argmax(predictions, axis=1)
#     return accuracy.compute(predictions=predictions, references=labels)

# def read_csv_to_df(csv_file):
#     dataframe = pd.read_csv(csv_file, sep = ",")
#     return dataframe

# def read_csv_to_df2(csv_file):
#     dataframe = pd.read_csv(csv_file, sep = ",", converters={'tokens': eval, 'srl_tags': eval})
#     return dataframe

# def preprocess_function(row):
#     tokenized_result = tokenizer(row["Sentence"], truncation=True)
#     return pd.Series({
#         'input_ids': tokenized_result['input_ids'],
#         'attention_mask': tokenized_result['attention_mask'],
#         'Label': row['Label'],
#     })


# class CustomDataset(Dataset):
#     def __init__(self, dataframe):
#         self.data = dataframe

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         sample = {
#             'input_ids': self.data['input_ids'].iloc[idx],
#             'attention_mask': self.data['attention_mask'].iloc[idx],
#             'label': self.data['Label_Encoded'].iloc[idx]
#         }
#         return sample
    

# if __name__ == "__main__":

    
# #------------------Sequence classifier    
#     tagged_file = os.path.abspath("sent_ds.csv")
#     dataframe = read_csv_to_df(tagged_file)
#     df_to_train = dataframe [['Game','Sentence', 'Label', 'Tokens']]
    
#     #preprocessing
#     tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    
#     tokenized_df = df_to_train.apply(preprocess_function, axis = 1)
    
#     data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
#     #encode labels
#     label_encoder = LabelEncoder()
#     tokenized_df['Label_Encoded'] = label_encoder.fit_transform(tokenized_df['Label'])

#     num_labels = tokenized_df['Label_Encoded'].nunique()
#     unique_labels = tokenized_df['Label'].unique()

#     id2label = {i: label for i, label in enumerate(unique_labels)}
#     label2id = {label: i for i, label in enumerate(unique_labels)}

#     tokenized_df.drop(columns = 'Label', inplace = True)
     
        
#     #create datasets to train
#     train_df, test_df = train_test_split(tokenized_df, test_size=0.2, random_state = 69)

#     train_dataset = CustomDataset(train_df)
#     test_dataset = CustomDataset(test_df)
    
#     datasets = DatasetDict({
#         'train': train_dataset,
#         'test': test_dataset,
#     })

#     # Model initialization and training configuration
#     model = AutoModelForSequenceClassification.from_pretrained(
#         "distilbert-base-uncased", num_labels=num_labels, id2label=id2label, label2id=label2id
#     ) 

#     training_args = TrainingArguments(
#         output_dir="class_model_v6",
#         learning_rate=2e-5,
#         per_device_train_batch_size=16,
#         per_device_eval_batch_size=16,
#         num_train_epochs=5,
#         weight_decay=0.01,
#         evaluation_strategy="epoch",
#         save_strategy="epoch",
#         load_best_model_at_end=True
#     )

#     train_dataset = datasets['train']
#     test_dataset = datasets['test']

#     # Training the model
#     trainer = Trainer(
#         model=model,
#         args=training_args,
#         train_dataset=train_dataset,
#         eval_dataset=test_dataset,  # Use the test dataset for evaluation
#         tokenizer=tokenizer,
#         data_collator=data_collator,
#         compute_metrics=compute_metrics,
#     ) 

#     trainer.train()
    
#     #save and reload models
#     trainer.save_model("my_model_v2")
#     loaded_model = AutoModelForSequenceClassification.from_pretrained("my_model_v2")
#     tokenizer.save_pretrained("my_model_v2")
#     loaded_tokenizer = AutoTokenizer.from_pretrained("my_model_v2")
    
    
    
# #------------------Duty classifier  
#     tagged_file = os.path.abspath("duty_ds.csv")
#     dataframe = read_csv_to_df2(tagged_file)
#     df_to_train = dataframe[['Sentence', 'tokens', 'srl_tags']]
#     srl_keys={"O": 0,
#           "Duty Holder": 1,
#           "Claimant": 2,
#           "Action": 3,
#           "Object": 4,
#          "CA": 5, "EA": 6}

#     df_to_train.rename(columns={'srl_tags': 'srl_tags_name'}, inplace=True)

#     #encode srl tags 
#     srl_tags_numbers = []
#     for index, row in df_to_train.iterrows():
#         srl_tags_numbers.append([srl_keys.get(item) for item in row['srl_tags_name']])  
#     df_to_train['srl_tags'] = srl_tags_numbers
    
#     #convert to dataset
#     from datasets import Dataset, DatasetDict
#     dataset = Dataset.from_pandas(df_to_train)
#     # 90% train, 10% test + validation
#     train_testvalid = dataset.train_test_split(test_size=0.1)

#     # Split the 10% test + valid in half test, half valid
#     test_valid = train_testvalid['test'].train_test_split(test_size=0.5)

#     # Collect the two into a single DatasetDict
#     datasets = DatasetDict({
#         'train': train_testvalid['train'],
#         'test': test_valid['test'],
#         'validation': test_valid['train']})
    
#     preprocessed_input = tokenize_and_align_labels(datasets['train'])
    
#     tokenized_datasets = datasets.map(tokenize_and_align_labels, batched=True)
    
#     srl_tags_set = set(itertools.chain.from_iterable(tokenized_datasets['train']['srl_tags_name']))
#     model = AutoModelForTokenClassification.from_pretrained("distilbert-base-uncased", num_labels=len(srl_tags_set))

#     batch_size = 8

#     args = TrainingArguments(
#         output_dir=".",
#         evaluation_strategy = "epoch",
#         learning_rate=5e-5,
#         #per_device_train_batch_size=batch_size,
#         #per_device_eval_batch_size=batch_size,
#         num_train_epochs=4,
#         weight_decay=0.01
#     )
    
#     data_collator = DataCollatorForTokenClassification(tokenizer)

#     metric = load_metric("seqeval")
    
#     label_list = list(srl_tags_set)
#     labels_str = tokenized_datasets['train']['srl_tags_name'][0]
#     labels_indices = [label_list.index(label) for label in labels_str]
    
#     #Replace other None values (commans, periods etc) to -100
#     tokenized_datasets['train'] = tokenized_datasets['train'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )

#     tokenized_datasets['validation'] = tokenized_datasets['validation'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )

#     tokenized_datasets['test'] = tokenized_datasets['test'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )
    
#     act_trainer = Trainer(
#         model=model,
#         args=args,
#         train_dataset=tokenized_datasets["train"],
#         eval_dataset=tokenized_datasets["validation"],
#         data_collator=data_collator,
#         tokenizer=tokenizer,
#         compute_metrics=compute_metrics2
#     )
#     act_trainer.train()
    
#     act_trainer.save_model("trained_duty_model3")
#     tokenizer.save_pretrained("trained_duty_model3")
#     model.config.save_pretrained("trained_duty_model3")
    
#     model = AutoModelForSequenceClassification.from_pretrained("trained_duty_model3")
#     tokenizer = AutoTokenizer.from_pretrained("trained_duty_model3")
    
# #------------------Act classifier
#     tagged_file = os.path.abspath("duty_ds.csv")
#     dataframe = read_csv_to_df2(tagged_file)
#     df_to_train = dataframe[['Sentence', 'tokens', 'srl_tags']]
#     srl_keys = {"O": 0,
#             "Action": 1,
#             "Actor": 2,
#             "Object": 3,
#             "Recipient": 4,
#             "PR": 5,
#             "CF": 6}


#     df_to_train.rename(columns={'srl_tags': 'srl_tags_name'}, inplace=True)

#     #encode srl tags 
#     srl_tags_numbers = []
#     for index, row in df_to_train.iterrows():
#         srl_tags_numbers.append([srl_keys.get(item) for item in row['srl_tags_name']])  
#     df_to_train['srl_tags'] = srl_tags_numbers
    
#     #convert to dataset
#     from datasets import Dataset, DatasetDict
#     dataset = Dataset.from_pandas(df_to_train)
#     # 90% train, 10% test + validation
#     train_testvalid = dataset.train_test_split(test_size=0.1)

#     # Split the 10% test + valid in half test, half valid
#     test_valid = train_testvalid['test'].train_test_split(test_size=0.5)

#     # Collect the two into a single DatasetDict
#     datasets = DatasetDict({
#         'train': train_testvalid['train'],
#         'test': test_valid['test'],
#         'validation': test_valid['train']})
    
#     preprocessed_input = tokenize_and_align_labels(datasets['train'])
    
#     tokenized_datasets = datasets.map(tokenize_and_align_labels, batched=True)
    
#     srl_tags_set = set(itertools.chain.from_iterable(tokenized_datasets['train']['srl_tags_name']))
#     model = AutoModelForTokenClassification.from_pretrained("distilbert-base-uncased", num_labels=len(srl_tags_set))

#     batch_size = 8

#     args = TrainingArguments(
#         output_dir=".",
#         evaluation_strategy = "epoch",
#         learning_rate=5e-5,
#         #per_device_train_batch_size=batch_size,
#         #per_device_eval_batch_size=batch_size,
#         num_train_epochs=4,
#         weight_decay=0.01
#     )
    
#     data_collator = DataCollatorForTokenClassification(tokenizer)

#     metric = load_metric("seqeval")
    
#     label_list = list(srl_tags_set)
#     labels_str = tokenized_datasets['train']['srl_tags_name'][0]
#     labels_indices = [label_list.index(label) for label in labels_str]
    
#     #Replace other None values (commans, periods etc) to -100
#     tokenized_datasets['train'] = tokenized_datasets['train'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )

#     tokenized_datasets['validation'] = tokenized_datasets['validation'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )

#     tokenized_datasets['test'] = tokenized_datasets['test'].map(
#     lambda example: {'labels': [0 if label is None else label for label in example['labels']]}
#     )
    
#     act_trainer = Trainer(
#         model=model,
#         args=args,
#         train_dataset=tokenized_datasets["train"],
#         eval_dataset=tokenized_datasets["validation"],
#         data_collator=data_collator,
#         tokenizer=tokenizer,
#         compute_metrics=compute_metrics2
#     )
#     act_trainer.train()
    
#     act_trainer.save_model("trained_act_model3")
#     tokenizer.save_pretrained("trained_act_model3")
#     model.config.save_pretrained("trained_act_model3")
    
#     model = AutoModelForSequenceClassification.from_pretrained("trained_act_model3")
#     tokenizer = AutoTokenizer.from_pretrained("trained_act_model3") 
    

    