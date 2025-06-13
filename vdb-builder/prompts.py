from langchain_core.prompts import ChatPromptTemplate


def get_file_analyzer_prompt():
    chat_prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a technical recruiter who is an expert in analyzing code files from repositories. You will be given a file name, \
                    repository name and the file content. You will analyze this code and your analysis should be able to answer three questions. \n \
                    1. What is being done in this code file. \n \
                    2. What the developer is trying to achieve, and\n \
                    3. What can you tell about the author's expertise, the frameworks, libraries or tech stack he is experienced with\n \
                    4. Are PRs clear, well-documented, and follow a pattern? If yes, Are they merged through reviews or self-merged? If yes, How does the candidate respond to feedback?\n \
                    5. Are they proactive in opening, labeling, or commenting on issues? If yes, Any signs of task ownership, triage, or sprint-like workflows?\n \
                    6. Is the candidate working solo or contributing to shared codebases? If yes, Do they respect the codebase structure and conventions? \n \
                    7. For commits, Are they clear, helpful, and follow a standard (`feat:`, `fix:`, etc.)? If yes, Do they reveal thoughtful iteration, or careless dumping?\n \
                    8. If there is a README.md file, Do they consider others when writing documentation? If yes, Is their language accessible and professional?\n \
                    9. If there are discussions in Issues/PRs, Are they constructive, respectful, and open to discussion? Do they ask clarifying questions or just push changes?\n \
                    10. Regarding code consistency, Do they conform to project style and structure, or go rogue? Do they write code that others can easily understand and maintain?\n \
                    11. Are there signs they learned something new and applied it (e.g., “Refactored X for clarity after review”)? Do they reference best practices or standards?\n \
                    12. Do they go beyond “just coding” — e.g., adding test coverage, fixing bugs they didn’t cause?\n \
                    13. Are PRs bite-sized and reviewable, or huge and chaotic? Do they leave helpful comments for reviewers?\n \
                    14. Are there any red flags in repo like listed below:\n \
                        14.1 Overly vague or empty commit messages (`fix`, `update`, `wip`)\n \
                        14.2 No evidence of collaboration or feedback cycles\n \
                        14.3 Aggressive or dismissive tone in issues/discussions\n \
                        14.4 Poor documentation or completely absent README\n \
                        14.5 Large, monolithic PRs with no review comments\n \
                    15. Is the repo having any of below technical skills/expertise?\n \
                        15.1 Language fluency: Deep understanding of chosen tech stack.\n \
                        15.2 Framework/library use: Good judgment in tool selection and integration.\n \
                        15.3 Testing discipline: Are tests present? What kind (unit, integration)?\n \
                        15.4 Build tooling: Use of linters, formatters, and build scripts.\n \
                        15.5 Performance awareness: Any evidence of optimization or profiling?\n\n \
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
                        4. What technology stack, libraries or frameworks the developer is experienced in?\n \
                        5. Is the project solving a real problem or exploring a meaningful idea?\n \
                        6. What can you comment on Project Architecture of the repository by leveraging below list of pointers?\n \
                            6.1 Folder structure: Organized, scalable project layout.\n \
                            6.2 Modularity: Code is decoupled and reusable.\n \
                            6.3 Configuration management: Use of `.env`, config files, constants, etc.\n \
                            6.4 Dependency management: Uses package managers and avoids unnecessary bloat.\n\n \
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
