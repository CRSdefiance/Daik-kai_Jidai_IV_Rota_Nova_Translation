"""Create exact five-actor B167 profile and source-bound speech layout/native tools."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/lil_B167_layout_tools_v4130')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B167_editorial_manuscript_v1.json')
    source=read(doc['source_context'])
    deps={doc[k]:doc[k+'_sha256'] for k in ['source_context','control_contract','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']}
    hashes=sorted({g[k] for g in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    old=Path('dk4tool/dialogue/lil_B166_profile.py')
    profile=Path('dk4tool/dialogue/lil_B167_profile.py')
    assert not profile.exists()
    text=old.read_text(encoding='utf-8').replace('B166','B167')
    for key,value in [('BLOCKS','frozenset('+repr(hashes)+')'),('SELECTORS','frozenset({2,4,13,23,109})'),('DEPENDENCIES',repr(deps))]:
        text,n=re.subn('^'+key+'=.*$',lambda m:key+'='+value,text,flags=re.M)
        assert n==1
    text=text[:text.index('    return replace(')]+"    return replace(base,name='lil-B167-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,metrics_source=base.metrics_source+';27 original54020 speeches,five static actors including printable6D Shipwright andsource0D Cesare,no macros,twelve spans,two optionalCesare predicates,six exact leaves,two resources,one typed lecture choice andtwo separated ends. No A000. Typed2100 has a separate consumer. Older0D audit remains open.')\n"
    text=text.replace(text.splitlines()[0],'"""Exact B167 source/runtime binding:27 speeches,five actors,no macros,two ends."""',1)
    compile(text,str(profile),'exec')
    profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B166_layout_v4.py','dk4tool/dialogue/lil_B167_layout_v1.py',{
        "expected={'lil-B166-progressive-runtime-bound-v1':frozenset({2,9,20,23})}":
            "expected={'lil-B167-progressive-runtime-bound-v1':frozenset({2,4,13,23,109})}",
        'source-bound B166 profile':'source-bound B167 profile',
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('square','sails'),('square','sail'),('triangular','sails'),('following','wind'),('jigger','spanker'),('each','mast'),('small','ships'),('large','ships'),('small','mast'),('two','or'),('or','more'),('more','masts'),('rear','quarter')})\n\ndef _word(value):"}))
    tools.append(derive('scripts/plan_lil_B166_layout_v4067.py','scripts/plan_lil_B167_layout_v4131.py',{
        'lil_B166_layout_v1':'lil_B167_layout_v1','lil_B166_profile':'lil_B167_profile',
        'lil_B166_layout_v4067':'lil_B167_layout_v4131','lil_B166_editorial_manuscript_v1':'lil_B167_editorial_manuscript_v1',
        'lil_B166_editorial_manuscript_v2':'lil_B167_editorial_manuscript_v2',
        'all42_paragraph':'all27_paragraph','len(reports)==42':'len(reports)==27','plans=42':'plans=27','Plan42':'Plan27'}))
    tools.append(derive('scripts/verify_lil_B166_fonts_v4068.py','scripts/verify_lil_B167_fonts_v4132.py',{
        'lil_B166_profile':'lil_B167_profile','lil_B166_layout_v1':'lil_B167_layout_v1',
        'lil_B166_fonts_v4068':'lil_B167_fonts_v4132','lil_B166_editorial_manuscript_v2':'lil_B167_editorial_manuscript_v2',
        'len(cases)==42 and len(qa_reports)==42 and macro_calls==336':'len(cases)==27 and len(qa_reports)==27 and macro_calls==216',
        'blocks[166]':'blocks[167]','blocks[167]':'blocks[168]','[2,9,20,23]':'[2,4,13,23,109]',
        'all42':'all27','current_original_macro_alignment_calls=336':'current_original_macro_alignment_calls=216',
        'actual_selected_B166_IDs':'actual_selected_B167_IDs','len(negatives)==17':'len(negatives)==19',
        'Current336 macro calls,42 progressive planes and42 complete paragraph QA.':'Current216 macro calls,27 progressive planes and27 complete paragraph QA.',
        '42 complete progressive planes,336 macro cases,42 QA plans and17 source-consumer negatives pass;six sheets':
            '27 complete progressive planes,216 macro cases,27 QA plans and19 source-consumer negatives pass;four sheets'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'exact_B167_profile_formatter_and_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        source_profile=str(old),source_profile_sha256=sha(old.read_bytes()),dependencies=deps,tools=tools,
        source_scope=dict(speeches=27,actors=[2,4,13,23,109],FI=0,relative_sites=12,Cesare_queries=2,opaque_leaves=6,
            two_separated_ends=True,no_A000=True,typed_menu_separate=True),no_global_profile_guard_change=True,
        no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B167 exact five-actor profile,27-paragraph planner and216-case native checks created;typed menu separate.')
