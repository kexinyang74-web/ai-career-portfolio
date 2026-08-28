# 给定两个字符串 s 和 t ，判断它们是否是同构的。
# 如果 s 中的字符可以按某种映射关系替换得到 t ，那么这两个字符串是同构的。
# 每个出现的字符都应当映射到另一个字符，同时不改变字符的顺序。不同字符不能映射到同一个字符上，相同字符只能映射到同一个字符上，字符可以映射到自己本身。

def is_isomorphic(s, t):
    if len(s) != len(t):
        return False

    正向 = {}    # s 的字符 → t 的字符（查"一个人一个号"）
    反向 = {}    # t 的字符 → s 的字符（查"一个号一个人"）

    for 左, 右 in zip(s, t):
        if 左 in 正向:
            if 正向[左] != 右:      # s 字符已经配过，配的却不是这个 → 冲突
                return False
        else:
            正向[左] = 右            # 第一次见，记下来

        if 右 in 反向:
            if 反向[右] != 左:      # t 字符已经被别人占 → 冲突
                return False
        else:
            反向[右] = 左

    return True

print(is_isomorphic("egg", "add"))
print(is_isomorphic("foo", "bar"))
print(is_isomorphic("paper", "title"))