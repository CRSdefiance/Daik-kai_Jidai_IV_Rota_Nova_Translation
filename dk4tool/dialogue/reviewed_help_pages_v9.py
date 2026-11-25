"""Keep reviewed skill thresholds, role names and sparse ending phrases continuous in Deck Help."""
from dk4tool.dialogue import reviewed_help_pages_v8 as previous
from scripts.prepare_help_pages_v281 import words,WIDTH
from scripts.source_locked_derivation_v5118 import checked_text

ROLES=[['Chief','Cook'],['Animal','Keeper'],['First','Mate'],['Boarding','Leader'],['Sail','Handler'],
    ['Shipwright'],['Surgeon'],['Missionary'],['Strategist'],['Purser'],['Captain'],['Surveyor'],['Helmsman'],['Lookout'],['Gunner'],['Deckhand']]
STATS={'Aim','Social','Tactics','Observe','Command','Swords','Health','Sailing','Survey','Finance'}
PHRASES=[['A','highly','skilled','Surveyor'],['for','exploring.'],['for','trade.'],['the','price.'],['If','every','mast'],
    ['Gun','Batteries'],['Cargo','Holds']]

def matches(tokens,at,phrase):
    actual=tokens[at:at+len(phrase)]
    return len(actual)==len(phrase)and all(isinstance(a,str)and a.rstrip('.,;:')in[b,b+'s']for a,b in zip(actual,phrase,strict=True))

def protected_wrap(text):
    tokens=words(text);groups=[];at=0
    while at<len(tokens):
        size=1;a=tokens[at]
        if isinstance(a,str):
            if a.lower()=='press'and at+1<len(tokens)and isinstance(tokens[at+1],str)and tokens[at+1].rstrip('.,;:')in['A','B','X','Y','L','R']:size=2
            if a in STATS and at+3<len(tokens)and isinstance(tokens[at+1],str)and tokens[at+1].isdigit()and tokens[at+2]=='or'and tokens[at+3].rstrip('.,;:')=='higher':size=4
            for phrase in PHRASES:
                if matches(tokens,at,phrase):size=max(size,len(phrase))
            for role in ROLES:
                if matches(tokens,at,role):size=max(size,len(role))
                if a.lower()in['a','an']and matches(tokens,at+1,role):size=max(size,len(role)+1)
        if at+2<len(tokens)and isinstance(a,dict)and tokens[at+1]=='and'and isinstance(tokens[at+2],dict)and a['label']=='Workrooms'and tokens[at+2]['label']=='Holds.':size=3
        groups.append(tokens[at:at+size]);at+=size
    rows=[];line=[];length=0
    for group in groups:
        width=sum(len(t['label']if isinstance(t,dict)else t)for t in group)+len(group)-1
        if width>WIDTH:raise ValueError('Help protected phrase exceeds validated width')
        if line and length+1+width>WIDTH:rows.append(line);line=[];length=0
        length+=bool(line)+width;line.extend(group)
    if line:rows.append(line)
    return rows

SOURCE=checked_text(previous.SOURCE,{
    "protected_plain_English_phrases=['press button','tip marker with next word','or L','or B','3 fatigue','when you approach','You may receive an item','Deck positions','to stop in place']":
        "protected_plain_English_phrases=['press button','native skill and complete threshold','native role with article','linked Workrooms and Holds','the price','If every mast','Gun Batteries','Cargo Holds','for exploring','for trade']",
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-prose-links-and-bounds-with-complete-Deck-phrases','exec'),env)
plan_articles=env['plan_articles']
