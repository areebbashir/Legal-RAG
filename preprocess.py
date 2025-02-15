import pdfplumber
import os
import openai
import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from vectorDB import create_vector_db
openAI_key = "your-openai-key"
openai.api_key = openAI_key

# Model for Embedding
EMBEDDING_MODEL = "text-embedding-ada-002"

# Directory to save vector DB
VECTOR_DB_DIR = "/content/vectorDB"

# Extract data using pdfplumber
def extract_data2(pdf_path):
    """
    Extracts and merges text data from a PDF, grouped by page.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list[dict]: List of dictionaries containing text and page numbers.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = []
        for page_number, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text.append({"page_number": page_number + 1, "text": page_text.replace("_", "").replace("\n", " ")})
    return text

# Chunking function
def chunk_text(data, chunk_size=500):
    """
    Splits the text data into smaller chunks of specified size.

    Args:
        data (list[dict]): List of dictionaries containing text and page numbers.
        chunk_size (int): Maximum number of characters per chunk.

    Returns:
        list[dict]: List of chunks with text and metadata.
    """
    chunks = []
    for page in data:
        page_text = page["text"]
        for i in range(0, len(page_text), chunk_size):
            chunk = page_text[i:i + chunk_size]
            chunks.append({"text": chunk, "page_number": page["page_number"]})
    return chunks

# Main function
def process_pdf(pdf_path, db_dir):
    """
    Processes a PDF file: extracts text, chunks it, and creates a vector DB.

    Args:
        pdf_path (str): Path to the PDF file.
        db_dir (str): Directory to save the vector database.

    Returns:
        str: Path to the created vector database.
    """
    file_name = os.path.basename(pdf_path).split(".")[0]
    db_path = os.path.join(db_dir, f"{file_name}_vector_db.pkl")

    print("Extracting text...")
    data = extract_data2(pdf_path)

    print("Chunking text...")
    chunks = chunk_text(data)

    print("Creating vector database...")
    create_vector_db(chunks, db_path)

    print(f"Vector database saved at: {db_path}")
    return db_path
