"""Prepare independent final35-source/predecessor/integrated provenance audit."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_editorial_handoff_v3344c.py');new=Path('scripts/verify_editorial_handoff_v3377b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'editorial_handoff_verification_v3343b':'editorial_handoff_verification_v3377b','lil_B131_B133_completion_v3342b':'lil_B135_B136_completion_v3376b',
      'lil_B131_B133_registration_v3337b':'lil_B135_B136_registration_v3371b',
      'lil_B131_B133_scope_reconciliation_v3327':'lil_B135_B136_scope_reconciliation_v3361',
      'lil_B131_B133_release_v3339':'lil_B135_B136_release_v3373',
      'lil_B131_B133_startup_v3341/current_B131_B133_scoped_startup_verification.json':'lil_B135_B136_startup_v3375/cold_boot_Lil_startup_town_verification.json',
      'lil_B131_B133_build_v3338':'lil_B135_B136_build_v3372','all-routes-unified-v3338':'all-routes-unified-v3372',
      'lil_B131_B133':'lil_B135_B136','[131,133]':'[135,136]',
      "doc,menu=map(read,[final['manuscript'],final['choices']])":"doc,menu=read(final['manuscript']),{'records':[]}",
      "sum(len(b['choice_commands']) for b in mapping['blocks'])==1":"sum(len(b['choice_commands']) for b in mapping['blocks'])==0",
      "padding['all1_final2100_object_two_labels_and3_selection_cancel_cases_bound']":"padding['no2100_objects_in_source_scope']",
      "padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']":"padding['all35_final_speech_prefixes_and_nonempty_bodies_preserved']",
      'equal_V3300':'equal_V3338','actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs',
      'unfinished_editorial_scope_v3342':'unfinished_editorial_scope_v3376','unfinished_editorial_scope_v3327':'unfinished_editorial_scope_v3361',
      'V3342':'V3376','B135_B140':'B137_B140',
      'all63_exact_source_predecessor_effective_integrated_references_verified':'all35_exact_source_predecessor_effective_integrated_references_verified',
      'all61_speech_planes_two_labels_source00_and_all_release_gates_verified':'all35_speech_planes_and_all_release_gates_verified',
      'all10_native_sheets_and_current6frame_sheet_reviewed':'all5_native_sheets_and_current6frame_sheet_reviewed',
      "len(font['cases'])==61":"len(font['cases'])==35","len(padding['final_target_parity_cases'])==61":"len(padding['final_target_parity_cases'])==35",
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    counts={4797:4832,4800:4835,3169:3185,1628:1647,2970:3005,3198:3233,63:35,27:16,36:19,521:522,112:61,24:4,120:20,488:280,244:140,19:15,28:14,22:21,50:28}
    t=re.sub(r'(?<!\d)(4797|4800|3169|1628|2970|3198|63|27|36|521|112|24|120|488|244|19|28|22|50)(?!\d)',lambda m:str(counts[int(m[0])]),t)
    t=t.replace("len(font['review_sheets'])==10","len(font['review_sheets'])==5")
    a=t.index('    fe,control,typed=');z=t.index('    assert sample[',a)
    t=t[:a]+"""    control=read(doc['relocated_control_proof'])
    assert len(control['relocated_dispatch_cases'])==35 and len(control['relocated_predicate_pairs'])==1 and control['original_event_queries']==[] and control['all_six_static_speaker_selectors_preserved_without_role_assignment']
    assert all(r['source_selector'] in {2,9,14,36,47,96} and r['kind']=='progressive' and b'\\0' not in bytes.fromhex(r['integrated_hex']) for r in rows)
"""+t[z:]
    t=t[:t.rindex('    print(')]+"    print('IndependentV3376audit passes:35completed,4832reread/integrated,4835source-prose;522batches/114layers/exactpatch/31freshframepairs. Fullwidergoal active.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B136_audit_tools_v3377');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
