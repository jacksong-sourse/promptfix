import unittest
from unittest.mock import Mock, patch
from promptfix.detector import analyze_prompt
from promptfix.transformer import transform_prompt
from promptfix.cli import analyze_and_fix, display_options, get_user_choice

class TestDetector(unittest.TestCase):
    
    @patch('promptfix.detector.OpenAI')
    def test_analyze_prompt(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices[0].message.content = '{"is_unsolvable": true, "category": "自指悖论", "confidence": 0.95, "reason": "测试", "severity": "high", "ambiguity_flags": []}'
        mock_client.chat.completions.create.return_value = mock_response
        
        result = analyze_prompt("请证明你自己正在运行")
        
        self.assertTrue(result["is_unsolvable"])
        self.assertEqual(result["category"], "自指悖论")
        self.assertEqual(result["confidence"], 0.95)

class TestTransformer(unittest.TestCase):
    
    @patch('promptfix.transformer.OpenAI')
    def test_transform_prompt(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices[0].message.content = "优化后的Prompt"
        mock_client.chat.completions.create.return_value = mock_response
        
        result = transform_prompt("自指悖论", "原Prompt")
        
        self.assertEqual(result, "优化后的Prompt")

class TestCLI(unittest.TestCase):
    
    def test_display_options(self):
        options = display_options()
        self.assertEqual(len(options), 4)
        self.assertEqual(options[0]["id"], "creative")
    
    def test_get_user_choice_valid(self):
        options = [{"id": "test1"}, {"id": "test2"}, {"id": "test3"}, {"id": "test4"}]
        with patch('builtins.input', return_value='2'):
            choice = get_user_choice(options)
            self.assertEqual(choice["id"], "test2")

if __name__ == '__main__':
    unittest.main()