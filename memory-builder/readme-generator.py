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
                # code_and_output.append((f"CODE: {code}", f"OUTPUT: {''.join(text_outputs)}"))
                code_and_output.append(code)
            except KeyError:
                continue
            except Exception:
                continue
    # return code_and_output
    return "\n".join(code_and_output)
# %%
def generate_prompt(r_name, file_name, file_content):
    if file_name.endswith('.py'):
        prompt = "You are expert in finding what a piece of code does, using repository name, and file content. "
        prompt += "I will give you a file name, repository name and the file content. "
        prompt += "You will analyze this python code file then you will answer three questions. \n1. What is being done in this code file. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    if file_name.endswith('.ipynb'):
        prompt = "You are expert in finding what a piece of code does in jupyter notebook, using repository name, and code from notebook. "
        prompt += "I will give you a file name, repository name and then the code from notebook"
        prompt += "You will analyze this code then you will answer three questions. \n1. What is being done in the notebook. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nList of Code Cells:\n{file_content}"
    if file_name.endswith('.cpp') or file_name.endswith('.h') or file_name.endswith('.c'):
        prompt = "You are expert in finding what a piece of code does in C/C++ files, using repository name, and file content. "
        prompt += "I will give you a file name, repository name and the file content. You will give me what does this code file do, what the author is trying to achieve, and what can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    if file_name.endswith('html') or file_name.endswith('htm'):
        prompt = "You are expert in analyzing HTML files, using repository name, and the html file content. "
        prompt += "I will give you a file name, repository name and the file content. "
        prompt += "You will analyze this HTML file then you will answer three questions. \n1. What is being done in this code file. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    if file_name.endswith('.css'):
        prompt = "You are expert in analyzing CSS files, using repository name, and css file content. "
        prompt += "I will give you a file name, repository name and the css file content. "
        prompt += "You will analyze this css code file then you will answer three questions. \n1. What is being done in this code file. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    if file_name.endswith('.js'):
        prompt = "You are expert in finding what a piece of code does in JavaScript files, using repository name, and file content. "
        prompt += "I will give you a file name, repository name and the js file content. "
        prompt += "You will analyze this js code file then you will answer three questions. \n1. What is being done in this code file. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    if file_name.endswith('.kt'):
        prompt = "You are expert in finding what a piece of code does in Kotlin files and what kind of app the user is trying to make, using repository name, and file content. "
        prompt += "I will give you a file name, repository name and the kotlin file content. "
        prompt += "You will analyze this kotlin code file then you will answer three questions. \n1. What is being done in this code file. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
        prompt += "You should strictly follow following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"    
        prompt += "code_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
        prompt += "For each of the above keys, you should provide a string value in just one paragraph.\n\n"
        prompt += f"Repository Name: {r_name}\n\nFile Name: {file_name}\n\nFile Content:\n{file_content}"
    return prompt

# %%
from ollama import chat
from ollama import ChatResponse
from ollama import Client
client = Client(
  host='http://scg004:11434',
)
def get_llm_description(prompt):
    response: ChatResponse = client.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']
# %%
for repo_name, repo_data in tqdm(repositories_data.items()):
    if not repo_data.get("is_fork", True):
        files = get_files(repo_name)
        descriptions = []
        for file_data in files:
            if file_data['name'].endswith(('.py', '.cpp', '.c', '.h', '.kt', '.html', '.htm', '.css', '.js')):
                raw_url = file_data['download_url']
                try:
                    raw_content = requests.get(raw_url).text
                    prompt = generate_prompt(repo_name, file_data['name'], raw_content)
                    description = get_llm_description(prompt)
                    # print("Repostrory Name:", repo_name)
                    # print("File Name:", file_data['name'])
                    # pprint(description)
                    descriptions.append({'file_name': file_data['name'], 'description': description})
                except Exception as e:
                    print(e)
                    print(f"Error in {repo_name}/{file_data['name']}")
                    continue
            if file_data['name'].endswith('.ipynb'):
                raw_url = file_data['download_url']
                try:
                    raw_content = requests.get(raw_url).json()
                    raw_content = extract_code_and_output(raw_content)
                    prompt = generate_prompt(repo_name, file_data['name'], raw_content)
                    description = get_llm_description(prompt)
                    # print("Repostrory Name:", repo_name)
                    # print("File Name:", file_data['name'])
                    # pprint(description)
                    descriptions.append({'file_name': file_data['name'], 'description': description})
                except Exception as e:
                    print(e)
                    print(f"Error in {repo_name}/{file_data['name']}")
                    continue
        repo_data['llm_analysis'] = descriptions
        
with open("updated_repositories_data.json", "w") as f:
    json.dump(repositories_data, f, indent=4)
# %%