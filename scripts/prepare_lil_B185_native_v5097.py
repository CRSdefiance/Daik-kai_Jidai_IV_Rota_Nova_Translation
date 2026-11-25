"""Freeze B185's exact roles,eleven commands and measured display geometry."""
from pathlib import Path
import re
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B185_native_tools_v5097')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B185_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract',
        'actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    parent=Path('dk4tool/dialogue/lil_B184_profile.py');text=parent.read_text(encoding='utf-8');body=text[text.index('def profile_for('):]
    changes={'B184':'B185','len(cases)!=18':'len(cases)!=16','All9':'All8',
        '8 original54020 speeches':'7 original54020 speeches','12 linear commands':'11 linear commands','00a0ffff011f22a1':'00a0ffff013807a1',
        'C200426,end428':'C200382,end384','Current V5030':'Current V5076','Tea/Sofala':'Furs/Stockholm'}
    assert all(k in body for k in changes)
    body=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],body)
    header='"""Exact B185 source/current commands,two couple roles and progressive/FE consumers."""\n'
    header+='from dataclasses import replace\nfrom pathlib import Path\nimport json\nfrom dk4tool.dialogue.profiles import get_dialogue_profile\nfrom dk4tool.patch.grand_race_menu_release import sha\n'
    header+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({164,165})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    profile=Path('dk4tool/dialogue/lil_B185_profile.py');assert not profile.exists();text=header+body
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    tools=[derive('dk4tool/dialogue/lil_B184_layout_v1.py','dk4tool/dialogue/lil_B185_layout_v1.py',{'B184':'B185'}),
        derive('scripts/plan_lil_B184_layout_v5050.py','scripts/plan_lil_B185_layout_v5098.py',{
            'B184':'B185','layout_v5050':'layout_v5098','Plan9':'Plan8','all9':'all8','len(reports)==9':'len(reports)==8','plans=9':'plans=8'}),
        derive('scripts/verify_lil_B184_fonts_v5051.py','scripts/verify_lil_B185_fonts_v5099.py',{
            'B184':'B185','fonts_v5051':'fonts_v5099','voices_v5040':'voices_v5088',
            'len(cases)==len(qa_reports)==9 and macro_calls==72':'len(cases)==len(qa_reports)==8 and macro_calls==64',
            'blocks[184]':'blocks[185]','blocks[183]':'blocks[184]',
            'all9_progressive_FE_native_planes_and72_alignment_cases':'all8_progressive_FE_native_planes_and64_alignment_cases',
            'current_original_macro_alignment_calls=72,progressive_alignment_calls=64,FE_null_actor_alignment_calls=8':
            'current_original_macro_alignment_calls=64,progressive_alignment_calls=56,FE_null_actor_alignment_calls=8',
            'complete_progressive_planes=8':'complete_progressive_planes=7',
            'B184 current-font progressive/FE planes and72 native alignment cases':'B185 current-font progressive/FE planes and64 native alignment cases',
            'All9 current-font native planes,72 alignment cases and18 source-consumer negatives pass;two sheets need visual review.':
            'All8 current-font native planes,64 alignment cases and18 source-consumer negatives pass;one sheet needs visual review.'})]
    ROOT.mkdir(parents=True);save(ROOT/'prepared_source_bound_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),
        profile_parent=str(parent),profile_parent_sha256=sha(parent.read_bytes()),tools=tools,dependencies=deps,
        no_inheritance_of_B184_tea_exact_paragraph_boundary_exception=True,no_new_phrase_exception_font_width_guard_or_manual_break_change=True,
        new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
