import os, requests, base64
import yfinance as yf
import pandas as pd
from datetime import datetime

# Step 1: Fetch today's date in the format day/month/year
today_date = datetime.now().strftime('%Y-%m-%d')

# Step 2: Fetch historical data for QLD (NASDAQ x2)
# Adjust the date range as needed
data = yf.download('QLD', start='2019-07-26', end=today_date)

# Convert the index (dates) to the desired format (day/month/year)
data.index = data.index.strftime('%d/%m/%Y')

# Step 3: Save the data to a CSV file
csv_filename = 'qld_stock_data.csv'
data.to_csv(csv_filename)

# Step 4: Prepare the CSV data for pushing to GitHub
# Update these variables with your GitHub repository details and token
github_token = os.getenv('GITHUB_TOKEN')
repo = 'awakzdev/test'
branch = 'main'
file_path_in_repo = 'qld_stock_data.csv'

# Step 5: Get the current file's SHA (needed to update a file in the repository)
url = f'https://api.github.com/repos/{repo}/contents/{file_path_in_repo}'
headers = {'Authorization': f'token {github_token}'}
response = requests.get(url, headers=headers)
response_json = response.json()

# Extract the SHA of the file
sha = response_json['sha']

# Step 6: Read the new CSV file and encode it in base64
with open(csv_filename, 'rb') as f:
    content = f.read()
content_base64 = base64.b64encode(content).decode('utf-8')

# Step 7: Create the payload for the GitHub API request
commit_message = 'Update QLD stock data'
data = {
    'message': commit_message,
    'content': content_base64,
    'branch': branch,
    'sha': sha  # Required to update an existing file
}

# Step 8: Push the updated file to the repository
response = requests.put(url, headers=headers, json=data)

# Check if the file was updated successfully
if response.status_code == 200 or response.status_code == 201:
    print('File updated successfully in the repository.')
else:
    print('Failed to update the file in the repository.')
    print('Response:', response.json())
