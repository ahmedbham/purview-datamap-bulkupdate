from azure.identity import DefaultAzureCredential
import requests
import csv
import argparse
import sys

# Check if the required arguments are provided
if len(sys.argv) < 3:
    print("Usage: python get_assets_for_one_collection.py <purviewAccountName> <collectionId>")
    sys.exit(1)

# Get the purviewAccountName and collectionId from the command line arguments
purview_account_name = sys.argv[1]
collection_id = sys.argv[2]

# Acquire a credential object
credential = DefaultAzureCredential()

# Get the access token
token = credential.get_token("https://purview.azure.net/.default")

# Set the headers with the access token
headers = {
    "Authorization": f"Bearer {token.token}"
}

# Define the endpoint for the POST request
post_endpoint = f"https://{purview_account_name}.purview.azure.com/datamap/api/search/query?api-version=2023-09-01"

# Loop through each name and make the POST request
post_data = {
    "collectionId": collection_id
}
post_response = requests.post(post_endpoint, headers=headers, json=post_data)

# Check if the POST request was successful
if post_response.status_code == 200:
    print("Successfully posted data")
    response_json = post_response.json()
    
    # Extract the "id", "entityType", and "name" fields from each item in the response
    ids = [item['id'] for item in response_json.get('value', [])]
    entityTypes = [item['entityType'] for item in response_json.get('value', [])]
    names = [item['name'] for item in response_json.get('value', [])]
    print("Extracted IDs:", ids)
    print("Extracted entityTypes:", entityTypes)
    print("Extracted names:", names)
    
    # Append the extracted data to the existing CSV file
    with open('DataMap-Attrib-Upload_file_1.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for id, name, entityType in zip(ids, names, entityTypes):
            writer.writerow([id, name, entityType])  # Write each row
else:
    print(f"Failed to post data: {post_response.status_code}")
    print("Response JSON:", post_response.json())
