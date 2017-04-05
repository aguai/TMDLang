import typing


def in_str_ret_list(s: str) -> list:
    return [i for i in s]


x = in_str_ret_list('hello 阿怪')
print(x)
y = in_str_ret_list('8')
print(y)
