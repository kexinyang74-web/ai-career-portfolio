strs = ["flower","flow","flight"]




def longest_common_prefix(strs):
    prefix = strs[0]                  # 先假设第一个就是答案
    for s in strs[1:]:
        while not s.startswith(prefix):   # s 不以 prefix 开头 → 还没对上
            prefix = prefix[:-1]          # 把暂定答案砍掉最后一个字符
            if prefix == "":
                return ""
    return prefix
print(longest_common_prefix(strs))