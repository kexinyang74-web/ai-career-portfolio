def count_words(text):
    return len(text.split())

print(count_words("I love python"))

def format_name(first,last):
    return first.strip().title() + " " + last.strip().title()

print(format_name(" ada ", " lovelace "))
