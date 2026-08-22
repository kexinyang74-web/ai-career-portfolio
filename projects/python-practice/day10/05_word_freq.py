#统计每个单词出现次数（字典+ split)
def word_freq(text):
    freq = {}
    for word in text.split():
        freq[word] = freq.get(word,0) +1
    return freq

print(word_freq("the cat and the dog"))

#找出出现次数最多的单词
def most_common(freq):
    best_word = None
    best_count = 0
    for word, count in freq.items():
        if count >best_count:
            best_word = word
            best_count = count 
    return best_word, best_count

freq = word_freq("the cat and the dog")
print(most_common(freq))
