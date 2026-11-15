"""Semantic Help paragraph pagination,compact repeated headings andwhole press-B phrase;no runtime edits."""
from dk4tool.dialogue import reviewed_help_pages_v2 as previous
from scripts.prepare_help_pages_v281 import words,WIDTH
from scripts.source_locked_derivation_v5118 import checked_text


def protected_wrap(text):
    tokens=words(text);merged=[];index=0
    while index<len(tokens):
        if tokens[index:index+2]==['press','B.']:
            merged.append('press B.');index+=2
        else:merged.append(tokens[index]);index+=1
    rows,line,length=[],[],0
    for token in merged:
        width=len(token['label'] if isinstance(token,dict) else token)
        if width>WIDTH:raise ValueError('Help token exceeds validated width')
        if length+bool(line)+width>WIDTH:rows.append(line);line=[];length=0
        length+=bool(line)+width;line.append(token)
    if line:rows.append(line)
    return rows


SOURCE=checked_text(previous.SOURCE,{
    "        title,english=row['heading'],row['english']":
        "        title,english=row['heading'],row['english']\n        continued_title=title.split(' (',1)[0]+' (continued)'",
    "            if topic!=37 or len(sections)!=2 or not row.get('semantic_section_reason'):":
        "            if topic not in [22,25,37,38,39] or len(sections)!=2 or not row.get('semantic_section_reason'):",
    'Only the bound source military-investment cost/outcome paragraphs aresectioned':
        'Only reviewed source-tip,letter-instruction,investment andcontract-condition paragraphs aresectioned',
    "            if '１口につき' not in Japanese or '投資すると武装度が上がります' not in Japanese:raise ValueError('Source military cost/outcome paragraphs missing')":
        """            markers={22:['【！】','主計長'],25:['紹介状','総督府'],37:['１口につき','投資すると武装度が上がります'],38:['100％','ただし'],39:['100％','ただし']}
            if any(marker not in Japanese for marker in markers[topic]):raise ValueError('Source semantic paragraph context missing')""",
    "title if not batches else title+' (continued)'":"title if not batches else continued_title",
    "title if number==0 else title+' (continued)'":"title if number==0 else continued_title",
    'formatting_gate_required=require_formatting,':
        "formatting_gate_required=require_formatting,continuation_headings_repeat_command_without_redundant_caller_context=True,protected_plain_English_phrases=['press B.'],",
})
env={**previous.plan_articles.__globals__,'wrap':protected_wrap,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-source-links-inverse-andnative-bounds-with-reviewed-paragraph-flow','exec'),env)
plan_articles=env['plan_articles']
