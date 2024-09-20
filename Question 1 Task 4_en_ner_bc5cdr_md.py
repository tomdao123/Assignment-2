import spacy
import os

# Get the full path of the current file
file_path = os.path.realpath(__file__)
# Extract the directory path
directory_path = os.path.dirname(file_path)

file_path = directory_path + '/texts.txt'

# Function to split the file into smaller parts
def split_file(file_path, chunk_size_mb=2):
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_number = 1
    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            with open(directory_path + f'/text_part_{file_number}.txt', 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = file.read(chunk_size)
    return file_number - 1  # Return the total number of chunks

# Split the text file into chunks
count = split_file(file_path)

def extract(doc, diseases_list, drugs_list):
    """Extract diseases and chemicals from the document using SpaCy."""
    for ent in doc.ents:
        if ent.label_ == "DISEASE" and ent.text not in diseases_list:
            diseases_list.append(ent.text)
        elif ent.label_ == "CHEMICAL" and ent.text not in drugs_list:
            drugs_list.append(ent.text)

# Load the SpaCy model for diseases and drugs (BC5CDR model)
model = spacy.load("en_ner_bc5cdr_md")

diseases = []
drugs = []

# Process each split file and extract diseases and drugs
for i in range(1, count + 1):
    part_file_path = directory_path + f'/text_part_{i}.txt'
    print(f"Processing file: {part_file_path}")
    
    with open(part_file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower().strip()
        model.max_length = len(text) + 100  # Adjust max length if needed
        doc = model(text)
    
    extract(doc, diseases, drugs)
    
    # Remove the chunk file after processing
    if os.path.exists(part_file_path):
        os.remove(part_file_path)

# Write extracted entities to output file
output_file_path = os.path.join(directory_path, 'text_bc5cdr.txt')

with open(output_file_path, 'w') as fp:
    fp.write(f"Total Diseases Extracted: {len(diseases)}\n")
    fp.write("Diseases extracted:\n")
    for disease in diseases:
        fp.write(f"{disease}\n")
    
    fp.write(f"\nTotal Drugs Extracted: {len(drugs)}\n")
    fp.write("Drugs extracted:\n")
    for drug in drugs:
        fp.write(f"{drug}\n")

print("Entities extraction complete.")
print(f"Extracted {len(diseases)} diseases: {diseases}")
print(f"Extracted {len(drugs)} drugs: {drugs}")
