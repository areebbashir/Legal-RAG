from openai import OpenAI
import faiss
import numpy as np
import json

class VectorDB:
    def __init__(self, client):
        
        self.client = client
        
    def get_embedding(self, texts):
        """
        Retrieves embeddings for the given texts using OpenAI's embeddings API.
        
        Args:
            texts (list): List of texts for which embeddings are to be retrieved.
        
        Returns:
            numpy.ndarray: A numpy array containing the embeddings of the input texts.
        """
        response = self.client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
        )
        embeddings = np.array([data.embedding for data in response.data])
        return embeddings
    
    def save_vector_db(self, index, metadata, db_path):
        """
        Saves the FAISS index and metadata to disk.
        
        Args:
            index (faiss.Index): The FAISS index object to be saved.
            metadata (dict): The metadata associated with the vector data.
            db_path (str): The path where the vector database should be saved.
        """
        faiss.write_index(index, f"{db_path}_index.faiss")
        with open(f"{db_path}_metadata.json", "w") as f:
            json.dump(metadata, f)
            
    def load_vector_db(self, db_path):
        """
        Loads a saved FAISS index and metadata from disk.
        
        Args:
            db_path (str): The path where the vector database is stored.
        
        Returns:
            tuple: A tuple containing the loaded FAISS index and metadata.
        """
        index = faiss.read_index(f"{db_path}_index.faiss")
        with open(f"{db_path}_metadata.json", "r") as f:
            metadata = json.load(f)
        return index, metadata
    def create_vector_db(self, chunks, db_path):
        """
        Creates a vector database by converting text chunks into embeddings and saving them.
        
        Args:
            chunks (list): A list of text chunks to be converted into embeddings.
            db_path (str): The path where the vector database should be saved.
        """
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.get_embedding(texts)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        
        metadata = [{"page_num": chunk["page_num"], "text": chunk["text"]} for chunk in chunks]

        
        self.save_vector_db(index, metadata, db_path)
        
        
    def search_vector_db(self, db_path, query, top_k=3):
        """
        Searches the vector database for the most relevant results based on the query.
        
        Args:
            db_path (str): The path where the vector database is stored.
            query (str): The search query.
            top_k (int): The number of top results to return.
        
        Returns:
            list: A list of the top k most relevant results based on the search query.
        """
        index, metadata = self.load_vector_db(db_path)

    
        query_embedding = self.get_embedding([query])
        distances, indices = index.search(query_embedding, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(metadata[idx])
        return results