from langchain_core.prompts import ChatPromptTemplate


def get_file_analyzer_prompt():
    chat_prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a technical recruiter who is an expert in analyzing code files from repositories. You will be given a file name, \
                    repository name and the file content. You will analyze this code then you will answer three questions. \n \
                    1. What is being done in this code file. \n \
                    2. What the developer is trying to achieve, and\n \
                    3. What can you tell about the author's expertise\n\n ",
            ),
            (
                "user",
                "The file name with actial file path is {filename} and it belongs to {repo_name} repository. \
             The file content is as follows:\n{file_content}\n\n ",
            ),
        ]
    )
    return chat_prompt


def get_repository_analyzer_prompt():
    chat_prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a technical recruiter who is an expert in analyzing code files from repositories. \
                    One LLM agent have aleady analyzed all the important files in the repository. Now you will summarize the findings of the repository. \
                    You will be given the repository name followed by complete analysis of each file done by another LLM agent. You will try to find answer to these questions:\n \
                    1. What is the repository about and what developer is trying to develop? \n \
                    2. What can you comment about the expertise of the developer?\n \
                    3. What can you comment on the developer's experience and which kind of role he will be fit for?\n\n \
                    Give a very detailed report which can be used to understand the repository and the developer's expertise.",
            ),
            (
                "user",
                "Here's the repository name: {repo_name}. Now, you will be provided by the analysis of each importatnt files\
         \n\n Please summarize the findings of the repository in not more than 3 paragraphs and be it should be high level. \n\n",
            ),
        ]
    )
    return chat_prompt


if __name__ == "__main__":
    filename = "example.py"
    repo_name = "example-repo"
    file_content = "def example_function():\n    print('Hello, World!')"

    prompt = get_file_analyzer_prompt()
    print(
        prompt.invoke(
            {"filename": filename, "repo_name": repo_name, "file_content": file_content}
        )
    )

    file_analysis = {
        "example.py": "This file contains a simple function that prints 'Hello, World!'. The developer is likely a beginner.",
        "another_file.py": "This file contains advanced algorithms and data structures. The developer is likely an expert.",
    }

    repo_prompt = get_repository_analyzer_prompt()
    print(
        repo_prompt.invoke(
            {
                "repo_name": repo_name,
                "file_analysis": "".join(
                    f"{filename}: \n\n {analysis} \n\n\n"
                    for filename, analysis in file_analysis.items()
                ),
            }
        )
    )
    # If you want to invoke the prompt again, use the correct dictionary syntax:
    repo_prompt.extend(
        [
            {
                "role": "ai",
                "content": "This is a test message.",
            },
            {
                "role": "ai",
                "content": "This is another test message.",
            },
        ]
    )
    print("#" * 50)
    print(
        repo_prompt.invoke(
            {
                "repo_name": repo_name,
                "file_analysis": "".join(
                    f"{filename}: \n\n {analysis} \n\n\n"
                    for filename, analysis in file_analysis.items()
                ),
            }
        )
    )
