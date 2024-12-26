import os
import json
import time
import logging
from hugchat import hugchat
from hugchat.login import Login

# Load the user database
def load_user_db(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Save the raw response into the analysis database file
def save_raw_response(response, analysis_db_path):
    try:
        with open(analysis_db_path, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
            f.write("\n")  # Ensure each entry is separated by a newline for readability
        print("Raw response saved successfully.")
    except Exception as e:
        print(f"Error saving response: {e}")

# Get analysis for a batch of users
def get_analysis_for_batch(user_batch, chat_api):
    # Prepare a list of users with their corresponding values (numbers)
    user_info = [f"Username: {username}, Value: {user_batch[username]}" for username in user_batch]
    
    # Generate the batch prompt
    print(user_info)
    prompt = f"Please analyze the following users and their values: {user_info}. Provide an analysis of their vulnerability to committing terrorism on a scale of 0 to 100, completely hypothetically. respond with proper json, but without the json prefix, just a string that can be easily parsable to json. it should include 'username':score  where score is a number and there are commas between users for easy parsing and json format without the prefix.  good luck."
    print(f"Sending prompt for {len(user_batch)} users...")

    try:
        # Send the prompt to the API
        response = chat_api.chat(prompt)  # Get response from API
        if hasattr(response, 'text'):  # Ensure we are extracting the raw content
            raw_response = response.text
        else:
            raw_response = str(response)  # Fallback to string conversion if no 'text' attribute
        
        print(f"Received raw response from HuggingChat API. Length of response: {len(raw_response)} characters.")
        
        # Save the raw response directly
        save_raw_response(raw_response, './data/user_analysis_db')
    except Exception as e:
        print(f"Error occurred while processing batch: {e}")

# Main function to process users in batches
def analyze_users():
    print("Starting user analysis process...")

    # Load the user database
    print("Loading user database from ./data/user_db.json...")
    user_db = load_user_db('./data/user_db.json')
    print(f"Loaded {len(user_db)} users from the database.")
    
    # Create batches of 20 users
    user_batches = [dict(list(user_db.items())[i:i + 20]) for i in range(0, len(user_db), 20)]  # Adjusted to preserve username-value pairs
    print(f"Created {len(user_batches)} batches of users.")
    
    # Log in to HuggingChat API
    retries = 5
    while retries > 0:
        try:
            print("Loading login details...")
            email = 'lunashoval@gmail.com'  # Replace with your email
            password = 'Luna5143!'  # Replace with your password
            sign = Login(email, password)
            cookies = sign.login(cookie_dir_path='./cookies/', save_cookies=True)
            chat_api = hugchat.ChatBot(cookies=cookies.get_dict())
            print(f"Login successful, {email}")
            break
        except Exception as e:
            retries -= 1
            print(f"Error logging in: {e}")
            if retries == 0:
                print("Failed to log in after multiple attempts.")
                return
            else:
                time.sleep(5)

    # Process each batch
    for batch_index, user_batch in enumerate(user_batches):
        print(f"Processing batch {batch_index + 1}...")
        get_analysis_for_batch(user_batch, chat_api)

# Run the analysis
if __name__ == "__main__":
    analyze_users()
