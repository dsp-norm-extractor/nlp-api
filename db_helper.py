from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
import certifi





def connect_to_mongo():
    #uri = "mongodb+srv://stathistrigas99:Di4hyHZrFagWA1iw@norms-for-games.uppnd2y.mongodb.net/?retryWrites=true&w=majority"
    

    uri = "mongodb+srv://stathis:NT7B2f4A2BgzN8JW@norms-for-games.uppnd2y.mongodb.net/?retryWrites=true&w=majority"

    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, tlsCAFile=certifi.where())

        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        
        print("Successfully connected to MongoDB!")

        return client

    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")



def get_data(client, database_name, collection_name):

    
    if client:
        try:

            # Access the specified database and collection
            db = client[database_name]
            collection = db[collection_name]


            # Perform your query or data retrieval here
            # Example: Fetch all documents in the collection
            result = collection.find({})
            
            for document in result:
                print(document)

        except Exception as e:
            print(f"Error getting data from MongoDB: {e}")

        # finally:
        #     # Close the MongoDB connection when done
        #     client.close()


def insert_document(client,database_name, collection_name, document):

    
    if client:
        try:
            # Access the specified database and collection
            db = client[database_name]
            collection = db[collection_name]

            # Insert the document into the collection
            result = collection.insert_one(document)

            print(f"Document inserted with ID: {result.inserted_id}")

        except Exception as e:
            print(f"Error inserting document into MongoDB: {e}")

        # finally:
        #     # Close the MongoDB connection when done
        #     client.close()