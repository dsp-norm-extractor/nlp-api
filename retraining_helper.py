import csv



def get_sentences_and_labels_from_db(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['sentence', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for doc in data:
            for sent in doc["details"]:
                sentence = sent["sentence"]
                label = ""
                
                if sent["acts"]:
                    label += "ACT "
                if sent["facts"]:
                    label += "FACT "
                if sent["duties"]:
                    label += "DUTY"
                
                writer.writerow({'sentence': sentence, 'label': label})






def do_model_retraining(data):

    csv_filename = 'output.csv'
    get_sentences_and_labels_from_db(data, csv_filename)
