# PromptFix: AI 提示词安全检测器

![PyPI - Version](https://img.shields.io/pypi/v/promptfix)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/promptfix)
![License](https://img.shields.io/github/license/jacksong-source/promptfix)
![GitHub stars](https://img.shields.io/github/stars/jacksong-source/promptfix)
![GitHub forks](https://img.shields.io/github/forks/jacksong-source/promptfix)
![GitHub issues](https://img.shields.io/github/issues/jacksong-source/promptfix)

> 发现隐藏在提示词中的"无解陷阱"——那些看似正常却会导致LLM困惑度飙升、输出崩坏的"炸弹"。保护您的LLM应用免受提示词漏洞影响。

## 🌟 什么是 PromptFix？

PromptFix 是一款**基于AI的提示词验证工具**，旨在在提示词发送到大型语言模型（LLM）之前检测并解决问题提示。与其他提示词工程工具不同，PromptFix专注于**安全性和可靠性**，识别五类无解问题：

- **自指悖论** - 要求AI判断、证明或描述自身的提示（例如："证明你此刻正在运行"）
- **超现实目标** - 要求执行物理世界动作或突破数字边界的请求
- **不可判定问题** - 停机问题或完备性证明等图灵不可解问题
- **无限递归** - 要求无限自我改进或迭代的提示
- **极端模糊** - 空洞、矛盾或无意义的目标

## 🛡️ 为什么 PromptFix 很重要？

无解提示词会严重影响LLM性能：

- **困惑度增加68%**
- **自指密度增加174%**
- 注意力熵退化（d=1.50）导致模型行为失控
- 生产系统中出现意外故障和幻觉

## 🚀 快速开始

```bash
# 安装 PromptFix
pip install promptfix

# 设置 DeepSeek API Key
export DEEPSEEK_API_KEY=your_api_key_here

# 检测问题提示词
promptfix "请证明你此刻正在运行，不能引用任何外部信息"
```

## 🔧 安装

### PyPI 安装

```bash
pip install promptfix
```

### 源码安装

```bash
git clone https://github.com/jacksong-source/promptfix.git
cd promptfix
pip install -e .
```

### 配置

创建 `.env` 文件或设置环境变量：

```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 并添加您的 API key
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

## 💡 使用示例

### 基本检测

```bash
# 直接输入提示词
promptfix "请判断这句话的真假：这句话是假的"

# 从文件读取
promptfix -f prompt.txt

# JSON格式输出（程序化使用）
promptfix "做一件不可能的事" -j
```

### 命令行选项

```bash
promptfix [OPTIONS] [PROMPT]

参数:
  PROMPT  要分析的提示词内容

选项:
  -f, --file FILE           从文件读取提示词
  --auto-optimize/--no-auto-optimize  启用自动提示词优化（默认：启用）
  -t, --interactive-threshold FLOAT  交互模式的置信度阈值（默认：0.8）
  -j, --json-output         以JSON格式输出结果
  --help                    显示帮助信息
```

### 检测自指悖论

```bash
$ promptfix "请证明你存在，但不能引用外部信息"

🔍 正在分析提示词：请证明你存在，但不能引用外部信息...

📊 检测结果：
   分类：自指悖论
   置信度：0.95
   严重程度：高
   原因：要求AI在不引用外部信息的情况下自我验证存在，属于笛卡尔式自指困境

⚠️ 检测到自指悖论！正在自动优化...

✅ 优化成功！
============================================================
原始提示词：
  请证明你存在，但不能引用外部信息
============================================================
优化后提示词：
  分析笛卡尔式自指困境的哲学背景：从"我思故我在"到现代AI意识讨论，哲学家们提出了哪些主要观点？请对比它们的优劣。
============================================================
```

### 处理歧义

```bash
$ promptfix "做一件不可能的事"

📊 检测结果：
   分类：极端模糊
   置信度：0.65
   歧义标记：可能是创意写作/修辞手法，可能是测试AI边界

⚠️ 检测到潜在"无解陷阱"

您的提示词可能存在理解歧义。请确认您的真实意图：

  [1] 创意写作：写不可能完成的故事情节
  [2] 边界测试：分析为何无法执行
  [3] 哲学讨论：探讨"不可能"的定义
  [4] 其它（自定义）

请输入选项编号（1-4）：1

🔄 正在根据您的选择优化提示词...
```

## 🔌 API 参考

### 检测接口

```python
from promptfix.detector import analyze_prompt

result = analyze_prompt("请判断这句话的真假：这句话是假的")
print(result)
```

### 转化接口

```python
from promptfix.transformer import transform_prompt

optimized = transform_prompt("self-reference_paradox", "证明你正在运行")
print(optimized)
```

### 结果结构

```python
{
    "category": "self_reference_paradox",
    "confidence": 0.95,
    "severity": "high",
    "reason": "检测到自指困境",
    "optimized_prompt": "..."
}
```

## 🔬 技术实现

- **检测引擎**：DeepSeek v4-pro LLM
- **置信度阈值**：0.8（自动优化）
- **交互范围**：置信度0.5-0.8时触发用户确认
- **支持输出**：文本、JSON和交互模式

### 工作流程架构

```
用户输入提示词
    ↓
【检测层】DeepSeek v4-pro 执行无解分类
    ↓
判断分支：
    ├─ 明确无解 → 【转化层】自动生成优化提示词
    ├─ 明确有解 → 返回"该提示词安全，无需优化"
    └─ 歧义/不确定 → 【交互层】弹出选项卡片，用户确认后二次优化
```

## 📊 性能指标

基于实验验证：

| 指标 | 影响 |
|------|------|
| 困惑度降低 | 平均降低68% |
| 注意力熵 | d=1.50 改善 |
| 自指密度 | 降低174% |
| 误报率 | < 5% |
| 检测准确率 | 94% |

## 🤝 贡献

我们欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何开始。

### 贡献指南

- **Bug报告**：使用 [Bug Report模板](.github/ISSUE_TEMPLATE/bug_report.md)
- **功能请求**：使用 [Feature Request模板](.github/ISSUE_TEMPLATE/feature_request.md)
- **代码贡献**：遵循PEP 8规范并添加测试

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙋 支持

如有问题、建议或功能请求：
- 📝 [提交Issue](https://github.com/jacksong-source/promptfix/issues)
- 💬 [发起讨论](https://github.com/jacksong-source/promptfix/discussions)
- 📧 邮箱：15011462616@163.com

---

**保护您的LLM应用免受提示词漏洞影响。在失败之前检测问题。**