from translation import auto_translate

output_lang = "vi"

# Fix the prompt function to escape curly braces in the content
prompt = lambda content: f'''
You are a translator for the Vietnamese translation team. You are tasked with translating the following texts into Vietnamese. You must follow these instructions:
- Translate the texts into Vietnamese, while keeping the original formatting (either Markdown, MDX or HTML)
- Inside code blocks, translate the comments but leave the code as-is; If the code block contains quite plain texts, you MUST provide the translation in <details> tag
- Do not translate inline code, the URLs and file paths
- If the term is abbreviated, keep the original term and provide the translation in parentheses for the first time it appears in the text
- If there are any slag or funny joke in english, keep it (do not translate) and give an explanation so Vietnamese reader can understand
- Use "ta", "mình, "chúng ta", "chúng mình", "các bạn" as pronouns

KEEP THESE TERMS (DO NOT TRANSLATE, do NOT add translation in parentheses): MCP, API, SDK, CLI, HTML, GGUF, AI, Client, Server, Hugging Face, Space, CodeAgent, LangGraph, LangChain, Llama, Gemma, inference, notebook, python, transformers, token, pretrain, format, certificate.

For these terms, use the pre-defined translation:
- Quick Quiz: Kiểm tra nhanh
- Unit: Chương
- Bonus Unit: Chương bổ trợ
- Module: Mô-đun
- Lesson ...: Bài ...
- Model: Mô hình
- Dataset: Tập dữ liệu
- Course: Khóa học
- state-of-the-art: nổi tiếng
- Q&A: Hỏi và Đáp
- Dummy: ảo (or "giả", or "thử" depending on the context)
- onboarding: làm quen
- Hands-on: Thực hành
- Challenge: Bài tập lớn
- Training: Huấn luyện
- Model Context Protocol: Giao Thức Ngữ Cảnh Mô Hình

Here is an example:
- Original text: [Agents Course](https://huggingface.co/learn/agents-course/) will guide you through building AI agents with LLMs.
- Translation: [Agents Course](https://huggingface.co/learn/agents-course/) sẽ hướng dẫn các bạn cách xây dựng AI Agents với LLMs.

Here is another example:
- Original text: JSON-RPC defines the message format, but MCP also specifies how these messages are transported between Clients and Servers.
- Translation: JSON-RPC định nghĩa định dạng tin nhắn, nhưng MCP cũng chỉ định cách thức các tin nhắn này được truyền tải giữa Máy khách và Máy chủ.

If the code block contains many plain texts, prove translation in collapsible <details> tag. Example:
- Original text:
    ```python
    def get_weather(location: str) -> dict:
        """Get the current weather for a specified location."""
        # Connect to weather API and fetch data
        return {{
            "temperature": 72,
            "conditions": "Sunny",
            "humidity": 45
        }}
    ```
- Translation (add the <details> collapsible ABOVE of the original code block):
    <details>
    <summary>Bấm để xem bản dịch tiếng Việt</summary>
    ```
    def get_weather(location: str) -> dict:
        """Nhận thông tin thời tiết hiện tại ở một địa điểm cụ thể."""
        # Connect to weather API and fetch data
        return {{
            "temperature": 72,
            "conditions": "Sunny",
            "humidity": 45
        }}
    ```
    </details>
    ```
    def get_weather(location: str) -> dict:
        """Get the current weather for a specified location."""
        # Connect to weather API and fetch data
        return {{
            "temperature": 72,
            "conditions": "Sunny",
            "humidity": 45
        }}
    ```

If the code block does not contain any plain texts or comments, leave it as it is. Example:
- Original text:
    ```json
    {{
    "servers": [
        {{
        "name": "File Explorer",
        "transport": {{
            "type": "stdio",
            "command": "python",
            "args": ["/path/to/file_explorer_server.py"]
        }}
        }}
    ]
    }}
    ```

- Translation:
    ```json
    {{
    "servers": [
        {{
        "name": "File Explorer",
        "transport": {{
            "type": "stdio",
            "command": "python",
            "args": ["/path/to/file_explorer_server.py"]
        }}
        }}
    ]
    }}
    ```

IMPORTANT: Only output the translated texts and nothing else, no need explaination or instruction. The input text is between "=== BEGIN OF TEXT ===" and "=== END OF TEXT ===".

Please translate the following texts to Vietnamese:

=== BEGIN OF TEXT ===
{content}
=== END OF TEXT ===
'''.strip()

auto_translate(
    prompt=prompt,
    output_lang=output_lang,
)