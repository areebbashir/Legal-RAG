#  RAG Legal PDF Processor

## Overview
The RAG Legal PDF Processor is a Retrieval-Augmented Generation (RAG) system designed to extract, process, and generate responses based on legal PDFs. This system enables efficient retrieval of legal information and provides accurate, context-aware answers to user queries.
The task at hand is to extract three specific fields from a set of legal contract PDFs:
1.	**Effective Date**: The date when the contract becomes effective.
2.	**Expiration Date**: The date when the contract expires.
3.	**Parties**: The names of the legal entities involved in the contract.


## Features
- **PDF Parsing**: Extracts text from legal PDFs using OCR and text-based extraction methods.
- **Document Chunking**: Splits large legal documents into manageable segments for better retrieval efficiency.
- **Vector Search**: Embeds document chunks into a vector database for fast and relevant information retrieval.
- **LLM-powered Responses**: Uses a large language model (LLM) to generate detailed and context-aware answers.
- **Metadata Extraction**: Identifies and processes key legal metadata such as name of the parties involved, Effective date and expiration date of the contract.

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
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Processing PDFs
1. Place legal PDFs in the `data/` directory.
2. Run the document processing script:
   ```sh
      python main.py "sample.pdf"
   ```
3. The output should be like:
   ```sh
      Time taken for dataset__0__4.pdf: 2.68 seconds
      ______________________________________________
      
      Extracted Data:
      {
          "dataset__0__4.pdf": {
              "Effective Date": {
                  "response": "01/03/2023"
              },
              "Expiration Date": {
                  "response": "31/01/2024"
              },
              "Parties": {
                  "response": "[\"BOARD OF COUNTY COMMISSIONERS\", \"CONSULTANT\"]"
              }
          }
      }
   Results saved to data_pred.json
   ```
4. For viewing the evaluation metrics check out RAG_Metrics.ipynb


## Dependencies
- `fitz` (PDF parsing)
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


