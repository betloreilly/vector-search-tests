from sentence_transformers import SentenceTransformer
import pymongo

# import the embedding model
# https://huggingface.co/obrizum/all-MiniLM-L6-v2
model = SentenceTransformer('obrizum/all-MiniLM-L6-v2')

# mongo connection
mongo_uri = ""
connection = pymongo.MongoClient(mongo_uri)
db = connection.sample_airbnb
collection = db.listingsAndReviews

# Replacing the documents with a new embedding column
for doc in collection.find({'summary':{"$exists": True}}):
    embeddings = model.encode(doc['summary']).tolist()
    doc['embedding'] = embeddings
    collection.replace_one({'_id': doc['_id']}, doc)
    
	
query = "central place in Istanbul"
vector_query = model.encode(query).tolist()
results = collection.aggregate([
    {
        '$search': {
            "index": "summarysearch",
            "knnBeta": {
                "vector": vector_query,
                "k": 4,
                "path": "embedding"}
        }
    }
])


for document in results:
    print(f'Airbnb Name: {document["name"]},\nSummary: {document["summary"]}\n')

