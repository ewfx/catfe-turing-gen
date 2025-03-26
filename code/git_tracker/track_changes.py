import subprocess

def check_latest_commit():
    result = subprocess.run(["git", "diff", "HEAD~1", "--name-only"], capture_output=True, text=True)
    modified_files = result.stdout.strip().split("\n")
    
    if any(file.startswith("backend/") or file.startswith("frontend/") for file in modified_files):
        print("Changes detected! Regenerating BDD scenarios...")
        subprocess.run(["python", "bdd_generator/ollama_model.py"])
        subprocess.run(["python", "bdd_tester/test_runner.py"])
    else:
        print("No major changes detected.")

if __name__ == "__main__":
    check_latest_commit()
