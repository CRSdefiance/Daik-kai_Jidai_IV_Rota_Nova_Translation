"""Exact-allocation full-width reflow for the reviewed recommendation offer775.

The other three reopened leads retain their exact layouts. No historical helper,
native filter, prose word, viewport, font metric or control is changed.
"""
from functools import cache

MESSAGE_ID=775
PARAGRAPH="And I'll write you a letter of recommendation to thank you for selling us so many popular goods."
ALLOCATION=105
WEAK=frozenset('a an as at for from in of the to with'.split())

def compile_letter(message_ID,english,allocation):
    if message_ID!=MESSAGE_ID or allocation!=ALLOCATION or english.removesuffix('{PAD}')!=PARAGRAPH:
        raise ValueError('Only the exact reviewed775 paragraph and105-byte allocation are owned')
    words=PARAGRAPH.split(' ')
    @cache
    def solve(start,row):
        if start==len(words):return (0,0,()),()
        if row==4:return None
        best=None
        for stop in range(start+1,len(words)+1):
            line=' '.join(words[start:stop]);final=stop==len(words)
            if len(line)>(35 if final else 34) or final and start and len(line)<=8:continue
            tail=solve(stop,row+1)
            if tail is None:continue
            weak=not final and words[stop-1].strip('.,!?;:').lower() in WEAK
            cost=(1+tail[0][0],int(weak)+tail[0][1],(() if final else (34-len(line),))+tail[0][2])
            if best is None or cost<best[0]:best=cost,(line,*tail[1])
        return best
    plan=solve(0,0)
    if plan is None:raise ValueError('No complete native layout')
    lines=list(plan[1]);result=bytearray(b'  ');phase=0
    for index,line in enumerate(lines):
        result.extend(line.encode());phase=(phase+len(line))&1
        if index<len(lines)-1:
            if phase:result.extend(b' ');phase=0
            result.extend(b'\n  ')
    padding=allocation-len(result)
    if padding<0 or len(lines[-1])+padding>35:raise ValueError('Owned padding escapes the final native row')
    result.extend(b' '*padding)
    if len(result)!=allocation or b' '.join(result.split())!=PARAGRAPH.encode():raise ValueError('Exact allocation or prose changed')
    return bytes(result),dict(lines=lines,generated_even_pre_LF_allocation_spaces=[0]*(len(lines)-1),generated_terminal_spaces=padding,
        complete_word_weak_endings=[dict(row=i,word=s.split()[-1]) for i,s in enumerate(lines[:-1]) if s.split()[-1].strip('.,!?;:').lower() in WEAK],
        fixed_native_budgets=[34]*(len(lines)-1)+[35],authored_breaks_or_alignment_spaces=False)
