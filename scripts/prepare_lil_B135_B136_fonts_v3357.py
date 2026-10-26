"""Prepare full progressive native planes andsource-consumer negatives."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_lil_B131_B133_fonts_v3319.py');new=Path('scripts/verify_lil_B135_B136_fonts_v3357b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={'lil_B131_B133_profile':'lil_B135_B136_profile','lil_B131_B133_layout_v1':'lil_B135_B136_layout_v1','lil_B131_B133_fonts_v3319':'lil_B135_B136_fonts_v3357b','lil_B131_B133_editorial_manuscript_v2':'lil_B135_B136_editorial_manuscript_v2','len(cases)==60 and len(qa_reports)==61 and macro_calls==480':'len(cases)==35 and len(qa_reports)==35 and macro_calls==280','all61_complete_source_speech_prefixes_preserved':'all35_complete_source_speech_prefixes_preserved','all61_full_QA_reports':'all35_full_QA_reports','current_original_macro_alignment_calls=480':'current_original_macro_alignment_calls=280','all60_progressive_full_QA_and_complete_native_fonts_pass':'all35_progressive_full_QA_and_complete_native_fonts_pass','all60_painted_consumers_original_progressive54020':'all35_painted_consumers_original_progressive54020','FE_body_QA_is_conservative_plan_only=True':'no_FE_or_choice_objects_in_this_source_scope=True','one_FE_and_two_two_option_labels_separately_required=True':'all35_speeches_share_original_progressive_consumer=True','actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    a=t.index("    reject('mutated-runtime'");z=t.index('    sheets=[]',a)
    t=t[:a]+"""    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[135]))
    reject('unrelated-source-block',lambda:profile_for(arm,blocks[134]))
    reject('mutated-source-block',lambda:profile_for(arm,blocks[135][:-1]+bytes([blocks[135][-1]^1])))
    progressive=profile_for(arm,blocks[135]);selectors=[2,9,14,36,47,96]
    for selector in selectors:
        row=next(r for r in doc['records'] if r['source_selector']==selector)
        tag='{SPEAKER:'+format(selector,'02X')+'}';alternate='{SPEAKER:'+format(9 if selector==2 else 2,'02X')+'}'
        reject('missing-'+format(selector,'02X')+'-actor-state',lambda r=row,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),progressive))
        reject('wrong-legal-'+format(selector,'02X')+'-actor-state',lambda r=row,t=tag,v=alternate:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,v),progressive))
    plain=next(r for r in doc['records'] if '{MACRO:' not in r['english'])
    reject('invented-native-macro',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:FI}',progressive))
    reject('manual-layout',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{LB}',progressive))
    reject('embedded-NUL',lambda:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+'{HEX:00}',progressive))
    reject('source00-outside-scope',lambda:encode_relocatable_dialogue(bytes([0])+b'Japanese','{SPEAKER:00}Hello.',progressive))
    reject('FE-outside-scope',lambda:encode_relocatable_dialogue(bytes([254])+b'Japanese','{SPEAKER:FE}Hello.',progressive))
    reject('FE-profile-outside-scope',lambda:profile_for(arm,blocks[135],'FE-paper'))
    assert len(negatives)==21
"""+t[z:]
    t=t[:t.rindex('    print(')]+"    print('35 complete progressive planes,280macro alignments,35QA plans and21 source-consumer negatives pass;five sheets require visual review. No gameplay orcredit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B136_font_tools_v3357');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
