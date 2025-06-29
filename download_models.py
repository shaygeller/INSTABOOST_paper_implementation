import os
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

# Proxy and SSL settings (if needed)
os.environ['CURL_CA_BUNDLE'] = ''

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")

# login to Hugging Face Hub
if hf_token:
    from huggingface_hub import login
    print("HUGGINGFACE_TOKEN found in environment variables. Logging in...")
    login(token=hf_token, add_to_git_credential=False)
    print("Logged in to Hugging Face Hub successfully.")
else:
    print("HUGGINGFACE_TOKEN not found in environment variables. Skipping login.")

models = [
    # Big Models (~7B+)
    "meta-llama/Llama-3.2-1B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen1.5-7B-Chat",
    "microsoft/Phi-3-mini-4k-instruct",
    
    # Medium Models (<=1B)
    "Qwen/Qwen2.5-0.5B-Instruct",

]

for repo_id in models:
    print(f"Downloading {repo_id}...")
    try:
        path = snapshot_download(
            repo_id=repo_id,
            token=hf_token,
            resume_download=True,
            max_workers=8,
        )
        print(f"✓ Downloaded {repo_id} at {path}")
    except Exception as e:
        print(f"❌ Error downloading {repo_id}: {e}")
