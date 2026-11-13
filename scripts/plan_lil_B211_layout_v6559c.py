"""Research automatic whole-paragraph wrapping for B211's two original consumers and FI."""
from functools import cache
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B211_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B211_layout_v6559c')
WEAK=set('a an as at for from in of the to with and or but so that than because if by into not i you he she it we they my your our his her their is are was were be been being can could will would shall should may might must have has had do does did this these those then why where what when how said them us me him against'.split())
WEAK.update({'on','there','like',"that's","there's","i'll","you've","it's","they're","i'd","i'm"})
PAIRS={('wait',"they're"),('what','a'),('lovely','square'),('looks','like'),('little','pond'),('a','pair'),('pair','of'),('of','swans'),('come','here'),('you','two'),('a','journey'),('as','well'),('so','close'),('i','envy'),('envy','you'),('carrying','something'),('off','to'),('what','are'),('are','you'),('you','doing'),('long','and'),('and','shiny'),('somewhere','near'),('near','amsterdam'),('go','take'),('take','a'),('a','look')}
def expanded(text):return text.replace('{MACRO:FI}','Lil')
def norm(word):return expanded(word).strip('.,!?;:\"\'()').casefold()
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';selector=row['source_selector'];assert (row['kind'],selector) in [('progressive',2),('progressive',7),('system-FE',254)] and body.strip()==body and all(32<=ord(c)<127 for c in body);words=body.split();assert ' '.join(words)==body
    assert body.count('{MACRO:FI}')==bytes.fromhex(row['source_hex'])[1:].count(b'FI') and all(m not in body for m in ['{MACRO:FA}','{MACRO:FO}'])
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==4:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(expanded(text));final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and expanded(text).endswith('I'):continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'))
            ordinary=(row['id']=='DK4_MES_B211_R0013' and words[stop-1]=='me,' and not final and words[stop]=='are') or (row['id']=='DK4_MES_B211_R0045' and pair in {('long','and'),('were','headed')});weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and (stop-start==1 or length<=8));candidate=((cost[0]+weak,cost[1]+tiny,cost[2]+1,cost[3]+(0 if final else (36-length)**2)),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No bounded whole-paragraph B211 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body;markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B211-source-bound-layout-RESEARCH-ONLY:'+row['id'],max_lines=4,leading_speaker_bytes=frozenset([selector]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,expanded_lines=[expanded(v) for v in lines],line_lengths=[len(expanded(v)) for v in lines],encoded_hex=encoded.encoded.hex(),diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=4,native_rows_per_page=4,all_words_punctuation_and_original_FI_unchanged=True,no_inherited_B210_ordinary_boundary_or_B208_notice_rule=True)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'twelve_whole_paragraph_research_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,progressive_physical_viewport=[216,64],FE_original228x48_logical228x64_physical_measured216_text_capacity_retained=True,maximum_native_rows=4,original_even_preLF_reservation_guard_and_pair_phase_not_changed=True,no_manual_breaks_or_padding_authored=True,all12_formatting_gates_remain_false=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False));print([(r['id'],r['expanded_lines'],r['planning_cost']) for r in rows]);print('FAILURES',failures)
    if failures:raise SystemExit(1)
