import base64
import os

import requests

# Store as environment variable for future Repo>Settings>Secrets & Variables>Actions>Repository Secret
auth_key = os.environ.get('API_SECRET')
print(f'AUTH KEY: {auth_key}')

# Get all repos in organization
url = "https://api.github.com/orgs/Sierra7-Organization-Sandbox/repos"

# Request headers
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {auth_key}",
    "X-GitHub-Api-Version":  "2022-11-28"
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    print("Request for repositories made successfully.")
    print(response.text)
else:
    print(f"Failed request. Status code: {response.status_code}")
    print(response.text)

repo_list = []

for item in response.json():
    repo_list.append(item['name'])

for repo in repo_list:
    # Retrieve the current content of the README file
    readme_url = f'https://api.github.com/repos/Sierra7-Organization-Sandbox/{repo}/contents/README.md'

    response = requests.get(readme_url, headers=headers)
    content = response.json()['content']
    print(response.json())

    readme_text = base64.b64decode(content).decode('utf-8')

    if 'EvanF_6564' not in readme_text:
        readme_text += ("\n\n``` diff\n- This is copied README INFO from across all repositories in Sierra7-Organization-Sandbox - EvanF_6564**\n```")

    update_readme_url = f'https://api.github.com/repos/Sierra7-Organization-Sandbox/{repo}/contents/README.md'

    new_content_encoded = base64.b64encode(readme_text.encode('utf-8')).decode('utf-8')

    print(response.json()['sha'])

    update_data = {
        'message': 'Update README.md',
        'content': new_content_encoded,
        'sha': response.json()['sha']  # SHA of current README from response
    }

    response = requests.put(readme_url, headers=headers, json=update_data)
    if response.status_code == 200:
        print("README.md updated successfully!")
    else:
        print("Failed to update README.md:", response.text)