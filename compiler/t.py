import re

ex = re.compile(r"""('.+')|(".+")""")
s = """Hello,my name is 'primelee',hahha"""
a = ex.search(s)
print a.group()