from dotenv import load_dotenv, find_dotenv, set_key

env_path = find_dotenv()
load_dotenv(env_path)

set_key(env_path, "GOOGLE_API_KEY", input("Enter your Google API key: ").strip())
set_key(env_path, "GOOGLE_CSE_ID", input(f"Enter your Google CSE ID: ").strip())
