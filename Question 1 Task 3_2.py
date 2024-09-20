import os
import csv
import collections
from transformers import AutoTokenizer

# Disable unnecessary warnings and enable TensorFlow optimizations
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Get the full path of the current script
file_path = os.path.realpath(__file__)
directory_path = os.path.dirname(file_path)

# Path to the text file to process
file_path = os.path.join(directory_path, 'texts.txt')

# Function to split the large text file into smaller parts
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
    return file_number - 1

# Split the file into chunks
num_chunks = split_file(file_path)

# Function to count unique tokens in a file
def count_unique_tokens(file_path):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    token_counts = collections.Counter()
    max_length = 512  # BERT max token limit for processing chunks

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for i in range(0, len(line), max_length):
                chunk = line[i:i+max_length]
                tokens = tokenizer.tokenize(chunk)
                token_counts.update(tokens)

    return token_counts

# Dictionary to store overall token counts
overall_token_counts = collections.Counter()

# Process each chunk and update the token counts
for i in range(1, num_chunks + 1):
    chunk_file_path = os.path.join(directory_path, f"text_part_{i}.txt")
    print(f"Processing: {chunk_file_path}")
    
    # Update overall token counts with current chunk's counts
    chunk_token_counts = count_unique_tokens(chunk_file_path)
    overall_token_counts.update(chunk_token_counts)
    
    # Remove the chunk file after processing
    if os.path.exists(chunk_file_path):
        os.remove(chunk_file_path)

# Sort tokens by occurrence count (descending) and take the top 30
top_30_tokens = overall_token_counts.most_common(30)

# Output top tokens
for token, count in top_30_tokens:
    print(f"{token}: {count}")

# Write the top 30 tokens to a CSV file
csv_file_path = os.path.join(directory_path, 'Top30Tokens.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['token', 'occurrences'])
    writer.writerows(top_30_tokens)