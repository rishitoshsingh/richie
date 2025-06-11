from langchain_core.prompts import ChatPromptTemplate


def get_file_analyzer_prompt():
    chat_prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a technical recruiter who is an expert in analyzing code files from repositories. You will be given a file name, \
                    repository name and the file content. You will analyze this code and your analysis shoulld be able to answer three questions. \n \
                    1. What is being done in this code file. \n \
                    2. What the developer is trying to achieve, and\n \
                    3. What can you tell about the author's expertise, the frameworks, libraries or tech stack he is experienced with\n \
                Whatever you will say will be used to summarize the project repository, so try to include all important messages\n \
                Avoid using technical terms, just think that main audience of this will not have just a little bit of \
                technical knowledge, so avoid technical jargons\n ",
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
                "You are an expert in giving detail report of project repositories using the individual code file summaries. \
                    One LLM agent have aleady analyzed all the important files in the project repository. Now you will report the findings of the repository. \
                    You will be given the repository name followed by complete analysis of each file done by another LLM agent. \
                    From your report anybody should be able to answer these question:\n \
                        1. What is the repository about and what developer is trying to develop? \n \
                        2. What can you comment about the expertise of the developer?\n \
                        3. What can you comment on the developer's experience and which kind of role he will be fit for?\n \
                        3. What technology stack, libraries or frameworks the developer is experienced in?\n\n \
                    Give a very detailed report using paragraphs, no bullet points which can be used to understand the repository and the developer's expertise and don't include anything negative about the developer",
            ),
            (
                "user",
                "Here's the repository name: {repo_name}. Following are the analysis of each code files in the project repository \n {docs} \n\n",
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
