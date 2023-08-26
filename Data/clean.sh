#!/bin/bash

# Create a new directory named CleanedData, if it doesn't already exist
mkdir -p CleanedData

# Spiritual
cat faith.txt god.txt spirituality.txt religion.txt > CleanedData/spiritual.txt

# Love
cat love.txt relationships.txt romance.txt > CleanedData/love.txt

# Inspirational
cat inspiration.txt inspirational-quotes.txt inspirational.txt motivation.txt motivational.txt > CleanedData/inspirational.txt

# Knowledge
cat life-lessons.txt life-quotes.txt life.txt > CleanedData/knowledge.txt

# Wisdom
cat knowledge.txt wisdom.txt > CleanedData/wisdom.txt

# Literary
cat poetry.txt writing.txt > CleanedData/literary.txt

# Copy the individual files to the CleanedData directory
cp death.txt CleanedData/
cp philosophy.txt CleanedData/
cp happiness.txt CleanedData/
cp hope.txt CleanedData/
cp time.txt CleanedData/
cp truth.txt CleanedData/
cp humor.txt CleanedData/
cp science.txt CleanedData/
cp success.txt CleanedData/

echo "Files have been grouped, merged, and copied to the CleanedData folder."

# Remove duplicate lines (while keeping one instance) from the files in CleanedData directory
for file in CleanedData/*.txt; do
    sort "$file" | uniq > "${file}.tmp" && mv "${file}.tmp" "$file"
done

echo "Duplicate lines have been removed from the files in the CleanedData folder, while keeping one instance of each line."

# Run the python script on the files in the CleanedData directory
for file in CleanedData/*.txt; do
    python3 clean.py "$file"
done

echo "Files in the CleanedData directory have been cleaned using the Python script."

