"""Plan complete source-faithful English paragraphs,typed notices and a full signature footer."""
from functools import cache
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B214_layout_v6705b import WEAK,norm
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B223_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B223_layout_v7091c')
PAIRS={('ian','dukov'),('mongol',"empire's"),('mongol','empire'),('ruling','line'),('two','hundred'),('hundred','years'),('years','ago'),('central','to'),('west','asia'),('coat','of'),('of','mail'),('enemy','arrows'),('sword','and'),('spear','blades'),('burial','goods'),('scorching','desert'),('russian','people'),('look','into'),('out','of')}
SCOPED_TWO_PAGE_ALLOWANCE={'DK4_MES_B223_R0031','DK4_MES_B223_R0040'}
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert body.strip()==body and all(32<=ord(c)<127 for c in body) and row['source_selector'] in [2,13,21,208]
    words=body.split();assert ' '.join(words)==body;maximum=8 if row['id'] in SCOPED_TWO_PAGE_ALLOWANCE else 4;signature=row['id']=='DK4_MES_B223_R0048';footer=words.index('--') if signature else None
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==maximum:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(text);final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and words[stop-1]=='I':continue
            if footer is not None and (start<footer<stop or start==footer and stop<len(words)):continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'))
            ordinary=row['id']=='DK4_MES_B223_R0040' and pair==('scorching','desert');weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and start!=footer and (stop-start==1 or length<=8))
            candidate=((cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+(0 if final else (36-length)**2*(2 if line==0 else 1))),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No complete source/prose-preserving B223 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body and all(lines) and len(lines)<=maximum
    markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B223-source-bound-layout-RESEARCH-ONLY',max_lines=maximum,leading_speaker_bytes=frozenset([2,13,21,208]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    enc=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);raw=bytes.fromhex(row['source_hex'])
    if row['kind']!='progressive':raw=bytes([row['source_selector']])+raw
    encoded=enc(raw,row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(v) for v in lines],encoded_hex=encoded.encoded.hex(),virtual_typed_selector_removed_when_packed=row['kind']!='progressive',diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=maximum,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4,signature_footer_on_separate_automatic_row=signature,all_words_punctuation_and_zero_macros_unchanged=True,automatic_boundaries=[dict(last=norm(a.split()[-1]),first=norm(b.split()[0]),pair=[norm(a.split()[-1]),norm(b.split()[0])]) for a,b in zip(lines,lines[1:])])
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'seventeen_complete_paragraph_plans_original_width_no_prose_changes.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,physical_viewport=[216,64],physical_native_rows_per_page=4,scoped_two_page_allowance=sorted(SCOPED_TWO_PAGE_ALLOWANCE),every_page_retains_original_geometry_no_taller_viewport=True,full_Ian_Dukov_footer_automatic_row_not_authored_indentation=True,no_manual_break_padding_alignment_or_prose_cut=True,unsafe_bare_uppercase_I_line_end_ineligible=True,minimize_orphans_then_rows_then_weak_boundaries_then_fullness=True,all17_formatting_gates_remain_false=True,native_complete_pages_QA_boundaries_and_actual_English_pending=True,exact_R40_scorching_desert_modifier_noun_boundary_fills_opening_not14=True,validated_guard_continuation_reservation_retained_no36_cell_exception=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],r['line_lengths'],r['planning_cost'])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
