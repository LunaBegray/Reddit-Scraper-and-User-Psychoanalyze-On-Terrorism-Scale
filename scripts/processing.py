import re
import json

def clean_raw_data(input_file):
    """
    Cleans the raw data from the input file by removing special characters,
    escape sequences (like \n, \\), and all spaces, and replacing specific patterns like 'n'.
    """
    try:
        # Read raw data from the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            raw_data = file.read()

        # Step 1: Remove 'n' occurrences that are not part of valid JSON
        cleaned_data = raw_data.replace("n", "")

        # Step 2: Remove all backslashes
        cleaned_data = cleaned_data.replace("\\", "")

        # Step 3: Remove newlines, tabs, and other whitespace
        cleaned_data = re.sub(r'\s+', '', cleaned_data)

        # Step 4: Ensure valid JSON-like structure
        cleaned_data = re.sub(r'[^\x00-\x7F]+', '', cleaned_data)  # Remove non-ASCII characters

        # Step 5: Remove enclosing quotes if present
        if cleaned_data.startswith('"') and cleaned_data.endswith('"'):
            cleaned_data = cleaned_data[1:-1]

        # Return cleaned data
        return cleaned_data

    except Exception as e:
        print(f"Error processing data: {e}")
        return ""

def save_as_json(cleaned_data, output_file):
    """
    Converts the cleaned string into JSON format and saves it to a file.
    """
    try:
        # Convert the cleaned string into a Python dictionary
        json_data = json.loads(cleaned_data)

        # Save the JSON data to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)

        print(f"Processed data saved to {output_file}.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Cleaned data that caused the error: {cleaned_data}")
    except Exception as e:
        print(f"Error saving JSON data: {e}")

def process_and_save_json():
    """
    Main function to process the raw data and save it as a JSON file.
    """
    input_file = './data/user_analysis_db'  # Path to your raw data file
    output_file = './data/analyzed_db.json'  # Path to save the processed JSON file

    # Clean the raw data
    cleaned_data = clean_raw_data(input_file)

    # Save the cleaned data as a JSON file
    save_as_json(cleaned_data, output_file)

# Call the function to process and save the JSON
if __name__ == "__main__":
    process_and_save_json()
