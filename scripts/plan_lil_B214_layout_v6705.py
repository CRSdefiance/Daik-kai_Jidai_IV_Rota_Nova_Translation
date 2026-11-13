"""Plan whole-paragraph wraps in original native width, keeping the letter signature together."""
from pathlib import Path
from functools import cache
from dataclasses import replace
from types import FunctionType
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B214_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B214_layout_v6705')
WEAK=set('a an as at for from in of the to with and or but so that than because if by into i you he she it we they my your our his her their is are was were be been can could will would shall should may might must have has had do does did this these those not'.split())
PAIRS={('janus','pasar'),('manuel','almeida'),('twelve','disciples'),('keen','edge'),('open','mind'),('jesus\'s','twelve'),('just','like'),('letter','from'),('in','touch'),('come','in'),('looking','for'),('lead','to')}
def norm(s):return s.strip('.,!?;:\"\'()').casefold()
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert body and body.strip()==body and all(32<=ord(c)<127 for c in body)
    words=body.split();assert ' '.join(words)==body;count=len(words);signature=row['id']=='DK4_MES_B214_R0068';footer=words.index('--') if signature else None
    @cache
    def solve(start,r):
        if start==count:return (0,0,0,0),()
        if r>=4:return None
        best=None
        for stop in range(start+1,count+1):
            line=' '.join(words[start:stop]);length=len(line);final=stop==count;reserve=int(not final and length%2==0)
            if length+reserve>36:continue
            if footer is not None and (start<footer<stop or start==footer and stop<count):continue
            tail=solve(stop,r+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'))
            weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and start!=footer and (stop-start==1 or length<=8))
            candidate=((cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+(0 if final else (36-length)**2)),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No complete bounded paragraph plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body and len(lines)<=4 and all(lines)
    markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B214-source-bound-layout-RESEARCH-ONLY',max_lines=4,leading_speaker_bytes=frozenset([2,4,23,208]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    enc=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__)
    raw=bytes.fromhex(row['source_hex'])
    if row['kind']!='progressive':raw=bytes([row['source_selector']])+raw
    encoded=enc(raw,row['english'],profile)
    boundaries=[dict(last=norm(a.split()[-1]),first=norm(b.split()[0]),pair=[norm(a.split()[-1]),norm(b.split()[0])]) for a,b in zip(lines,lines[1:])]
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(v) for v in lines],encoded_hex=encoded.encoded.hex(),virtual_typed_selector_removed_when_packed=row['kind']!='progressive',diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=4,native_rows_per_page=4,signature_footer_on_separate_automatic_row=signature,all_words_and_punctuation_unchanged=True,automatic_boundaries=boundaries)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);results=[];failures=[]
    for row in doc['records']:
        try:results.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'seventeen_complete_paragraph_plans_original_width_no_prose_changes.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=results,failures=failures,all_original216x64_four_row_single_page_plans=True,complete_Janus_Pasar_footer_automatic_row_not_authored_indentation=True,no_new_native_guards_font_metrics_or_viewport=True,minimize_orphans_then_added_rows_before_reviewing_exact_ordinary_boundaries=True,exact_weak_boundaries_and_native_first_last_glyphs_require_review=True,all_formatting_gates_remain_false=True,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in results:print(r['id'],r['lines'],r['line_lengths'],r['planning_cost'])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
