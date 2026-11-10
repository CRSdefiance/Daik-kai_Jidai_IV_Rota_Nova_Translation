"""Plan full-width zero-macro English paragraphs with guarded literal-I eligibility."""
from functools import cache
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B214_layout_v6705b import WEAK,norm
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B234_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B234_layout_v7586d')
PAIRS={('these', 'days'), ('pope', 'treasured'), ('of', 'it'), ('back', 'to'), ('flourished', 'in'), ('a', 'pope'), ('how', 'much'), ('to', 'venice'), ('they', 'say'), ('think', 'of'), ('own', 'business'), ('quite', 'a'), ('to', 'have'), ("god's", 'favor'), ('back', 'in'), ('at', 'last'), ('papal', 'power'), ('we', 'found'), ('linked', 'to'), ('lost', 'in'), ('back', 'then'), ('on', 'business'), ('those', 'lands'), ('used', 'by'), ('turn', 'up'), ('trade', 'in'), ('the', 'pope'), ('once', 'ruled'), ('he', 'may'), ('made', 'fortunes'), ('the', 'church'), ('hard', 'work'), ('power', 'was'), ('the', 'lords'), ('vacant', 'look'), ('when', 'did'), ('moving', 'goods'), ('a', 'discovery'), ('he', 'once'), ('in', 'thought'), ('a', 'point'), ('their', 'ship'), ('get', 'here'), ('said', 'to'), ('to', 'give'), ('my', 'great-grandfather'), ('how', 'lucky'), ('a', 'blessing'), ('in', 'action'), ('kind', 'of'), ('almost', 'to'), ('your', 'face'), ('been', 'used'), ('direct', 'rule'), ('on', 'your'), ('draw', 'customers'), ('have', 'been'), ('papal', 'states'), ('your', 'own'), ('goods', 'around'), ('carry', 'a'), ('make', 'fortunes'), ('old', 'self'), ('it', 'was'), ('come', 'to'), ('its', 'height')}

def display(text):return text.replace('{MACRO:FA}','Argot').replace('…','XX')
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert row['kind']=='progressive' and row['source_selector'] in [19,104] and body.strip()==body and all(32<=ord(c)<127 or c=='…' and row['id']=='DK4_MES_B234_R0005' and body=='………' and bytes.fromhex(row['source_hex'])==bytes.fromhex('68816381638163') for c in body)
    limit=4;words=body.split();assert ' '.join(words)==body
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==limit:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(display(text));final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and words[stop-1]=='I':continue
            if not final and row['id']=='DK4_MES_B234_R0033' and (norm(words[stop-1]),norm(words[stop]))==('papal','states'):continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'));ordinary=pair in {'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set());weak=int(not final and not ordinary and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int((final and start>0 and (stop-start==1 or length<=8)) or (line==0 and not final and length<=12))
            candidate=((cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+(0 if final else (36-length)**2*(2 if line==0 else 1))),(stop,*breaks))
            if best is None or candidate[0] < best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:limit=8;solve.cache_clear();result=solve(0,0)
    if result is None:raise ValueError('No source/prose-preserving B234 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body;markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B234-source-bound-layout-RESEARCH-ONLY',max_lines=limit,leading_speaker_bytes=frozenset([19,104]));assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(display(v)) for v in lines],encoded_hex=encoded.encoded.hex(),diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=limit,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4,all_words_punctuation_and_zero_macros_unchanged=True,automatic_boundaries=[dict(last=norm(a.split()[-1]),first=norm(b.split()[0]),pair=[norm(a.split()[-1]),norm(b.split()[0])]) for a,b in zip(lines,lines[1:])])
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'eighteen_whole_paragraph_plans_no_macros_no_prose_changes.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,physical_viewport=[216,64],physical_native_rows_per_page=4,no_original_or_invented_FI_FA_FO_substitutions=True,no_manual_breaks_padding_or_alignment_authored=True,minimize_orphans_then_rows_then_contextual_weak_boundaries_within_source_four_rows=True,no_inherited_letter_style_or_unreviewed_pagination_assumption=True,automatic_extra_native_page_only_if_original_four_rows_cannot_hold_complete_prose=True,no_preapproved_weak_boundary_waiver_all_individual_decisions_pending=True,all18_formatting_gates_remain_false=True,native_complete_pages_and_source_specific_controls_pending=True,only_exact_source_R5_three_CP932_ellipses_allowed_no_global_non_ASCII_exception=True,source_R33_Papal_States_kept_together_within_original_four_row_page=True,R16_draw_customers_ordinary_complete_word_boundary_not_global_weak_rule_waiver=True,source_bound_printable68_selector_not_generic_ASCII_prefix=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],r['line_lengths'],r['planning_cost'])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
