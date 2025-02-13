#  RAG Legal PDF Processor

## Overview
The RAG Legal PDF Processor is a Retrieval-Augmented Generation (RAG) system designed to extract, process, and generate responses based on legal PDFs. This system enables efficient retrieval of legal information and provides accurate, context-aware answers to user queries.

## Features
- **PDF Parsing**: Extracts text from legal PDFs using OCR and text-based extraction methods.
- **Document Chunking**: Splits large legal documents into manageable segments for better retrieval efficiency.
- **Vector Search**: Embeds document chunks into a vector database for fast and relevant information retrieval.
- **LLM-powered Responses**: Uses a large language model (LLM) to generate detailed and context-aware answers.
- **Metadata Extraction**: Identifies and processes key legal metadata such as case numbers, statutes, and court rulings.
- **Multi-document Querying**: Allows searching across multiple legal documents simultaneously.

## Installation
### Prerequisites
- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/areebbashir/Legal-RAG.git
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Processing PDFs
1. Place legal PDFs in the `data/` directory.
2. Run the document processing script:
   ```sh
   python process_documents.py
   ```
3. The extracted and embedded text will be stored in the vector database.

### Querying the System
Run the query interface to retrieve legal information:
```sh
python query.py --question "What is the precedent for contract disputes?"
```

## Dependencies
- `pymupdf` (PDF parsing)
- `openai` (LLM integration)
- `faiss` (Vector database)
- `transformers` (LLM models)
- `torch` (Deep learning framework)

## Roadmap
- [ ] Implement a great pdf parser which would extract unstructured pdfs
- [ ] Use a fast vector database for fast retrieval
- [ ] Create a evaluation metric like G-Eval


## Contact
For questions or contributions, contact **areebbashir13@gmail.com** or open an issue on GitHub.


