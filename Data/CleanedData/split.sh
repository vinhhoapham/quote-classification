#!/bin/bash

# Split ratios
TRAIN_RATIO=0.8
TEST_RATIO=0.1
# The remaining portion will be used for validation

# Create the directories if they don't exist and check for success
mkdir -p train test val

if [ ! -d "train" ] || [ ! -d "test" ] || [ ! -d "val" ]; then
    echo "Failed to create directories. Exiting."
    exit 1
fi

# Loop through all .txt files in the current directory
for file in *.txt; do
    # Shuffle the file and store it in a temporary file
    shuf "$file" > "${file}.tmp"
    
    # Get the total number of lines in the shuffled file
    TOTAL_LINES=$(wc -l < "${file}.tmp")
    
    # Calculate number of lines for train, test, and validation
    TRAIN_LINES=$(echo "$TOTAL_LINES * $TRAIN_RATIO" | bc | cut -d'.' -f1)
    TEST_LINES=$(echo "$TOTAL_LINES * $TEST_RATIO" | bc | cut -d'.' -f1)
    VAL_LINES=$(echo "$TOTAL_LINES - $TRAIN_LINES - $TEST_LINES" | bc)

    # Split the shuffled file
    head -n "$TRAIN_LINES" "${file}.tmp" > "train/$file"
    tail -n +$(($TRAIN_LINES + 1)) "${file}.tmp" | head -n "$TEST_LINES" > "test/$file"
    tail -n "$VAL_LINES" "${file}.tmp" > "val/$file"
    
    # Remove the temporary shuffled file
    rm "${file}.tmp"
done
