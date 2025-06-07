# richie

## Setup

1. Create a fine-grained GitHub API token with all repository access with "Contents" and "Metadata" set to Read-Only.
2. Create a file `auth/github-auth.json` with this GitHub Api token as:
```json
{
    "username": "your-github-username",
    "access_token": "your-personal-access-token"
}
```
3. Create a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
4. Create a file `auth/gemini.json` with this API key as:

```json
{
    "api-key": "gemini-api-key"
}
```

## Steps
1. Install required libraries
2. Generate GitHub repository data using:
```terminal
$ python repo_fetcher/explorer.py
```
