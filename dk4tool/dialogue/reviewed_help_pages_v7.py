"""Scoped Help phrase continuity;preserve all original tokens andlink objects while avoiding tiny tails."""
from dk4tool.dialogue import reviewed_help_pages_v6 as previous
from scripts.prepare_help_pages_v281 import words,WIDTH
from scripts.source_locked_derivation_v5118 import checked_text

def protected_wrap(text):
    tokens=words(text);groups=[];index=0
    phrases=[['or','L,'],['or','B'],['3','fatigue.'],['when','you','approach.'],
      ['You','may','receive','an','item.'],['to','stop','in','place.']]
    while index<len(tokens):
        size=1
        for phrase in phrases:
            if tokens[index:index+len(phrase)]==phrase:size=len(phrase);break
        if index+1<len(tokens):
            a,b=tokens[index:index+2]
            if isinstance(a,str) and a.lower()=='press' and isinstance(b,str) and b.rstrip('.,;:') in ['A','B','X','Y','L','R']:size=2
            if a=='[Tip]':size=2
            if isinstance(a,dict) and a['label']=='Deck' and b=='positions.':size=2
        groups.append(tokens[index:index+size]);index+=size
    rows=[];line=[];length=0
    for group in groups:
        width=sum(len(t['label']if isinstance(t,dict)else t)for t in group)+len(group)-1
        if width>WIDTH:raise ValueError('Help protected phrase exceeds validated width')
        if line and length+1+width>WIDTH:rows.append(line);line=[];length=0
        length+=bool(line)+width;line.extend(group)
    if line:rows.append(line)
    return rows

SOURCE=checked_text(previous.SOURCE,{
 "protected_plain_English_phrases=['press A','press B','press X','press Y','at least 150.']":
 "protected_plain_English_phrases=['press button','tip marker with next word','or L','or B','3 fatigue','when you approach','You may receive an item','Deck positions','to stop in place']",
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-andallocation-guards-with-reviewed-phrase-continuity','exec'),env)
plan_articles=env['plan_articles']
