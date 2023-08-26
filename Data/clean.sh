#!/bin/bash

# Source directory for raw text files
src_dir="./RawData"

# Create CleanedData directory
mkdir -p CleanedData

# Merge and group files by category
cat $src_dir/{faith,god,spirituality,religion}.txt > CleanedData/spiritual.txt
cat $src_dir/{love,relationships,romance}.txt > CleanedData/love.txt
cat $src_dir/{inspiration,inspirational-quotes,inspirational,motivation,motivational}.txt > CleanedData/inspirational.txt
cat $src_dir/{life-lessons,life-quotes,life}.txt > CleanedData/knowledge.txt
cat $src_dir/{knowledge,wisdom}.txt > CleanedData/wisdom.txt
cat $src_dir/{poetry,writing}.txt > CleanedData/literary.txt

# Copy individual files
cp $src_dir/{death,philosophy,happiness,hope,time,truth,humor,science,success}.txt CleanedData/

# Remove duplicates
for file in CleanedData/*.txt; do
    sort "$file" | uniq > "${file}.tmp" && mv "${file}.tmp" "$file"
done

# Run Python cleaning script
for file in CleanedData/*.txt; do
    python3 clean.py "$file"
done
