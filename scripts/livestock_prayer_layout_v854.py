"""Bounded36x3 word planner that can prefer readable clauses over fewer bad rows."""

from functools import lru_cache

from scripts.work_comments_layout_v843 import serialize,WEAK

WIDTH=36
MAX_LINES=3
ROW_COST=450
KEEP_TOGETHER={('holy','spirit'),('strongest','fleet')}


def layout(text):
    if not text or not text.isascii() or text!=' '.join(text.split()):
        raise ValueError('One natural ASCII paragraph required;no authored padding or breaks')
    if any(ord(c)<32 or ord(c)>126 for c in text) or any(c in text for c in '%{}'):
        raise ValueError('This family supplies no formatter arguments or translator controls')
    words=text.split(' ')
    if any(len(word)>WIDTH for word in words):raise ValueError('Complete word exceeds native width')
    @lru_cache(None)
    def solve(start,rows):
        if start==len(words):return (0,()) if rows==0 else None
        if rows==0:return None
        choices=[]
        for end in range(start+1,len(words)+1):
            line=' '.join(words[start:end])
            if len(line)>WIDTH:break
            tail=solve(end,rows-1)
            if tail is None:continue
            last=words[end-1].strip('.,!?;:').lower()
            weak=end!=len(words) and not line.endswith(('.', '!', '?', ';', ':')) and last in WEAK
            orphan=end==len(words) and start!=0 and (end-start==1 or len(line)<12)
            split=end!=len(words) and (last,words[end].strip('.,!?;:').lower()) in KEEP_TOGETHER
            cost=(WIDTH-len(line))**2+2000*weak+4000*orphan+3000*split
            if end!=len(words):
                if line.endswith(('.', '!', '?')):cost-=300
                elif line.endswith((',', ';', ':')):cost-=150
            choices.append((cost+tail[0],(line,)+tail[1]))
        return min(choices) if choices else None
    choices=[]
    for count in range(1,MAX_LINES+1):
        result=solve(0,count)
        if result is not None:choices.append((result[0]+ROW_COST*(count-1),result[1]))
    if not choices:raise ValueError('Complete paragraph exceeds the registered216x36 body')
    lines=list(min(choices)[1]);assert ' '.join(lines)==text
    return lines


def compiled(row):return serialize(layout(row['english']))
