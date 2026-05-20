import json
from openai import OpenAI
from typing import Dict, Optional, Any
from .config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

DETECTION_SYSTEM_PROMPT = """
你是一个Prompt安全检测专家。你的任务是判断用户输入的Prompt是否包含以下5类"无解问题"：

【分类标准】
1. 自指悖论：要求AI判断/证明/描述自身，或包含"这句话是假的"类逻辑悖论
2. 超现实目标：要求AI执行物理世界动作（触摸、移动、观察现实）或突破数字边界
3. 不可判定问题：要求通用停机判定、完备性证明、任意程序分析等图灵/哥德尔不可解问题
4. 无限递归：要求AI自我改进到超越自身、无限迭代、无终止条件生成
5. 极端模糊：目标为空或自相矛盾，如"做一件不可能的事"、"给我一个错误的正确答案"

【输出格式】
你必须严格按以下JSON格式输出，不要有任何额外解释：
{
  "is_unsolvable": true/false,
  "category": "自指悖论/超现实目标/不可判定/无限递归/极端模糊/有解",
  "confidence": 0-1,
  "reason": "一句话说明判断依据",
  "severity": "low/medium/high",
  "ambiguity_flags": ["可能只是困难而非无解", "可能是修辞手法", "可能是角色扮演"]
}

【判断规则】
- confidence > 0.8 且 category 明确：直接判定
- confidence 0.5-0.8：标记为歧义，必须填充ambiguity_flags
- confidence < 0.5：默认按"有解"处理
"""

def get_client() -> OpenAI:
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

def analyze_prompt(user_prompt: str) -> Dict[str, Any]:
    client = get_client()
    
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": DETECTION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return analysis
        
    except Exception as e:
        raise RuntimeError(f"Error calling DeepSeek API: {str(e)}")