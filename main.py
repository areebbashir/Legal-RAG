from new_preprocess_vectordb import extract_data2, chunk_text
from vectordb import create_vector_db, search_vector_db
import json
import os
import re
import pdfplumber
from openai import OpenAI
import time
import argparse
openAI_key = "your-openai-key"
client = OpenAI(api_key=openAI_key)
folder_path = "/content/pdfs/"

def create_prompt(context, field):
    if field == "Effective Date":
      prompt_field = "Effective Date or Start Date"
    elif field == "Expiration Date":
      prompt_field = "Expiration Date or End Date"
    else: 
      prompt_field = "Companies or Organisations or Corporations"
    prompt = f"""
    You are an expert contract analyst. Extract the {prompt_field} from the following contract text.
    Contract Text:
    {context}

    Respond with ONLY and ONLY {prompt_field} with the format specified below and nothing else.
    The output should contain only the given format. If the {prompt_field} is not found reply with N/A.
    """
    if field == "Expiration Date":
      prompt+='Some times Expiration Date or End Date may not be explicitly given but it can be written for e.g "The contract expires 2 years from the effective date", which would mean Expiration data is equal to Effective date plus 2 years which you would have to figure out.'
    if prompt_field == "Effective Date or Start Date" or prompt_field == "Expiration Date or End Date":
        prompt += "Format: dd/mm/yyyy"
    elif prompt_field == "Companies or Organisations or Corporations":
        prompt += 'Format:["Party 1", "Party 2"]'
    return prompt

def get_llm_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content



import json
import os
import re
from openai import OpenAI


def extract_fields(pdf_path):
    llm_fields = {"Effective Date": None, "Expiration Date": None, "Parties": None}
    
    data = extract_data2("/content/pdfs/"+pdf_path)
    chunks = chunk_text(data)
    create_vector_db(chunks, "/content/vectorDB/" + pdf_path.split(".")[0])
    db_fields = ["Effective Date Start Date from", "Expire Date End Date to", "Company"]
    for db_field, llm_field in zip(db_fields, llm_fields.keys()):
        best_response = "N/A"
        retry = 0 
        while best_response =="N/A":
            print(f"Searching for '{db_field}' in the document...")
            results = search_vector_db("/content/vectorDB/"+ pdf_path.split(".")[0], db_field)
            combined_context = "\n".join([chunk["text"] for chunk in results])
            prompt = create_prompt(combined_context, llm_field)
            response = get_llm_response(prompt)
            print(response)
            retry+=1
            if retry == 5: break
            if response != "N/A":
                best_response = response
                break
            
        if best_response == "N/A":
            best_response = "-"
        llm_fields[llm_field] = {"response": best_response}
    return llm_fields





if __name__ == "__main__":
    # Set up argument parser for PDF path
    parser = argparse.ArgumentParser(description="Process PDF and extract fields.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    args = parser.parse_args()

    # Initialize variables
    pdf_path = args.pdf_path
    json_file = []
    time_taken_per_document = []

    # Start processing the given PDF
    start_time = time.time()
    extracted_data = extract_fields(pdf_path)
    end_time = time.time()

    time_taken = end_time - start_time
    time_taken_per_document.append(time_taken)

    json_file.append({pdf_path: extracted_data})
    print(f"Time taken for {pdf_path}: {time_taken:.2f} seconds")
    print(f"______________________________________________")

    # Save the results to a JSON file
    output_json = {}
    for item in json_file:
        output_json.update(item)

    # Print the output_json to see the results
    print("\nExtracted Data:")
    print(json.dumps(output_json, indent=4))

    with open("Outputs.json", "w") as outfile:
        json.dump(output_json, outfile, indent=4)

    print("\nResults saved to Outputs.json")


