# %%
import json
with open("all_repositories_data.json", "r") as f:
    repositories_data = json.load(f)
print("Number of repositories:", len(repositories_data))
# %%
import requests
from tqdm import tqdm
from pprint import pprint
# Replace with your GitHub username and personal access token
with open('github-auth.json') as auth_file:
    auth_data = json.load(auth_file)
    GITHUB_USERNAME = auth_data['username']
    GITHUB_TOKEN = auth_data['access_token']
# %%
def get_files(repo_name):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()
# %%
def extract_code_and_output(notebook_json):
    code_and_output = []
    for cell in notebook_json['cells']:
        if cell['cell_type'] == 'code':
            try:
                code = ''.join(cell['source'])
                outputs = cell.get('outputs', [])
                text_outputs = [
                    ''.join(output['text']) if isinstance(output['text'], list) else output['text']
                    for output in outputs if output['output_type'] == 'stream'
                ]
                code_and_output.append((f"CODE: {code}", f"OUTPUT: {''.join(text_outputs)}"))
            except KeyError:
                continue
            except Exception:
                continue
    return code_and_output
# %%
def generate_prompt(r_name, file_name, file_content):
    prompt = "You are expert in in finding what a piece of code does, using repository name, and file content. "
    prompt += "I will give you a file name, repository name and the file content. You will give me what does this code file do, what the author is trying to achieve, and what can you tell about the author like using this code file, what is the author's expertise, etc.\n\n"
    prompt += "You should answer this question in python dicrtionary format. You should strictly follow following format, just replace <str> with your response. Don't use any other new_line character:\n"    
    prompt +=  "{'code_description': <str> \n 'author_goal': <str> \n 'author_expertise': <str> }\n\n"
    prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
    prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    return prompt

# %%
from ollama import chat
from ollama import ChatResponse
def get_llm_description(prompt):
    response: ChatResponse = chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']
# %%
import ast
import re
def extract_llm_response(response):
    msg = response
    msg = " ".join(msg.split())
    pattern = r"({.*})"
    match = re.search(pattern, msg, re.DOTALL)
    if match:
        extracted_dict = match.group(1)
        extracted_dict = ast.literal_eval(extracted_dict)
        return extracted_dict
    else:
        return "Failed to extract response."
# %%
for repo_name, repo_data in tqdm(repositories_data.items()):
    if not repo_data.get("is_fork", True):
        files = get_files(repo_name)
        for file_data in files:
            if file_data['name'].endswith(('.py', '.cpp', '.c', '.h', '.kt', '.html', '.htm', '.css', '.js')):
                raw_url = file_data['download_url']
                raw_content = requests.get(raw_url).text
                print(f"Repository: {repo_name}")
                print(f"File: {file_data['name']}")
                prompt = generate_prompt(repo_name, file_data['name'], raw_content)
                description = get_llm_description(prompt)
                response = extract_llm_response(description)
                repo_data['llm_analysis'] = response
            if file_data['name'].endswith('.ipynb'):
                raw_url = file_data['download_url']
                raw_content = requests.get(raw_url).json()
                raw_content = extract_code_and_output(raw_content)
                print(f"Repository: {repo_name}")
                print(f"File: {file_data['name']}")
                prompt = generate_prompt(repo_name, file_data['name'], raw_content)
                response = extract_llm_response(description)
                repo_data['llm_analysis'] = response
            
with open("updated_repositories_data.json", "w") as f:
    json.dump(repositories_data, f, indent=4)
# %%