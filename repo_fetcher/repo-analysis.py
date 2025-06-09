# %%
import json

with open("updated_repositories_data.json", "r") as f:
    repositories_data = json.load(f)
print("Number of repositories:", len(repositories_data))
from pprint import pprint

# %%
from tqdm import tqdm


# %%
def generate_prompt(r_name, llm_analysis):
    prompt = "You are an expoert project manager in a tech company. You can find out what a repository is all about given each file code description, author goal and author expertise. "
    prompt += "I will give you a repository name and each file names with their code description, author goal and author expertise. "
    prompt += "pu will compile everything and give me three things: \n1. What is being done in this repository. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise\n\n"
    prompt += f"The repository name is: {r_name} and the files with their descriptions are:\n"
    for i, file_data in enumerate(llm_analysis):
        prompt += f"\nFile {i+1}:\n"
        prompt += f"\n{file_data['description']}"
    prompt += "\n\n"
    prompt += "You should strictly follow following format to answer these questions:  \n1. What is being done in this repository. \n2. What the author is trying to achieve, and\n3. What can you tell about the author's expertise"
    prompt += "\n\njust replace <str> with your response. Don't use any other new_line character:\n"
    prompt += "repository_description:\n<str>\nauthor_goal:\n<str>\nauthor_expertise:\n<str>\n\n"
    prompt += "For each of the above keys, you should provide a string value in atmost two paragraphs.\n\n"
    return prompt

# %%
from ollama import ChatResponse, Client, chat

client = Client(
  host='http://scg014:11434',
)
def get_llm_analysis(prompt):
    response: ChatResponse = client.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']
# %%
for repo_name, repo_data in tqdm(repositories_data.items()):
    if "llm_analysis" in repo_data and repo_data["llm_analysis"]:
        prompt = generate_prompt(repo_name, repo_data["llm_analysis"])
        repo_data['llm_repo_analysis'] = get_llm_analysis(prompt)
        
with open("repositories_data.json", "w") as f:
    json.dump(repositories_data, f, indent=4)
# %%