"""Source-bound full-width formatting research for two reviewed Market letters.

No historical planner or runtime filter is changed. Prose has no authored breaks
or padding. Ordinary soft wrapping may end one row with a complete word 'for'.
Native planes, exact allocations and actual release scope require separate proof.
"""
from functools import cache

PARAGRAPHS={
    774:"Oh, I know! I'll write you a letter of introduction to thank you for selling us those popular goods.",
    775:"And I'll write you a letter of recommendation to thank you for selling us so many popular goods.",
}
WEAK=frozenset('a an as at for from in of the to with'.split())

def compile_letter(message_ID,english,allocation):
    if message_ID not in PARAGRAPHS or english.removesuffix('{PAD}')!=PARAGRAPHS[message_ID]:
        raise ValueError('Only the two reviewed complete letter paragraphs are owned')
    text=PARAGRAPHS[message_ID];words=text.split(' ')
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
    if plan is None:raise ValueError('No complete native four-row layout')
    lines=list(plan[1]);extras=[0]*(len(lines)-1)
    def encode():
        result=bytearray(b'  ');phase=0
        for index,line in enumerate(lines):
            result.extend(line.encode());phase=(phase+len(line))&1
            if index<len(lines)-1:
                result.extend(b' '*extras[index])
                if phase:result.extend(b' ');phase=0
                result.extend(b'\n  ')
        return bytes(result)
    result=encode();padding=allocation-len(result)
    if padding<0:raise ValueError('Reviewed wording exceeds the exact owned allocation')
    # Keep the original NUL address. Even pre-LF allocation spaces preserve the
    # draw-pair phase and all glyph origins; final spaces stay inside35 cells.
    for i,line in enumerate(lines[:-1]):
        while len(lines[-1])+padding>35 and len(line)+extras[i]+2<=34 and padding>=2:
            extras[i]+=2;padding-=2
    if len(lines[-1])+padding>35:raise ValueError('Owned tail padding would escape the final native row')
    result=encode()+b' '*padding
    if len(result)!=allocation or b' '.join(result.split())!=text.encode():raise ValueError('Exact allocation or prose changed')
    return result,dict(lines=lines,generated_even_pre_LF_allocation_spaces=extras,generated_terminal_spaces=padding,
        complete_word_weak_endings=[dict(row=i,word=s.split()[-1]) for i,s in enumerate(lines[:-1]) if s.split()[-1].strip('.,!?;:').lower() in WEAK],
        fixed_native_budgets=[34]*(len(lines)-1)+[35],authored_breaks_or_alignment_spaces=False)
