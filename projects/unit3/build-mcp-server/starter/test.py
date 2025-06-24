from server import analyze_file_changes, get_pr_templates
import asyncio
import json

result = asyncio.run(analyze_file_changes())
diff = json.loads(result)["diff"]
changed_files = json.loads(result)["changed_files"]

print(diff)
print(changed_files)

result = asyncio.run(get_pr_templates())
templates = json.loads(result)["templates"]
print(templates)