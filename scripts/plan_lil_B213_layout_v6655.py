"""Plan full-width whole paragraphs, retaining all prose and one justified native page continuation."""
from functools import cache
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B212_layout_v6608 import WEAK,norm
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B213_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B213_layout_v6655')
PAIRS={('kublai','khan'),('shandong','peninsula'),('three','hundred'),('two','hundred'),('gold','seal'),('sea','king'),('great','emperor'),('this','continent'),('this','land'),('that','hero'),('my','family'),('for','a'),('a','moment'),('ruler','of'),('of','the'),('the','seas')}
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert row['kind']=='progressive' and row['source_selector'] in [2,9,170] and body.strip()==body and all(32<=ord(c)<127 for c in body);words=body.split();assert ' '.join(words)==body;long=row['id']=='DK4_MES_B213_R0042';maximum=8 if long else 4
    def display(text):return text.replace('{MACRO:FI}','Lil')
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==maximum:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(display(text));final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and display(text).endswith('I'):continue
            # Retain the whole final instruction on page2, following the completed territory statement.
            if long and line==3 and not final and words[stop-1]!='conquer.':continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'));weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and (stop-start==1 or length<=8));candidate=((cost[0]+weak,cost[1]+tiny,cost[2]+1,cost[3]+(0 if final else (36-length)**2)),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No source/prose-preserving B213 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body;markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B213-source-bound-layout-RESEARCH-ONLY',max_lines=maximum,leading_speaker_bytes=frozenset([2,9,170]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile);return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(display(v)) for v in lines],encoded_hex=encoded.encoded.hex(),diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=maximum,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4,all_words_punctuation_and_single_FI_unchanged=True,page_boundary_reason='The completed statement about the unconquered land ends page1. The full imperative Give my sword to that hero begins page2. All152 characters survive through original four-row pagination; no dramatic command, viewport/font edit, shortening or inherited letter-footer rule.' if long else None)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'eighteen_whole_paragraph_plans_one_original_page_continuation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,physical_viewport=[216,64],physical_native_rows_per_page=4,original_single_FI_default_expansion_Lil_three_bytes_bound=True,no_manual_breaks_or_padding_authored=True,no_inherited_B209_letter_footer_or_B212_menu_exception=True,native_19_pages_and144_alignment_cases_pending=True,all18_formatting_gates_remain_false=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False));print([(r['id'],r['lines'],r['planning_cost']) for r in rows]);print('FAILURES',failures)
    if failures:raise SystemExit(1)
