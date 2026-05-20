import click
import json
from colorama import init, Fore, Style
from .detector import analyze_prompt
from .transformer import transform_prompt, transform_with_user_choice
from .config import (
    INTERACTIVE_THRESHOLD, 
    LOW_CONFIDENCE_THRESHOLD,
    STATUS_COLORS,
    SEVERITY_COLORS
)

init(autoreset=True)

OPTIONS = [
    {"id": "creative", "label": "创意写作：写不可能完成的故事情节"},
    {"id": "boundary_test", "label": "边界测试：分析为何无法执行"},
    {"id": "philosophy", "label": "哲学讨论：探讨'不可能'的定义"},
    {"id": "other", "label": "其它（自定义）"}
]

def print_status(status, message):
    color = STATUS_COLORS.get(status, "")
    print(f"{color}{message}{Style.RESET_ALL}")

def print_severity(severity, message):
    color = SEVERITY_COLORS.get(severity, "")
    print(f"{color}{message}{Style.RESET_ALL}")

def display_options():
    print("\n⚠️ 检测到潜在\"无解陷阱\"")
    print("\n您的提示词可能存在理解歧义。请确认您的真实意图：")
    print()
    
    for i, opt in enumerate(OPTIONS, 1):
        print(f"  [{i}] {opt['label']}")
    
    print()
    return OPTIONS

def get_user_choice(options):
    while True:
        try:
            choice = int(input("请输入选项编号（1-4）："))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("无效选项，请输入1-4之间的数字")
        except ValueError:
            print("请输入有效数字")

def get_custom_input():
    return input("请输入您的具体需求：")

def analyze_and_fix(prompt, auto_optimize=True, interactive_threshold=INTERACTIVE_THRESHOLD):
    print(f"\n🔍 正在检测Prompt：{prompt[:50]}..." if len(prompt) > 50 else f"\n🔍 正在检测Prompt：{prompt}")
    
    try:
        analysis = analyze_prompt(prompt)
    except Exception as e:
        print(f"{Fore.RED}检测失败：{str(e)}{Style.RESET_ALL}")
        return
    
    confidence = analysis.get("confidence", 0)
    category = analysis.get("category", "有解")
    is_unsolvable = analysis.get("is_unsolvable", False)
    reason = analysis.get("reason", "")
    severity = analysis.get("severity", "low")
    ambiguity_flags = analysis.get("ambiguity_flags", [])
    
    print(f"\n📊 检测结果：")
    print(f"   分类：{category}")
    print(f"   置信度：{confidence:.2f}")
    print(f"   严重程度：{severity}")
    print(f"   原因：{reason}")
    
    if ambiguity_flags:
        print(f"   歧义标记：{', '.join(ambiguity_flags)}")
    
    if confidence < LOW_CONFIDENCE_THRESHOLD:
        print_status("safe", "\n✅ 该Prompt安全，无需优化")
        return {
            "status": "safe",
            "original_prompt": prompt,
            "analysis": analysis
        }
    
    if confidence < interactive_threshold or (ambiguity_flags and len(ambiguity_flags) > 0):
        options = display_options()
        selected_option = get_user_choice(options)
        
        if selected_option["id"] == "other":
            custom_input = get_custom_input()
        else:
            custom_input = None
        
        print("\n🔄 正在根据您的选择优化Prompt...")
        optimized = transform_with_user_choice(prompt, selected_option["id"], custom_input)
        
        print(f"\n{Fore.GREEN}优化成功！{Style.RESET_ALL}")
        display_comparison(prompt, optimized)
        
        return {
            "status": "optimized",
            "original_prompt": prompt,
            "analysis": analysis,
            "user_choice": selected_option["id"],
            "optimized_prompt": optimized
        }
    
    if is_unsolvable and auto_optimize:
        print_severity(severity, f"\n⚠️ 检测到{category}！正在自动优化...")
        optimized = transform_prompt(category, prompt)
        
        print(f"\n{Fore.GREEN}优化成功！{Style.RESET_ALL}")
        display_comparison(prompt, optimized)
        
        return {
            "status": "unsolvable_detected",
            "original_prompt": prompt,
            "analysis": analysis,
            "optimized_prompt": optimized
        }
    
    print_status("safe", "\n✅ 该Prompt安全，无需优化")
    return {
        "status": "safe",
        "original_prompt": prompt,
        "analysis": analysis
    }

def display_comparison(original, optimized):
    print("\n" + "="*60)
    print(f"{Fore.RED}原始Prompt：{Style.RESET_ALL}")
    print(f"  {original}")
    print("\n" + "="*60)
    print(f"{Fore.GREEN}优化后Prompt：{Style.RESET_ALL}")
    print(f"  {optimized}")
    print("="*60)

@click.command()
@click.argument('prompt', required=False)
@click.option('--file', '-f', type=click.File('r'), help='从文件读取prompt')
@click.option('--auto-optimize/--no-auto-optimize', default=True, help='是否自动优化')
@click.option('--interactive-threshold', '-t', type=float, default=INTERACTIVE_THRESHOLD, help='交互阈值')
@click.option('--json-output', '-j', is_flag=True, help='输出JSON格式')
def main(prompt, file, auto_optimize, interactive_threshold, json_output):
    if file:
        prompt = file.read().strip()
    
    if not prompt:
        prompt = input("请输入要检测的Prompt：")
    
    result = analyze_and_fix(prompt, auto_optimize, interactive_threshold)
    
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()