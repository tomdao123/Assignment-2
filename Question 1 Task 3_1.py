import pandas as pd
import os
import re
import csv
import sys

file_path = os.path.realpath(__file__)
directory_path = os.path.dirname(file_path)

# Read the content of the text file
with open(os.path.join(directory_path, 'texts.txt')) as file:
    data = file.read().replace('\n', ' ')

# Function to count word occurrences
def word_count(text):
    counts = dict()
    # Normalize the input text: remove non-alphabet characters and split into words
    words = re.sub(r"[^a-zA-Z]", " ", text).split()

    for word in words:
        word = word.lower()  # Make the word lowercase for case-insensitive counting
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

# Sort word counts by frequency in descending order
sorted_list = sorted(word_count(data).items(), key=lambda x: x[1], reverse=True)

# Get the top 30 words
Print_List = sorted_list[:30]

# Print the top 30 words
for word, count in Print_List:
    print(f"{word}: {count}")

# Write the top 30 words to a CSV file
csv_file_path = os.path.join(directory_path, 'Top30Words.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['word', 'occurrences'])  # Write header
    writer.writerows(Print_List)  # Write the data
