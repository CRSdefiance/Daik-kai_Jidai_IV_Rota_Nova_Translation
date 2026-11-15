"""Freeze B184's exact two voices and progressive/FE display contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B184_native_tools_v5049')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B184_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys}
    hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    parent=Path('dk4tool/dialogue/lil_B183_profile.py');text=parent.read_text(encoding='utf-8')
    body=text[text.index('def profile_for('):]
    replacements={
        'B183':'B184','len(cases)!=50':'len(cases)!=18',"sum(r['source_selector']==254 for r in cases)!=4":"sum(r['source_selector']==254 for r in cases)!=2",
        'All25':'All9','Both FE objects':'The FE object',
        '23 original54020 speeches,five static actors and ten read-only names.153 is progressive Sailor,separate catalogue Retainer,voice4;other four source voices0.28 linear commands,A0008 raw00a0ffff013926a1,C200950,end952. No inferred player identity or relationship. Current V4914 font/guards;native planes need fresh approval.':
        '8 original54020 speeches,two static couple roles164/165,four read-only name consumers and source voice0.12 linear commands,A0008 raw00a0ffff011f22a1,C200426,end428. No inferred marriage,age or kinship. Current V5030 font/guards;native planes need fresh approval.',
        'two original24310null actor then5473C objects:closing impact sound and prospective Artwork/Basra notice.':
        'one original24310null actor then5473C object:prospective Tea/Sofala notice.'}
    import re
    assert all(k in body for k in replacements)
    body=re.sub('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)),lambda m:replacements[m.group(0)],body)
    header='"""Exact B184 source/current commands,two couple roles and progressive/FE consumers."""\n'
    header+='from dataclasses import replace\nfrom pathlib import Path\nimport json\nfrom dk4tool.dialogue.profiles import get_dialogue_profile\nfrom dk4tool.patch.grand_race_menu_release import sha\n'
    header+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({164,165})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    profile=Path('dk4tool/dialogue/lil_B184_profile.py');assert not profile.exists()
    text=header+body;compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B183_layout_v3.py','dk4tool/dialogue/lil_B184_layout_v1.py',{
        'B183':'B184','frozenset({85,110,132,148,153})':'frozenset({164,165})'}))
    tools.append(derive('scripts/plan_lil_B183_layout_v4944.py','scripts/plan_lil_B184_layout_v5050.py',{
        'B183':'B184','lil_B183_layout_v3':'lil_B184_layout_v1','layout_v4944':'layout_v5050',
        'Plan25':'Plan9','all25':'all9','len(reports)==25':'len(reports)==9','plans=25':'plans=9',
        'editorial_manuscript_v6':'editorial_manuscript_v2'}))
    tools.append(derive('scripts/verify_lil_B183_fonts_v4945.py','scripts/verify_lil_B184_fonts_v5051.py',{
        'B183':'B184','lil_B183_layout_v3':'lil_B184_layout_v1','fonts_v4945':'fonts_v5051','voices_v4926':'voices_v5040',
        'editorial_manuscript_v6':'editorial_manuscript_v2',
        'len(cases)==len(qa_reports)==25 and macro_calls==200':'len(cases)==len(qa_reports)==9 and macro_calls==72',
        "sum(c['kind']=='system-FE' for c in cases)==2":"sum(c['kind']=='system-FE' for c in cases)==1",
        'blocks[183]':'blocks[184]','blocks[182]':'blocks[183]',
        'for selector in [85,110,132,148,153,254]':'for selector in [164,165,254]',
        'format(110 if selector==85 else 85':'format(165 if selector==164 else 164',
        "r['source_selector']==85":"r['source_selector']==164",
        "b'\\x55Japanese','{SPEAKER:55}Hello.'":"b'\\xa4Japanese','{SPEAKER:A4}Hello.'",
        'assert len(negatives)==24':'assert len(negatives)==18',
        'all25_progressive_FE_native_planes_and200_alignment_cases':'all9_progressive_FE_native_planes_and72_alignment_cases',
        'current_original_macro_alignment_calls=200,progressive_alignment_calls=184,FE_null_actor_alignment_calls=16':
        'current_original_macro_alignment_calls=72,progressive_alignment_calls=64,FE_null_actor_alignment_calls=8',
        'complete_progressive_planes=23,complete_FE_logical_and_physical_planes=2':'complete_progressive_planes=8,complete_FE_logical_and_physical_planes=1',
        'all_six_selectors_preserved':'all_three_selectors_preserved',
        'B183 current-font progressive/FE planes and200 native alignment cases':'B184 current-font progressive/FE planes and72 native alignment cases',
        'All25 current-font native planes,200 alignment cases and24 source-consumer negatives pass;four sheets need visual review.':
        'All9 current-font native planes,72 alignment cases and18 source-consumer negatives pass;two sheets need visual review.'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        profile_parent=str(parent),profile_parent_sha256=sha(parent.read_bytes()),tools=tools,dependencies=deps,
        inherited_fitting_first_sentence_and_complete_locative_planner_rules=True,
        no_new_phrase_exception_font_width_guard_or_manual_break_change=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
