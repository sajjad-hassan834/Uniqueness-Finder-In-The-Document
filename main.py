from fastapi import FastAPI, File, UploadFile
from utils.file_processor import process_file
from utils.similarity import check_uniqueness
from utils.chromadb_handler import ChromaDBHandler

app = FastAPI()

# Initialize ChromaDB handler
db_handler = ChromaDBHandler(persist_directory="./chromadb_data", Unique_db="file_storage")

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Process the uploaded file
        file_content = await process_file(file)
        
        # Generate embedding for the new content
        embedding = db_handler.generate_embedding(file_content)
        
        # Check uniqueness against ChromaDB
        uniqueness_score = check_uniqueness(embedding, db_handler.collection)
        
        # Store the new embedding in ChromaDB
        db_handler.add_document(file.filename, embedding)
        
        if uniqueness_score >= 0.6:
            return {"message": "This is good", "uniqueness_score": uniqueness_score}
        else:
            return {"message": "Not okay", "uniqueness_score": uniqueness_score}
    except Exception as e:
        return {"error": str(e)}