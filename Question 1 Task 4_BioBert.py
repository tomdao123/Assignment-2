import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Get the full path of the current file
file_path = os.path.realpath(__file__)
directory_path = os.path.dirname(file_path)
file_path = os.path.join(directory_path, 'texts.txt')

# Function to split the large text file into smaller chunks
def split_file(file_path, chunk_size_mb=20):
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_number = 1

    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            part_file_path = os.path.join(directory_path, f"text_part_{file_number}.txt")
            with open(part_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = file.read(chunk_size)
    return file_number - 1  # Return the number of chunks

# Split the text file into chunks
count = split_file(file_path, chunk_size_mb=20)

# Function to load the tokenizer and model, and perform NER (Named Entity Recognition)
def extract_disease_and_drug(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)  # By default, this uses PyTorch
    
    # Identify entities in the text
    ner_results = ner_pipeline(text)
    return ner_results

# Initialize lists to store extracted diseases and drugs
diseases = []
drugs = []

# Load BioBERT NER models once for efficiency
disease_model_name = "ugaray96/biobert_ncbi_disease_ner"
drug_model_name = "alvaroalon2/biobert_chemical_ner"

# Loop through each chunk file and process it
for i in range(1, count + 1):
    part_file_path = os.path.join(directory_path, f"text_part_{i}.txt")
    print(f"Processing: {part_file_path}")

    # Read the content of the current chunk
    with open(part_file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower().strip()

    # Extract diseases
    ner_results = extract_disease_and_drug(text, disease_model_name)
    for result in ner_results:
        if result["entity"] == "Disease":
            diseases.append(result['word'])

    # Extract drugs
    ner_results = extract_disease_and_drug(text, drug_model_name)
    for result in ner_results:
        if result["entity"] == "B-CHEMICAL":
            drugs.append(result['word'])

    # Clean up chunk file after processing
    if os.path.exists(part_file_path):
        os.remove(part_file_path)

# Write the extracted diseases and drugs to an output file
output_file_path = os.path.join(directory_path, 'text_BioBert.txt')
with open(output_file_path, 'w') as fp:
    fp.write("Total Extracted Diseases: " + str(len(diseases)) + "\n")
    for disease in diseases:
        fp.write("%s\n" % disease)
    print('Diseases extraction complete.')

    fp.write("\nTotal Extracted Drugs: " + str(len(drugs)) + "\n")
    for drug in drugs:
        fp.write("%s\n" % drug)
    print('Drugs extraction complete.')

