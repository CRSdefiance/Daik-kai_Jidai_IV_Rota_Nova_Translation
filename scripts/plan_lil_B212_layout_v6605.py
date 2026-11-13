"""Plan B212's ten complete paragraphs within the unchanged four-row native viewport."""
from functools import cache
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B212_editorial_manuscript_v2.json');ROOT=Path('work/analysis/lil_B212_layout_v6605')
WEAK=set('a an as at for from in of the to with and or but so that than because if by into not i you he she it we they my your our his her their is are was were be been being can could will would shall should may might must have has had do does did this these those then why where what when how said them us me him her against'.split())
WEAK.update({"that's","there's","i'll","you've","it's","must've","blade's","doesn't","couldn't"})
PAIRS={('three','kingdoms'),('zhao','yun'),('guan','yu'),('zhuge','liang'),('changban','bridge'),('cao','cao'),('to','tears'),('his','chest'),('get','along'),('favorite','general'),('give','it'),('a','read'),('a','lot'),('around','here'),('i','think'),('have','better'),('better','luck'),('magnificent','beard'),('memorial','before'),('before','the'),('the','expedition')}
def norm(word):return word.strip('.,!?;:\"\'()').casefold()
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert row['kind']=='progressive' and row['source_selector'] in [149] and body.strip()==body and all(32<=ord(c)<127 for c in body);words=body.split();assert ' '.join(words)==body
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==4:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(text);final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and text.endswith('I'):continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'))
            ordinary=False;weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and (stop-start==1 or length<=8));candidate=((cost[0]+weak,cost[1]+tiny,cost[2]+1,cost[3]+(0 if final else (36-length)**2)),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No bounded whole-paragraph B212 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body;markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B212-source-bound-layout-RESEARCH-ONLY',max_lines=4,leading_speaker_bytes=frozenset([149]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(v) for v in lines],encoded_hex=encoded.encoded.hex(),diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=4,native_rows_per_page=4,all_words_and_punctuation_unchanged=True,no_inherited_B209_footer_continuation_or_boundary_exemption=True)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        if row['kind']!='progressive':continue
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'nine_whole_paragraph_research_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,physical_viewport=[216,64],maximum_native_rows=4,source_bound_original_even_preLF_reservation_not_changed_codec=True,no_manual_breaks_or_padding_authored=True,no_B209_source_page_footer_or_boundary_exception=True,all14_formatting_gates_remain_false=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False));print([(r['id'],r['lines'],r['planning_cost']) for r in rows]);print('FAILURES',failures)
    if failures:raise SystemExit(1)
