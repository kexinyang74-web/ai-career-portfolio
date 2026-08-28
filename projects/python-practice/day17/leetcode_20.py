# 20. 有效的括号
# 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s，判断字符串是否有效。
# 有效字符串需满足：
#   1. 左括号必须用相同类型的右括号闭合
#   2. 左括号必须以正确的顺序闭合

# 示例 1：
# 输入：s = "()"        → True
# 示例 2：
# 输入：s = "()[]{}"    → True
# 示例 3：
# 输入：s = "(]"        → False
# 示例 4：
# 输入：s = "([)]"      → False  （括号顺序错误：先 [ 后 )，交叉了）
# 示例 5：
# 输入：s = "{[]}"      → True

class Solution:
    def isValid(self, s: str) -> bool:                      # 定义一个方法，参数是字符串 s，返回值是布尔值
        stack = []                                         # 定义一个栈，用于存储左括号
        for char in s:                                     # 遍历字符串 s           # 如果字符是左括号，则入栈      # 如果字符是右括号，则出栈  
            if char in "({[":                              # 如果字符是左括号，则入栈
                stack.append(char)                         # 将字符入栈
            elif char in ")}]":                            # 如果字符是右括号，则出栈               
                if not stack:                            # 如果栈为空，则返回 False
                    return False                           
                top = stack.pop()                        # 如果栈不为空，则出栈
                if char == ")" and top != "(":            # 如果右括号和左括号不匹配，则返回 False
                    return False                            
                if char == "}" and top != "{":            # 如果右括号和左括号不匹配，则返回 False
                    return False                            
                if char == "]" and top != "[":            # 如果右括号和左括号不匹配，则返回 False
                    return False                            
        return not stack                               # 如果栈为空，则返回 True
        
if __name__ == "__main__":
    solution = Solution()
    print(solution.isValid("()"))
    print(solution.isValid("()[]{}"))
    print(solution.isValid("(]"))
    print(solution.isValid("([)]"))
    print(solution.isValid("{[]}"))