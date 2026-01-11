import os
import requests
from openai import OpenAI

# SECURITY UPDATE:
# We look for the key in the environment variables.
# If it's not found, we crash (which is good, it tells us something is wrong).
api_key = os.getenv("OPENAI_API_KEY")

# 2. GitHub Config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY") # e.g., "Sanket-Rotangar/pr-reviewer-bot"
PR_NUMBER = os.getenv("PR_NUMBER") # We will pass this in the YAML

if not api_key:
    raise ValueError("No OpenAI API Key found! Please set OPENAI_API_KEY in the environment.")

client = OpenAI(api_key=api_key)

# def review_code(file_path):
#     # 2. Read the file content
#     with open(file_path, 'r') as file:
#         code_content = file.read()

#     # 3. Create the Prompt (The "Instructions" for the AI)
#     # We tell it WHO it is and WHAT to do.
#     prompt = f"""
#     You are an expert Pull Request Reviewer. 
#     You will be provided with a Git Diff. 
#     Focus ONLY on the lines starting with '+' (added lines).
#     Do not review code that wasn't changed (lines starting with space).
    
#     Identify bugs and style issues in the added code.
    
#     Git Diff to review:
#     {code_content}
#     """

#     print("🤖 Analyzing code... please wait...")

#     # 4. Call the API
#     response = client.chat.completions.create(
#         model="gpt-4o-mini", # or "gpt-3.5-turbo"
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

    # 5. Extract and print the answer
    # feedback = response.choices[0].message.content
    # print("\n" + "="*30)
    # print("REVIEW REPORT")
    # print("="*30)
    # print(feedback)

def get_ai_review(diff_content):
    prompt = f"""
    You are an expert Pull Request Reviewer. 
    You will be provided with a Git Diff. 
    Focus ONLY on the lines starting with '+' (added lines).
    Do not review code that wasn't changed.
    
    Identify bugs, security risks, and style issues.
    Be concise and constructive.
    
    Git Diff:
    {diff_content}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def post_comment(comment_body):
    if not GITHUB_TOKEN or not REPO_NAME or not PR_NUMBER:
        print("Skipping comment posting (Missing Environment Variables)")
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment_body}
    
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 201:
        print("✅ Comment posted successfully!")
    else:
        print(f"❌ Failed to post comment: {resp.text}")


def main():
    # Read the diff
    try:
        with open("changes.diff", "r") as f:
            diff_content = f.read()
    except FileNotFoundError:
        print("No diff file found. Exiting.")
        return

    if not diff_content.strip():
        print("Diff is empty. Nothing to review.")
        return

    print("🤖 Analyzing changes...")
    review = get_ai_review(diff_content)
    
    print("📝 Posting comment to GitHub...")
    post_comment(review)

if __name__ == "__main__":
    main()