from langchain_core.prompts import ChatPromptTemplate

def get_file_analyzer_prompt():
    chat_prompt = ChatPromptTemplate([
        ("system", "You are a technical recruiter who is an expert in analyzing code files from repositories. You will be given a file name, \
         repository name and the file content. You will analyze this code then you will answer three questions. \n \
         1. What is being done in this code file. \n \
         2. What the developer is trying to achieve, and\n \
         3. What can you tell about the author's expertise\n\n "),
        ("user", "The file name with actial file path is {filename} and it belongs to {repo_name} repository. \
         The file content is as follows:\n{file_content}\n\n ")
    ])
    return chat_prompt


def get_repository_analyzer_prompt():
    chat_prompt = ChatPromptTemplate([
        ("system", "You are a technical recruiter who is an expert in analyzing code files from repositories. \
         You have already analyzed all the important files in the repository. Now you will summarize the findings of the repository. \
         You will be given the repository name followed by a list of files with your complete analysis. You will try to find answer to these questions:\n \
         1. What is the repository about and what developer is trying to develop? \n \
         2. What can you comment about the expertise of the developer?"),
        ("user", "Here's the repository name: {repo_name}. and the file names with your complete analysis is as follows:\n {file_analysis} \
         \n\n Please summarize the findings of the repository in not more than 3 paragraphs and be it should be high level. \n\n")
    ])
    return chat_prompt


if __name__ == "__main__":
    filename = "example.py"
    repo_name = "example-repo"
    file_content = "def example_function():\n    print('Hello, World!')"
    
    prompt = get_file_analyzer_prompt()
    print(prompt.invoke({"filename": filename, "repo_name": repo_name, "file_content": file_content}))
    
    file_analysis = {
        "example.py": "This file contains a simple function that prints 'Hello, World!'. The developer is likely a beginner.",
        "another_file.py": "This file contains advanced algorithms and data structures. The developer is likely an expert."
    }
    
    repo_prompt = get_repository_analyzer_prompt()
    print(repo_prompt.invoke({"repo_name": repo_name, "file_analysis": "".join(f"{filename}: \n\n {analysis} \n\n\n" for filename, analysis in file_analysis.items()) }))
