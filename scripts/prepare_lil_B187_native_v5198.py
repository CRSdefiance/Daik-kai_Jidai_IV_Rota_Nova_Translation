"""Freeze exact B187 roles/linear commands and prepare unshortened paragraph checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B187_native_tools_v5198')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B187_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B187_profile.py');assert not profile.exists()
    text='''"""Exact B187 source/current blocks,Sailor155/Shopkeeper87 and progressive/FE consumers."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({87,155})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B187 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B187 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=32 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All16 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('The FE object must remain null-actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B187 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B187-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';15 original54020 speeches,clean Square Shopkeeper87 voice0 and progressive Sailor155 voice4,separate full-catalogue Retainer155,four read-only name consumers.19 linear commands,A0008 raw00a0ffff014e2fa1,C200672,end674,two tailzeros,no predicates/relative sites. Current V5177 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B187-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C object:tentative Almonds/Malacca notice.228x48logical/228x64physical,conservative216px planning. Almonds is dialogue inflection of approved Almond78. No earlier location,earned boom or verified remedy claim;fresh native approval required.')
    raise ValueError('Unknown B187 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B185_layout_v1.py','dk4tool/dialogue/lil_B187_layout_v1.py',{
        'B185':'B187','frozenset({164,165})':'frozenset({87,155})',
    })]
    rows.append(derive('scripts/plan_lil_B185_layout_v5098.py','scripts/plan_lil_B187_layout_v5199.py',{
        'B185':'B187','layout_v5098':'layout_v5199','Plan8':'Plan16','all8':'all16','len(reports)==8':'len(reports)==16','plans=8':'plans=16',
    }))
    rows.append(derive('scripts/verify_lil_B185_fonts_v5099.py','scripts/verify_lil_B187_fonts_v5200.py',{
        'B185':'B187','fonts_v5099':'fonts_v5200','voices_v5088':'voices_v5189',
        'len(cases)==len(qa_reports)==8 and macro_calls==64':'len(cases)==len(qa_reports)==16 and macro_calls==128',
        'blocks[185]':'blocks[187]','blocks[184]':'blocks[186]','[164,165,254]':'[87,155,254]',
        '165 if selector==164 else 164':'155 if selector==87 else 87',"r['source_selector']==164":"r['source_selector']==87",
        "b'\\xa4Japanese','{SPEAKER:A4}Hello.'":"b'\\x57Japanese','{SPEAKER:57}Hello.'",
        'all8_progressive_FE_native_planes_and64_alignment_cases':'all16_progressive_FE_native_planes_and128_alignment_cases',
        'current_original_macro_alignment_calls=64,progressive_alignment_calls=56,FE_null_actor_alignment_calls=8':
        'current_original_macro_alignment_calls=128,progressive_alignment_calls=120,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=7':'complete_progressive_planes=15',
        'B185 current-font progressive/FE planes and64 native alignment cases':'B187 current-font progressive/FE planes and128 native alignment cases',
        'All8 current-font native planes,64 alignment cases and18 source-consumer negatives pass;one sheet needs visual review.':
        'All16 current-font native planes,128 alignment cases and18 source-consumer negatives pass;two sheets need visual review.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        dependencies=deps,tools=rows,source_exact87_155_selector_guard_prepared_before_planning=True,
        no_inheritance_of_B186_R13_ordinary_boundary_exceptions=True,
        no_prose_shortening_authored_break_font_width_metric_guard_or_global_weak_word_change=True,
        new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared B187 exact profile,paragraph planner and128-alignment verifier;source87/155 guards bound with no inherited R13 exception.')
