import json,re
from pathlib import Path
TOKEN=re.compile(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+')
def parse(s):
 stack=[]
 for t in TOKEN.findall(s):
  if t=='(':stack.append([])
  elif t==')':
   n=stack.pop()
   if stack:stack[-1].append(n)
   else:return n
  else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
def nodes(n,k):return [x for x in n if isinstance(x,list) and x and x[0]==k]
def one(n,k):return next(iter(nodes(n,k)),None)
def prop(n,k):return next((x[2] for x in nodes(n,'property') if x[1]==k),None)
