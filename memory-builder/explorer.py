import requests
import json
import time
SLEEP_TIME=2

# Replace with your GitHub username and personal access token
with open('github-auth.json') as auth_file:
    auth_data = json.load(auth_file)
    GITHUB_USERNAME = auth_data['username']
    GITHUB_TOKEN = auth_data['access_token']

def get_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()

def get_commits(repo_name):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()

def get_commit_details(repo_name, commit_sha):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits/{commit_sha}'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    response.raise_for_status()
    return response.json()

def main():
    all_repositories_data = {}
    repositories = get_repositories(GITHUB_USERNAME)
    for repo in repositories:
        repo_name = repo['name']
        print(f'Repository: {repo_name}')
        repo_data = {
            'author': repo['owner']['login'],
            'is_fork': repo['fork'],
            'files': [],
            'unique_file_extensions': set(),
            'commits_by_user': []
        }
        commits = get_commits(repo_name)
        for commit in commits:
                # time.sleep(SLEEP_TIME)  # Pause for 1 second to avoid rate limit
                commit_sha = commit['sha']
                commit_details = get_commit_details(repo_name, commit_sha)
                repo_data['commits_by_user'].append({
                    'commithash': commit_sha,
                    'commit_message': commit_details['commit']['message']
                })
                if 'files' in commit_details:
                    for file in commit_details['files']:
                        repo_data['files'].append(file['filename'])
                        file_extension = file['filename'].split('.')[-1]
                        repo_data['unique_file_extensions'].add(file_extension)
        repo_data['unique_file_extensions'] = list(repo_data['unique_file_extensions'])
        all_repositories_data[repo_name] = repo_data

    with open('all_repositories_data.json', 'w') as json_file:
        json.dump(all_repositories_data, json_file, indent=4)

if __name__ == '__main__':
    main()