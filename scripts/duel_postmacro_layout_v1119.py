"""CPU prototype only:balanced24x3 paragraphs after original macro expansion."""
from functools import lru_cache

WIDTH,MAX_ROWS=24,3
WEAK={'a','an','the','to','of','with','for','from','on','in','as','at','and'}
KEEP={('a','duel'),('fair','duel'),("let's",'duel'),('one','on'),('on','one'),('let','us')}


def layout(raw):
    text=raw.decode('cp932')
    if not text or text!=' '.join(text.split()) or any(ord(c)<32 for c in text):
        raise ValueError('One post-expansion paragraph without authored alignment required')
    words=text.split(' ')
    cells=lambda s:len(s.encode('cp932'))
    if any(cells(w)>WIDTH for w in words):raise ValueError('A complete source word exceeds native24 columns')
    @lru_cache(None)
    def solve(start,rows):
        if start==len(words):return (0,()) if rows==0 else None
        if rows==0:return None
        choices=[]
        for end in range(start+1,len(words)+1):
            line=' '.join(words[start:end]);width=cells(line)
            if width>WIDTH:break
            tail=solve(end,rows-1)
            if tail is None:continue
            last=words[end-1].strip('.,!?;:').lower()
            weak=end<len(words) and not line.endswith(('.', '!', '?', ';', ':')) and last in WEAK
            orphan=end==len(words) and start>0 and end-start==1
            short=end==len(words) and start>0 and width<9
            split=end<len(words) and (last,words[end].strip('.,!?;:').lower()) in KEEP
            score=(WIDTH-width)**2+2000*weak+8000*orphan+1000*short+3000*split
            if end<len(words):
                if line.endswith(('.', '!', '?')):score-=200
                elif line.endswith((',', ';', ':')):score-=100
            choices.append((score+tail[0],(line,)+tail[1]))
        return min(choices) if choices else None
    choices=[]
    for rows in range(1,MAX_ROWS+1):
        result=solve(0,rows)
        if result is not None:choices.append((result[0]+160*(rows-1),result[1]))
    if not choices:raise ValueError('Complete source paragraph exceeds actual24x3 duel viewport')
    lines=list(min(choices)[1]);assert ' '.join(lines)==text
    # Before LF the original static painter must finish an odd ASCII pair.
    # No guard indent is authored or emitted at the next line. The NUL case
    # already has its own native invisible final-space flush.
    encoded=[]
    for i,line in enumerate(lines):
        value=line.encode('cp932')
        if i<len(lines)-1 and trailing_ascii_phase(line):value+=b' '
        encoded.append(value)
    output=b'\n'.join(encoded)
    assert b' '.join(output.split())==raw and all(len(v)<=WIDTH for v in encoded)
    return output,lines


def trailing_ascii_phase(text):
    """A native double-byte glyph ends the preceding ASCII draw batch."""
    phase=0
    for character in text:
        encoded=character.encode('cp932')
        if len(encoded)==2:phase=0
        else:
            if len(encoded)!=1 or encoded[0]>=128:
                raise ValueError('Unmapped one-byte non-ASCII glyph in duel prototype')
            phase^=1
    return phase
