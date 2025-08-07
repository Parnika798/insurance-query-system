# main.py

import subprocess
import os
from Backend.parsepolicy import process_policy_file

# ----------------- Config -----------------
project_dir = os.path.dirname(os.path.abspath(__file__))  # Current project directory
policy_path = os.path.join(project_dir, "Test Sample.pdf")  # Input PDF in same folder
chunk_output_path = os.path.join(project_dir, "chunked_clauses.csv")  # Output path
python_path = "python"  # or full path to Python executable if needed

# ----------------- Step 1: Parse -----------------
print("📄 Parsing and chunking policy...")
df = process_policy_file(policy_path)
df.to_csv(chunk_output_path, index=False)
print(f"✅ Chunked clauses saved to {chunk_output_path}\n")

# ----------------- Step 2: Embed & Store -----------------
print("🔗 Running embedandstore.py ...\n")
try:
    embed_script_path = os.path.join(project_dir, "embedandstore.py")
    subprocess.run([python_path, embed_script_path, chunk_output_path], check=True)

except subprocess.CalledProcessError as e:
    print(f"⚠️ Error in embedandstore.py:\n {e}")
