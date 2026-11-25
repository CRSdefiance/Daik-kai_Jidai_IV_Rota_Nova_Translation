"""Create narrowly bound successors without modifying prior executed tools."""
from pathlib import Path
import json
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B139_B140_layout_tools_v3469')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B139_B140_controls_v3464/all67_dispatches12_predicates1_query_and_C200_contract.json')
VOICE=Path('work/analysis/lil_B139_B140_voices_v3460/current_seven_static_names_voices_and207_catalog_rebind.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);control=read(CONTROL);pairs=[]
    dependencies=[SOURCE,CONTROL,VOICE,Path('work/analysis/lil_B139_B140_terms_v3466/clean_current_items_polder_names_entries_and_copy_census.json'),Path('work/analysis/lil_B139_B140_branches_v3463b/original_relative_skip_operand_proof.json')]
    dependencies += [Path(control[k]) for k in ['registered_catalog_binding','source_exact_conditional_result_contract','source_C200_contract']]
    profile=Path('dk4tool/dialogue/lil_B139_B140_profile.py');assert not profile.exists()
    hashes={b[k] for b in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']}
    text='''"""Exact B139/B140 progressive consumers and source-owned UI control."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=%r
BLOCKS=frozenset(%r)
SELECTORS=frozenset({2,4,9,16,20,21,171})
DEPENDENCIES=%r
CONTROL=Path(%r)
VOICE=Path(%r)
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B139/B140 clean/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Source contract changed:'+path)
    c=json.loads(CONTROL.read_text(encoding='utf-8'));v=json.loads(VOICE.read_text(encoding='utf-8'))
    if consumer!='progressive' or len(c['speech_dispatch_cases'])!=134 or len(c['current_original_predicate_cases'])!=13 or len(c['original_event_queries'])!=1 or c['original_event_queries'][0]['event']!=129 or c['source_macro_counts']!={'FI':7,'FA':0,'FO':0} or len(c['source_C200_cases'])!=1 or len(v['fresh_seven_actor_names']['rows'])!=7:raise ValueError('Complete seven actor, twelve predicate, query129, FI7 and C200 contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B139-B140-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';67 progressive speeches, seven static actors, Lil captain2 and FI7. Original query129, twelve predicates and source-owned C200 UI writes bound. Resource bodies and selected scene not executed by this profile.')
'''%(source['current_ARM9_sha256'],sorted(hashes),{str(p):sha(p.read_bytes()) for p in dependencies},str(CONTROL),str(VOICE))
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8')
    def make(old,new,changes):
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('dk4tool/dialogue/lil_B138_layout_v2.py','dk4tool/dialogue/lil_B139_B140_layout_v1.py',[
        ('lil-B138-progressive-runtime-bound-v1','lil-B139-B140-progressive-runtime-bound-v1'),('frozenset({2,14,20,21,22,23,92})','frozenset({2,4,9,16,20,21,171})'),('exact source-bound B138 profile','exact source-bound B139/B140 profile'),
        ('def _word(value):',"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('evergreen','lotus'),('lotus','leaf'),('kushan','platter'),('indian',\"ocean's\"),('coastal','dikes'),('pump','out'),('polder','project'),('living','expenses'),('farming','village'),('every','day'),('one','day'),('make','people'),('people','happy')})\n\ndef _word(value):")])
    make('scripts/plan_lil_B138_layout_v3436b.py','scripts/plan_lil_B139_B140_layout_v3469.py',[
        ('plan44','plan67'),('lil_B138_layout_v3436b','lil_B139_B140_layout_v3469'),('lil_remaining_B138_B140_source_v3422','lil_remaining_B139_B140_source_v3456'),('next44_B138','next67_B139_B140'),('lil_B138_profile','lil_B139_B140_profile'),('lil_B138_layout_v2','lil_B139_B140_layout_v1'),('lil_B138_editorial_manuscript_v4','lil_B139_B140_editorial_manuscript_v1'),('lil_B138_editorial_manuscript_v5','lil_B139_B140_editorial_manuscript_v2'),('all44','all67'),('len(reports)==44','len(reports)==67'),('plans=44','plans=67'),('leading FE staging','source staging')])
    make('scripts/verify_lil_B138_fonts_v3435.py','scripts/verify_lil_B139_B140_fonts_v3470.py',[
        ('Current352 macro calls,44 progressive planes and44 full paragraph QA.','Current536 macro calls,67 progressive planes and67 full paragraph QA.'),('lil_B138_profile','lil_B139_B140_profile'),('lil_B138_layout_v1','lil_B139_B140_layout_v1'),('lil_B138_fonts_v3435','lil_B139_B140_fonts_v3470'),('lil_B138_editorial_manuscript_v4','lil_B139_B140_editorial_manuscript_v2'),('len(cases)==44 and len(qa_reports)==44 and macro_calls==352','len(cases)==67 and len(qa_reports)==67 and macro_calls==536'),('blocks[138]','blocks[139]'),('selectors=[2,14,20,21,22,23,92]','selectors=[2,4,9,16,20,21,171]'),('format(14 if selector==2 else 2','format(4 if selector==2 else 2'),('all44','all67'),('current_original_macro_alignment_calls=352','current_original_macro_alignment_calls=536'),('actual_selected_B137_IDs','actual_selected_B139_B140_IDs'),('44complete progressiveplanes,352macro cases,44QAplans','67 complete progressive planes,536 macro cases,67 QA plans'),('sixsheets','nine sheets')])
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),scoped_profile=str(profile),scoped_profile_sha256=sha(profile.read_bytes()),successors=pairs,producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,no_review_or_completion_credit=True,full_goal_complete=False))
