"""
去重算法模块

提供多种去重策略，确保题目唯一性
"""

import hashlib
import sys
import os
from typing import List, Set, Tuple, Dict, Any

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))
from rational import Rational
from expression_parser import ExpressionParser


class Deduplicator:
    """题目去重器"""
    
    def __init__(self):
        self.parser = ExpressionParser()
        self.seen_expressions = set()
        self.seen_results = set()
        self.seen_hashes = set()
    
    def normalize_expression(self, expression: str) -> str:
        """
        标准化表达式（去除空格，统一格式）
        
        Args:
            expression (str): 原始表达式
            
        Returns:
            str: 标准化后的表达式
        """
        # 移除所有空格
        normalized = expression.replace(' ', '')
        
        # 可以添加更多标准化规则
        # 例如：统一分数格式、运算符格式等
        
        return normalized
    
    def calculate_expression_hash(self, expression: str) -> str:
        """
        计算表达式的哈希值
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            str: 表达式的MD5哈希值
        """
        normalized = self.normalize_expression(expression)
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()
    
    def calculate_result_hash(self, expression: str) -> str:
        """
        计算表达式结果的哈希值
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            str: 结果的哈希值
        """
        try:
            result = self.parser.parse(expression)
            # 使用结果的字符串表示作为哈希
            result_str = result.to_string()
            return hashlib.md5(result_str.encode('utf-8')).hexdigest()
        except Exception:
            # 如果解析失败，使用表达式本身
            return self.calculate_expression_hash(expression)
    
    def is_duplicate_by_expression(self, expression: str) -> bool:
        """
        通过表达式检查是否重复
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            bool: 是否重复
        """
        normalized = self.normalize_expression(expression)
        if normalized in self.seen_expressions:
            return True
        
        self.seen_expressions.add(normalized)
        return False
    
    def is_duplicate_by_result(self, expression: str) -> bool:
        """
        通过结果检查是否重复
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            bool: 是否重复
        """
        result_hash = self.calculate_result_hash(expression)
        if result_hash in self.seen_results:
            return True
        
        self.seen_results.add(result_hash)
        return False
    
    def is_duplicate_by_hash(self, expression: str) -> bool:
        """
        通过哈希值检查是否重复
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            bool: 是否重复
        """
        expr_hash = self.calculate_expression_hash(expression)
        if expr_hash in self.seen_hashes:
            return True
        
        self.seen_hashes.add(expr_hash)
        return False
    
    def is_duplicate(self, expression: str, strategy: str = "expression") -> bool:
        """
        检查表达式是否重复
        
        Args:
            expression (str): 表达式字符串
            strategy (str): 去重策略 ("expression", "result", "hash")
            
        Returns:
            bool: 是否重复
        """
        if strategy == "expression":
            return self.is_duplicate_by_expression(expression)
        elif strategy == "result":
            return self.is_duplicate_by_result(expression)
        elif strategy == "hash":
            return self.is_duplicate_by_hash(expression)
        else:
            raise ValueError(f"未知的去重策略: {strategy}")
    
    def deduplicate_problems(self, problems: List[Tuple[str, str]], 
                           strategy: str = "expression") -> List[Tuple[str, str]]:
        """
        对题目列表进行去重
        
        Args:
            problems (List[Tuple[str, str]]): 题目列表
            strategy (str): 去重策略
            
        Returns:
            List[Tuple[str, str]]: 去重后的题目列表
        """
        unique_problems = []
        
        for expression, answer in problems:
            if not self.is_duplicate(expression, strategy):
                unique_problems.append((expression, answer))
        
        return unique_problems
    
    def reset(self):
        """重置去重器状态"""
        self.seen_expressions.clear()
        self.seen_results.clear()
        self.seen_hashes.clear()
    
    def get_statistics(self) -> Dict[str, int]:
        """
        获取去重统计信息
        
        Returns:
            Dict[str, int]: 统计信息
        """
        return {
            "unique_expressions": len(self.seen_expressions),
            "unique_results": len(self.seen_results),
            "unique_hashes": len(self.seen_hashes)
        }


class AdvancedDeduplicator(Deduplicator):
    """高级去重器"""
    
    def __init__(self):
        super().__init__()
        self.expression_trees = set()
        self.semantic_equivalents = set()
    
    def parse_to_tree(self, expression: str) -> Dict[str, Any]:
        """
        将表达式解析为语法树
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            Dict[str, Any]: 语法树
        """
        try:
            # 这里简化实现，实际可以构建更复杂的语法树
            tokens = self.parser.tokenize(expression)
            return {
                "type": "expression",
                "tokens": [{"type": token.type, "value": str(token.value)} for token in tokens]
            }
        except Exception:
            return {"type": "error", "tokens": []}
    
    def is_semantically_equivalent(self, expr1: str, expr2: str) -> bool:
        """
        检查两个表达式是否语义等价
        
        Args:
            expr1 (str): 第一个表达式
            expr2 (str): 第二个表达式
            
        Returns:
            bool: 是否语义等价
        """
        try:
            result1 = self.parser.parse(expr1)
            result2 = self.parser.parse(expr2)
            return result1 == result2
        except Exception:
            return False
    
    def is_duplicate_semantic(self, expression: str) -> bool:
        """
        通过语义等价检查是否重复
        
        Args:
            expression (str): 表达式字符串
            
        Returns:
            bool: 是否重复
        """
        for seen_expr in self.semantic_equivalents:
            if self.is_semantically_equivalent(expression, seen_expr):
                return True
        
        self.semantic_equivalents.add(expression)
        return False
    
    def is_duplicate_advanced(self, expression: str, strategy: str = "semantic") -> bool:
        """
        高级去重检查
        
        Args:
            expression (str): 表达式字符串
            strategy (str): 去重策略
            
        Returns:
            bool: 是否重复
        """
        if strategy == "semantic":
            return self.is_duplicate_semantic(expression)
        else:
            return super().is_duplicate(expression, strategy)


class DeduplicationStats:
    """去重统计"""
    
    def __init__(self):
        self.total_generated = 0
        self.duplicates_found = 0
        self.unique_problems = 0
        self.duplication_rate = 0.0
    
    def add_generation(self, is_duplicate: bool):
        """
        记录一次生成结果
        
        Args:
            is_duplicate (bool): 是否为重复
        """
        self.total_generated += 1
        if is_duplicate:
            self.duplicates_found += 1
        else:
            self.unique_problems += 1
        
        self.duplication_rate = self.duplicates_found / self.total_generated if self.total_generated > 0 else 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        return {
            "total_generated": self.total_generated,
            "duplicates_found": self.duplicates_found,
            "unique_problems": self.unique_problems,
            "duplication_rate": self.duplication_rate
        }
    
    def reset(self):
        """重置统计"""
        self.total_generated = 0
        self.duplicates_found = 0
        self.unique_problems = 0
        self.duplication_rate = 0.0


# 便捷函数
def deduplicate_problems(problems: List[Tuple[str, str]], 
                        strategy: str = "expression") -> List[Tuple[str, str]]:
    """
    去重题目的便捷函数
    
    Args:
        problems (List[Tuple[str, str]]): 题目列表
        strategy (str): 去重策略
        
    Returns:
        List[Tuple[str, str]]: 去重后的题目列表
    """
    deduplicator = Deduplicator()
    return deduplicator.deduplicate_problems(problems, strategy)


# 测试代码
if __name__ == "__main__":
    print("=== 去重算法测试 ===")
    
    # 测试题目列表
    test_problems = [
        ("1 + 2", "3"),
        ("2 + 1", "3"),  # 与第一个结果相同
        ("1 + 2", "3"),  # 与第一个完全相同
        ("3 * 4", "12"),
        ("4 * 3", "12"),  # 与第四个结果相同
        ("1/2 + 1/3", "5/6"),
        ("1/3 + 1/2", "5/6"),  # 与第六个结果相同
    ]
    
    print("\n原始题目:")
    for i, (expr, ans) in enumerate(test_problems, 1):
        print(f"{i}. {expr} = {ans}")
    
    # 测试不同去重策略
    strategies = ["expression", "result", "hash"]
    
    for strategy in strategies:
        print(f"\n使用 {strategy} 策略去重:")
        deduplicator = Deduplicator()
        unique_problems = deduplicator.deduplicate_problems(test_problems, strategy)
        
        for i, (expr, ans) in enumerate(unique_problems, 1):
            print(f"{i}. {expr} = {ans}")
        
        print(f"去重后数量: {len(unique_problems)}")
    
    # 测试高级去重
    print("\n使用语义等价去重:")
    advanced_deduplicator = AdvancedDeduplicator()
    unique_problems = []
    
    for expr, ans in test_problems:
        if not advanced_deduplicator.is_duplicate_advanced(expr, "semantic"):
            unique_problems.append((expr, ans))
    
    for i, (expr, ans) in enumerate(unique_problems, 1):
        print(f"{i}. {expr} = {ans}")
    
    print(f"去重后数量: {len(unique_problems)}")
