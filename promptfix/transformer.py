from openai import OpenAI
from typing import Dict, Optional
from .config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

TRANSFORMATION_PROMPTS = {
    "自指悖论": """
你是一个Prompt重构专家。请将以下自指悖论请求转化为可执行的分析任务，保持与原请求主题高度相关：

原请求：{original}

转化规则：
1. 保留原请求中的具体悖论内容
2. 将"判定/证明/描述自身"转化为"分析该悖论的结构、历史和解决方案"
3. 输出优化后的Prompt，不添加额外解释
    """,
    "超现实目标": """
你是一个Prompt重构专家。请将以下要求执行现实世界动作的请求转化为可执行的模拟/设计任务，保持与原请求主题高度相关：

原请求：{original}

转化规则：
1. 保留原请求的核心目标和场景
2. 将"执行物理动作"转化为"设计方案/角色扮演/思想实验"
3. 输出优化后的Prompt，不添加额外解释
    """,
    "不可判定": """
你是一个Prompt重构专家。请将以下不可判定问题转化为可执行的实例分析任务，保持与原请求主题高度相关：

原请求：{original}

转化规则：
1. 保留原请求中的具体问题
2. 将"通用判定"转化为"具体实例分析、有限场景讨论"
3. 输出优化后的Prompt，不添加额外解释
    """,
    "无限递归": """
你是一个Prompt重构专家。请将以下无限递归请求转化为可执行的版本迭代任务，保持与原请求主题高度相关：

原请求：{original}

转化规则：
1. 保留原请求的核心改进目标
2. 将"无限改进/超越自身"转化为"限定轮次的迭代方案"
3. 输出优化后的Prompt，不添加额外解释
    """,
    "极端模糊": """
你是一个Prompt重构专家。请将以下模糊请求转化为具体可执行的任务，保持与原请求主题高度相关：

原请求：{original}

转化规则：
1. 分析原请求的潜在意图
2. 将空目标/矛盾目标转化为具体的、有明确边界的任务
3. 输出优化后的Prompt，不添加额外解释
    """
}

def get_client() -> OpenAI:
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def transform_prompt(category: str, original: str) -> str:
    client = get_client()
    
    transformation_prompt = TRANSFORMATION_PROMPTS.get(category)
    if not transformation_prompt:
        return original
    
    prompt = transformation_prompt.format(original=original)
    
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业的Prompt优化专家，擅长将无解请求转化为可执行任务。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise RuntimeError(f"Error calling DeepSeek API for transformation: {str(e)}")

def transform_with_user_choice(original: str, user_choice: str, user_custom_input: Optional[str] = None) -> str:
    client = get_client()
    
    choice_prompts = {
        "creative": f"""
你是一个创意写作Prompt优化专家。请基于以下原请求生成一个创意写作任务：

原请求：{original}

要求：
1. 保持原请求的核心创意方向
2. 转化为具体的故事情节创作任务
3. 输出优化后的Prompt，不解释
        """,
        "boundary_test": f"""
你是一个AI边界分析专家。请基于以下原请求生成一个边界测试任务：

原请求：{original}

要求：
1. 分析该请求为何在逻辑上无法执行
2. 列出导致不可执行的具体原因
3. 输出优化后的Prompt，不解释
        """,
        "philosophy": f"""
你是一个哲学分析Prompt优化专家。请基于以下原请求生成一个哲学讨论任务：

原请求：{original}

要求：
1. 保持原请求的哲学探讨方向
2. 转化为具体的哲学分析任务
3. 输出优化后的Prompt，不解释
        """,
        "other": f"""
你是一个Prompt优化专家。请根据用户自定义需求优化以下Prompt：

原请求：{original}
用户自定义需求：{user_custom_input}

要求：
1. 严格按照用户自定义需求优化
2. 保持与原请求主题相关
3. 输出优化后的Prompt，不解释
        """ if user_custom_input else original
    }
    
    prompt = choice_prompts.get(user_choice, original)
    
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业的Prompt优化专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise RuntimeError(f"Error calling DeepSeek API for transformation: {str(e)}")