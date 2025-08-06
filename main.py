# main.py

import subprocess
import os
from parsepolicy import process_policy_file

# ----------------- Config -----------------
policy_path = r"C:\Users\parni\Projects\Insurance Policy\Test Sample.pdf"
chunk_output_path = r"C:\Users\parni\Projects\Insurance Policy\chunked_clauses.csv"
python_path = "python"  # or full path to Python executable if needed

# ----------------- Step 1: Parse -----------------
print("📄 Parsing and chunking policy...")
df = process_policy_file(policy_path)
df.to_csv(chunk_output_path, index=False)
print(f"✅ Chunked clauses saved to {chunk_output_path}\n")

# ----------------- Step 2: Embed & Store -----------------
print("🔗 Running embed&store.py ...\n")
try:
    project_dir = os.path.dirname(os.path.abspath(__file__))  # ✅ This was missing
    embed_script_path = os.path.join(project_dir, "embedandstore.py")
    subprocess.run([python_path, embed_script_path, chunk_output_path], check=True)

except subprocess.CalledProcessError as e:
    print(f"⚠️ Error in embed&store.py:\n {e}")

