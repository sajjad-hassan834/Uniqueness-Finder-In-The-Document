import PyPDF2
import pandas as pd
import json
import io

async def process_file(file):
    print(f"Processing file: {file.filename}")
    file_extension = file.filename.split(".")[-1].lower()
    content = await file.read()
    try:
        if file_extension == "pdf":
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() for page in pdf_reader.pages)
        elif file_extension == "csv":
            # Extract text from CSV
            df = pd.read_csv(io.BytesIO(content))
            text = df.to_string(index=False)
        elif file_extension == "json":
            # Extract text from JSON
            data = json.loads(content)
            text = json.dumps(data)
        elif file_extension == "txt":
            # Read plain text
            text = content.decode("utf-8")
        else:
            raise ValueError("Unsupported file format")
        
        print(f"Processed content: {text[:100]}...")  # Print first 100 characters
        return text
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise ValueError(f"Error processing file: {str(e)}")