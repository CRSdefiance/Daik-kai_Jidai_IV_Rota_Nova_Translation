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
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json');ROOT=Path('work/analysis/lil_B221_layout_v6976c')
PAIRS={('holy','land'),('islamic','history'),('peace','terms'),('come','to'),('think','of'),('of','it'),('anything','went'),('gone','missing'),('our','true'),('true','hero'),('good','person'),('dirty','tricks')}
def display(text):return text.replace('{MACRO:FA}','Argot')
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert row['kind']=='progressive' and row['source_selector'] in [2,17,85] and body.strip()==body and all(32<=ord(c)<127 for c in body)
    words=body.split();assert ' '.join(words)==body;maximum=8 if row['id'] in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060'] else 4
    @cache
    def solve(start,line):
        if start==len(words):return (0,0,0,0),()
        if line==maximum:return None
        best=None
        for stop in range(start+1,len(words)+1):
            text=' '.join(words[start:stop]);length=len(display(text));final=stop==len(words);reserve=int(not final and length%2==0)
            if length+reserve+int(line>0)>36:continue
            if not final and words[stop-1]=='I':continue
            if line==3 and not final and row['id'] in ['DK4_MES_B221_R0046','DK4_MES_B221_R0060'] and words[stop-1]!=('slaughter...' if row['id'].endswith('0046') else 'terms.'):continue
            tail=solve(stop,line+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None;terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'));weak=int(not final and ((word in WEAK and not terminal) or pair in PAIRS));tiny=int(final and start>0 and (stop-start==1 or length<=8))
            if row['id']=='DK4_MES_B221_R0067' and pair==('had','gone'):weak=0
            candidate=((cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+(0 if final else (36-length)**2*(2 if line==0 else 1))),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No source/prose-preserving B221 plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body;markup=prefix+'{LB}'.join(lines);profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B221-source-bound-layout-RESEARCH-ONLY',max_lines=maximum,leading_speaker_bytes=frozenset([2,17,85]));assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(display(v)) for v in lines],encoded_hex=encoded.encoded.hex(),diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=maximum,native_rows_per_page=4,expected_native_pages=(len(lines)+3)//4,all_words_punctuation_and_zero_macros_unchanged=True,automatic_boundaries=[dict(last=norm(a.split()[-1]),first=norm(b.split()[0]),pair=[norm(a.split()[-1]),norm(b.split()[0])]) for a,b in zip(lines,lines[1:])])
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rows=[];failures=[]
    for row in doc['records']:
        try:rows.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'fourteen_whole_paragraph_plans_no_macros_no_prose_changes.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,physical_viewport=[216,64],physical_native_rows_per_page=4,no_original_or_invented_FI_FA_FO_substitutions=True,no_manual_breaks_padding_or_alignment_authored=True,minimize_orphans_then_rows_before_weak_boundaries=True,no_inherited_letter_style_or_multipage_exception=True,scoped_two_page_records=['DK4_MES_B221_R0046','DK4_MES_B221_R0060'],page_boundary_reasons={'DK4_MES_B221_R0046':'The reported wealth question and plunder/slaughter examples remain together on the first page. The second page keeps the complete anything-went report and its hearsay tag together, rather than stranding so I hear alone. No word is cut or added.','DK4_MES_B221_R0060':'The first page completes all three examples of humane conduct, including peace terms. The second page contains the entire following praise without splitting dirty tricks across a page. No word, viewport or native row limit changes.'},all14_formatting_gates_remain_false=True,native_complete_pages_and_source_specific_controls_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],r['line_lengths'],r['planning_cost'])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
