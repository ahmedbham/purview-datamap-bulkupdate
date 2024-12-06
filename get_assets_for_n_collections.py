from azure.identity import DefaultAzureCredential
import requests
import csv
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process purview account name.')

# Add the purview_account_name argument
parser.add_argument('purview_account_name', type=str, help='The name of the Purview account')

# Parse the arguments
args = parser.parse_args()

# Check if purview_account_name is provided
if not args.purview_account_name:
    parser.error("Purview Account Name is required. Please provide it as a command line argument.")

# Use the purview_account_name argument
purview_account_name = args.purview_account_name

# Construct the URL for Collections endpoint
url = f"https://{purview_account_name}.purview.azure.com/collections?api-version=2019-11-01-preview"

# Acquire a credential object
credential = DefaultAzureCredential()

# Get the access token
token = credential.get_token("https://purview.azure.net/.default")

# Set the headers with the access token
headers = {
    "Authorization": f"Bearer {token.token}"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Access the list of items
    items = data.get('value', [])
    
    # Extract the list of "name" values
    names = [item['name'] for item in items]
    print("Names:", names)
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Define the endpoint for the POST request
post_endpoint = f"https://{purview_account_name}.purview.azure.com/datamap/api/search/query?api-version=2023-09-01"

# Loop through each name and make the POST request
for name in names:
    post_data = {
        "collectionId": name
    }
    post_response = requests.post(post_endpoint, headers=headers, json=post_data)
    
    # Check if the POST request was successful
    if post_response.status_code == 200:
        print(f"Successfully posted data for {name}")
        response_json = post_response.json()
        
        # Extract the "id", "entityType", and "name" fields from each item in the response
        ids = [item['id'] for item in response_json.get('value', [])]
        entityTypes = [item['entityType'] for item in response_json.get('value', [])]
        names = [item['name'] for item in response_json.get('value', [])]
        print("Extracted IDs:", ids)
        print("Extracted entityTypes:", entityTypes)
        print("Extracted names:", names)
        
        # Loop through names up to 5 elements and write data to separate CSV files
        for index, (id, name, entityType) in enumerate(zip(ids, names, entityTypes)):
            if index >= 5:
                break
            file_name = f"DataMap-Attrib-Upload_file_{index + 1}.csv"
            with open(file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id, name, entityType])  # Write each row
    else:
        print(f"Failed to post data for {name}: {post_response.status_code}")
        print("Response JSON:", post_response.json())
