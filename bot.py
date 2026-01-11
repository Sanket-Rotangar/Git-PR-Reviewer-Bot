import os
from openai import OpenAI

# SECURITY UPDATE:
# We look for the key in the environment variables.
# If it's not found, we crash (which is good, it tells us something is wrong).
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No OpenAI API Key found! Please set OPENAI_API_KEY in the environment.")

client = OpenAI(api_key=api_key)

def review_code(file_path):
    # 2. Read the file content
    with open(file_path, 'r') as file:
        code_content = file.read()

    # 3. Create the Prompt (The "Instructions" for the AI)
    # We tell it WHO it is and WHAT to do.
    prompt = f"""
    You are an expert Pull Request Reviewer. 
    You will be provided with a Git Diff. 
    Focus ONLY on the lines starting with '+' (added lines).
    Do not review code that wasn't changed (lines starting with space).
    
    Identify bugs and style issues in the added code.
    
    Git Diff to review:
    {code_content}
    """

    print("🤖 Analyzing code... please wait...")

    # 4. Call the API
    response = client.chat.completions.create(
        model="gpt-4o-mini", # or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # 5. Extract and print the answer
    feedback = response.choices[0].message.content
    print("\n" + "="*30)
    print("REVIEW REPORT")
    print("="*30)
    print(feedback)

if __name__ == "__main__":
    # Point the bot to our bad file
    review_code("changes.diff")