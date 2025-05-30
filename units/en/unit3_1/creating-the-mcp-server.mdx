# Creating the MCP Server

The MCP server is the heart of our Pull Request Agent. It provides the tools that our agent will use to interact with the Hugging Face Hub, specifically for reading and updating model repository tags. In this section, we'll build the server using FastMCP and the Hugging Face Hub Python SDK.

## Understanding the MCP Server Architecture

Our MCP server provides two essential tools:

| Tool | Description |
| --- | --- |
| `get_current_tags` | Retrieves existing tags from a model repository |
| `add_new_tag` | Adds a new tag to a repository via pull request |

These tools abstract the complexity of Hub API interactions and provide a clean interface for our agent to work with.

![MCP Server Tools](https://huggingface.co/datasets/mcp-course/images/resolve/main/unit3/architecture.png)

## Complete MCP Server Implementation

Let's create our `mcp_server.py` file step by step. We'll build this incrementally so you understand each component and how they work together.

### 1. Imports and Configuration

First, let's set up all the necessary imports and configuration. 

```python
#!/usr/bin/env python3
"""
Simplified MCP Server for HuggingFace Hub Tagging Operations using FastMCP
"""

import os
import json
from fastmcp import FastMCP
from huggingface_hub import HfApi, model_info, ModelCard, ModelCardData
from huggingface_hub.utils import HfHubHTTPError
from dotenv import load_dotenv

load_dotenv()
```

The imports above give us everything we need to build our MCP server. `FastMCP` provides the server framework, while the `huggingface_hub` imports give us the tools to interact with model repositories.

The `load_dotenv()` call automatically loads environment variables from a `.env` file, making it easy to manage secrets like API tokens during development.

<Tip>

If you're using uv, you can create a `.env` file in the root of the project and you won't need to use `load_dotenv()` if you use `uv run` to run the server.

</Tip>

Next, we'll configure our server with the necessary credentials and create the FastMCP instance:

```python
# Configuration
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize HF API client
hf_api = HfApi(token=HF_TOKEN) if HF_TOKEN else None

# Create the FastMCP server
mcp = FastMCP("hf-tagging-bot")
```

This configuration block does three important things:
1. Retrieves the Hugging Face token from environment variables
2. Creates an authenticated API client (only if a token is available)
3. Initializes our FastMCP server with a descriptive name

The conditional creation of `hf_api` ensures our server can start even without a token, which is useful for testing the basic structure.

### 2. Get Current Tags Tool

Now let's implement our first tool - `get_current_tags`. This tool retrieves the existing tags from a model repository:

```python
@mcp.tool()
def get_current_tags(repo_id: str) -> str:
    """Get current tags from a HuggingFace model repository"""
    print(f"🔧 get_current_tags called with repo_id: {repo_id}")

    if not hf_api:
        error_result = {"error": "HF token not configured"}
        json_str = json.dumps(error_result)
        print(f"❌ No HF API token - returning: {json_str}")
        return json_str
```

The function starts with validation - checking if we have an authenticated API client. Notice how we return JSON strings instead of Python objects. This is crucial for MCP communication.

<Tip>

All MCP tools must return strings, not Python objects. That's why we use `json.dumps()` to convert our results to JSON strings. This ensures reliable data exchange between the MCP server and client.

</Tip>

Let's continue with the main logic of the `get_current_tags` function:

```python
    try:
        print(f"📡 Fetching model info for: {repo_id}")
        info = model_info(repo_id=repo_id, token=HF_TOKEN)
        current_tags = info.tags if info.tags else []
        print(f"🏷️ Found {len(current_tags)} tags: {current_tags}")

        result = {
            "status": "success",
            "repo_id": repo_id,
            "current_tags": current_tags,
            "count": len(current_tags),
        }
        json_str = json.dumps(result)
        print(f"✅ get_current_tags returning: {json_str}")
        return json_str

    except Exception as e:
        print(f"❌ Error in get_current_tags: {str(e)}")
        error_result = {"status": "error", "repo_id": repo_id, "error": str(e)}
        json_str = json.dumps(error_result)
        print(f"❌ get_current_tags error returning: {json_str}")
        return json_str
```

This implementation follows a clear pattern:
1. **Fetch data** using the Hugging Face Hub API
2. **Process the response** to extract tag information
3. **Structure the result** in a consistent JSON format
4. **Handle errors gracefully** with detailed error messages

<Tip>

The extensive logging might seem overkill, but it helps with debugging and monitoring when the server is running. Remember, your application will autonomously reacting to events from the Hub, so you won't be able to see the logs in real time.

</Tip>

### 3. Add New Tag Tool

Now for the more complex tool - `add_new_tag`. This tool adds a new tag to a repository by creating a pull request. Let's start with the initial setup and validation:

```python
@mcp.tool()
def add_new_tag(repo_id: str, new_tag: str) -> str:
    """Add a new tag to a HuggingFace model repository via PR"""
    print(f"🔧 add_new_tag called with repo_id: {repo_id}, new_tag: {new_tag}")

    if not hf_api:
        error_result = {"error": "HF token not configured"}
        json_str = json.dumps(error_result)
        print(f"❌ No HF API token - returning: {json_str}")
        return json_str
```

Similar to our first tool, we start with validation. Now let's fetch the current repository state to check if the tag already exists:

```python
    try:
        # Get current model info and tags
        print(f"📡 Fetching current model info for: {repo_id}")
        info = model_info(repo_id=repo_id, token=HF_TOKEN)
        current_tags = info.tags if info.tags else []
        print(f"🏷️ Current tags: {current_tags}")

        # Check if tag already exists
        if new_tag in current_tags:
            print(f"⚠️ Tag '{new_tag}' already exists in {current_tags}")
            result = {
                "status": "already_exists",
                "repo_id": repo_id,
                "tag": new_tag,
                "message": f"Tag '{new_tag}' already exists",
            }
            json_str = json.dumps(result)
            print(f"🏷️ add_new_tag (already exists) returning: {json_str}")
            return json_str
```

This section demonstrates an important principle: **validate before acting**. We check if the tag already exists to avoid creating unnecessary pull requests.

<Tip>

Always check the current state before making changes. This prevents duplicate work and provides better user feedback. It's especially important when creating pull requests, as duplicate PRs can clutter the repository.

</Tip>

Next, we'll prepare the updated tag list and handle the model card:

```python
        # Add the new tag to existing tags
        updated_tags = current_tags + [new_tag]
        print(f"🆕 Will update tags from {current_tags} to {updated_tags}")

        # Create model card content with updated tags
        try:
            # Load existing model card
            print(f"📄 Loading existing model card...")
            card = ModelCard.load(repo_id, token=HF_TOKEN)
            if not hasattr(card, "data") or card.data is None:
                card.data = ModelCardData()
        except HfHubHTTPError:
            # Create new model card if none exists
            print(f"📄 Creating new model card (none exists)")
            card = ModelCard("")
            card.data = ModelCardData()

        # Update tags - create new ModelCardData with updated tags
        card_dict = card.data.to_dict()
        card_dict["tags"] = updated_tags
        card.data = ModelCardData(**card_dict)
```

This section handles model card management. We try to load an existing model card first, but create a new one if none exists. This ensures our tool works with any repository, even if it's empty.

The model card (`README.md`) contains the repository metadata, including tags. By updating the model card data and creating a pull request, we're following the standard Hugging Face workflow for metadata changes.

Now for the pull request creation - the main part of our tool:

```python
        # Create a pull request with the updated model card
        pr_title = f"Add '{new_tag}' tag"
        pr_description = f"""
## Add tag: {new_tag}

This PR adds the `{new_tag}` tag to the model repository.

**Changes:**
- Added `{new_tag}` to model tags
- Updated from {len(current_tags)} to {len(updated_tags)} tags

**Current tags:** {", ".join(current_tags) if current_tags else "None"}
**New tags:** {", ".join(updated_tags)}

🤖 This is a pull request created by the Hugging Face Hub Tagging Bot.
"""

        print(f"🚀 Creating PR with title: {pr_title}")
```

We create a detailed pull request description that explains what's changing and why. This transparency is crucial for repository maintainers who will review the PR.

<Tip>

Clear, detailed PR descriptions are essential for automated pull requests. They help repository maintainers understand what's happening and make informed decisions about whether to merge the changes.

Also, it's good practice to clearly state that the PR is created by an automated tool. This helps repository maintainers understand how to deal with the PR.

</Tip>

Finally, we create the commit and pull request:

```python
        # Create commit with updated model card using CommitOperationAdd
        from huggingface_hub import CommitOperationAdd

        commit_info = hf_api.create_commit(
            repo_id=repo_id,
            operations=[
                CommitOperationAdd(
                    path_in_repo="README.md", path_or_fileobj=str(card).encode("utf-8")
                )
            ],
            commit_message=pr_title,
            commit_description=pr_description,
            token=HF_TOKEN,
            create_pr=True,
        )

        # Extract PR URL from commit info
        pr_url_attr = commit_info.pr_url
        pr_url = pr_url_attr if hasattr(commit_info, "pr_url") else str(commit_info)

        print(f"✅ PR created successfully! URL: {pr_url}")

        result = {
            "status": "success",
            "repo_id": repo_id,
            "tag": new_tag,
            "pr_url": pr_url,
            "previous_tags": current_tags,
            "new_tags": updated_tags,
            "message": f"Created PR to add tag '{new_tag}'",
        }
        json_str = json.dumps(result)
        print(f"✅ add_new_tag success returning: {json_str}")
        return json_str
```

The `create_commit` function with `create_pr=True` is the key to our automation. It creates a commit with the updated `README.md` file and automatically opens a pull request for review.

Don't forget the error handling for this complex operation:

```python
    except Exception as e:
        print(f"❌ Error in add_new_tag: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

        error_result = {
            "status": "error",
            "repo_id": repo_id,
            "tag": new_tag,
            "error": str(e),
        }
        json_str = json.dumps(error_result)
        print(f"❌ add_new_tag error returning: {json_str}")
        return json_str
```

The comprehensive error handling includes the full traceback, which is invaluable for debugging when things go wrong.

Emojis in log messages might seem silly, but they make scanning logs much faster. 🔧 for function calls, 📡 for API requests, ✅ for success, and ❌ for errors create visual patterns that help you quickly find what you're looking for.

<Tip>

Whilst building this application, it's easy to accidentally create an infinite loop of PRs. This is because the `create_commit` function with `create_pr=True` will create a PR for every commit. If the PR is not merged, the `create_commit` function will be called again, and again, and again...

We've added checks to prevent this, but it's something to be aware of.

</Tip>

## Next Steps

Now that we have our MCP server implemented with robust tagging tools, we need to:

1. **Create the MCP Client** - Build the interface between our agent and MCP server
2. **Implement Webhook Handling** - Listen for Hub discussion events
3. **Integrate Agent Logic** - Connect webhooks with MCP tool calls
4. **Test the Complete System** - Validate end-to-end functionality

In the next section, we'll create the MCP client that will allow our webhook handler to interact with these tools intelligently.

<Tip>

The MCP server runs as a separate process from your main application. This isolation provides better error handling and allows the server to be reused by multiple clients or applications.

</Tip> 