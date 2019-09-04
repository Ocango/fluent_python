# def factorial(n):
#     """return factorial n!"""
#     return 1 if n<2 else n * factorial(n-1)

# print(factorial.__doc__)

# fact = factorial
# print(list(map(fact,range(11))))


def clip(text:str,max_len:'int > 0' = 10) -> str:
    """
    最长max_len后截断空格
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ',0,max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_before = text.rfind(' ',max_len)
            if space_before >= 0:
                end = space_before
    
    if end is None:
        end = len(text)
    return text[:end].rstrip()

print(clip("""Everyone don't like this question.""",max_len=20))
print(clip.__defaults__)
print(clip.__code__.co_varnames)
print(clip.__code__.co_argcount)
print(clip.__annotations__)
