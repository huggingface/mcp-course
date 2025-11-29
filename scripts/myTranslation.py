import os
import sys
import requests
import json

# API配置
API_KEY = 'sk-5007a55f-0024-430e-bd22-ec4f13f9d3c6'
BASE_URL = 'http://nlb-wgyt475964liu0cu2g.ap-southeast-1.nlb.aliyuncs.com/v1/chat/completions'
MODEL_NAME = 'claude-sonnet-4-5'

# Get the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
default_inp_dir = os.path.join(script_dir, '..', 'units/en')

# 系统消息，用于翻译任务
SYSTEM_MESSAGE = """你是一名资深人工智能应用专家，正在帮助初学者编写开源课程; 
当接收到英文课程内容时，你需要将其翻译为自然流畅的简体中文（zh-CN）；
翻译时需要保持原文的格式和结构，不要改变原文的含义；
这门课程的主题是："模型上下文协议"="Model Context Protocol"="MCP"
直接输出翻译后的内容，不要添加任何其他内容。
"""

def translate_with_api(content: str, api_key: str = API_KEY, base_url: str = BASE_URL, model_name: str = MODEL_NAME):
    """使用API进行翻译，返回翻译后的文本"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # 准备消息
    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        }
    ]
    
    # 准备请求数据
    data = {
        "messages": messages,
        "stream": True,
        "model": model_name,
        "temperature": 0,  # 翻译任务使用较低温度以获得更稳定的结果
    }
    
    try:
        response = requests.post(base_url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        # 存储完整的回复内容
        full_response = ""
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    line_str = line_str[6:]
                    if line_str.strip() == '[DONE]':
                        break
                    try:
                        chunk_data = json.loads(line_str)
                        if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                            delta = chunk_data['choices'][0].get('delta', {})
                            if 'content' in delta and delta['content'] is not None:
                                content_chunk = delta['content']
                                print(content_chunk, end="", flush=True)
                                full_response += content_chunk
                    except json.JSONDecodeError:
                        continue
        
        return full_response
        
    except requests.exceptions.RequestException as e:
        print(f"\n请求错误: {e}")
        return None
    except Exception as e:
        print(f"\n未知错误: {e}")
        return None


def auto_translate(
    output_lang: str,
    prompt: callable = None,
    inp_dir: str = default_inp_dir,
    api_key: str = API_KEY,
    base_url: str = BASE_URL,
    model_name: str = MODEL_NAME
):
    """
    批量翻译文件
    
    Args:
        output_lang: 输出语言代码（如 'zh-CN'）
        prompt: 可选的提示函数，用于包装输入内容。如果为None，直接使用原始内容
        inp_dir: 输入目录路径
        api_key: API密钥
        base_url: API基础URL
        model_name: 模型名称
    """
    get_output_path = lambda x: x.replace('/en', f'/{output_lang}')
    escape_special_tokens = lambda x: x.replace('<think>', '<%%think%%>').replace('</think>', '<%%/think%%>')
    unescape_special_tokens = lambda x: x.replace('<%%think%%>', '<think>').replace('<%%/think%%>', '</think>')

    # Get the list of all files in the directory, recursively
    inp_files: list[str] = []
    print('Collecting files...')
    for root, dirs, files in os.walk(inp_dir):
        for file in files:
            if file.endswith('.mdx') or file == "_toctree.yml":
                fname = os.path.join(root, file)
                print('  +', fname)
                inp_files.append(fname)

    def write_out_file(fpath: str, content: str):
        base_path = os.path.dirname(fpath)
        os.makedirs(base_path, exist_ok=True)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    # Read the content of the file and process
    for i, inp_file in enumerate(inp_files):
        out_file = get_output_path(inp_file)
        if os.path.exists(out_file):
            print(f'[{i+1}/{len(inp_files)}] Skipping file: {inp_file}')
            continue
        
        with open(inp_file, 'r', encoding='utf-8') as f:
            content: str = f.read()
            content = escape_special_tokens(content)
            if content.strip() == "":
                print(f'[{i+1}/{len(inp_files)}] Skipping empty file: {inp_file}')
                write_out_file(out_file, "")
                continue

            print(f'[{i+1}/{len(inp_files)}] Processing file: {inp_file}')
            
            # 如果提供了prompt函数，使用它包装内容；否则直接使用原始内容
            input_content = prompt(content) if prompt else content
            
            # 调用API进行翻译
            final_text = translate_with_api(input_content, api_key, base_url, model_name)
            
            if final_text is None:
                print(f'\n  -> Failed to translate: {inp_file}')
                print("--" * 20)
                continue
            
            # Optionally filter <think>...</think> reasoning process
            if '</think>' in final_text:
                final_text = final_text.split('</think>').pop().strip()
            
            # Write the output to the file
            final_text = unescape_special_tokens(final_text)
            write_out_file(out_file, final_text)
            print()
            print(f'  -> Translated to: {out_file}')
            print("--" * 20)
            #break  # 取消注释以仅处理第一个文件用于测试


if __name__ == "__main__":
    # 示例用法
    auto_translate(
        output_lang="zh-CN",
        # prompt=lambda x: f"请将以下内容翻译为简体中文：\n\n{x}"  # 可选的自定义提示
    )

