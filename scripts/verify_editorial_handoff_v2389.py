"""Final scoped audit of49 retentions and zero-credit next battle repair packet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_editorial_handoff_v2342.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'scripts.work_comments_layout_v843 import compiled as cook_compiled':'scripts.gunnery_deck_layout_v887 import compiled as gunnery_compiled',
 'scripts.livestock_prayer_layout_v854 import compiled as livestock_compiled':'scripts.battle_personal_layout_v892 import compiled as battle_compiled',
 'editorial_handoff_verification_v2342':'editorial_handoff_verification_v2389',
 "('cooking',cook_compiled,range(1410,1423)),('livestock_prayer',livestock_compiled,range(1423,1447)),('planning_finance',planning_compiled,range(1447,1471))":"('gunnery_deck',gunnery_compiled,range(1547,1571)),('battle_personal',battle_compiled,range(1571,1596))",
 'set(range(1410,1471))':'set(range(1547,1596))',
 '[1419,1432,1444,1456,1468]':'[1556,1568,1572]',
 "row['speaker']=='Hodram (native captain1)'":"row['speaker']in('Hodram (native captain1)','Hodram')",
 '1495':'1620',
 "':839":"':964",
 'bridge_duties_handoff_v2341':'battle_repair_medical_handoff_v2388',
 'completed_this_turn\']==61':'completed_this_turn\']==49',
 'planning_finance_completion_v2339':'battle_personal_completion_v2386',
 '648':'523',
 '647':'522',
 'V2342-audit-of-V2341':'V2389-audit-of-V2388',
 'completed_this_turn=61,retained=61':'completed_this_turn=49,retained=49',
 'all61':'all49',
 'next28_packet_credit':'next24_packet_credit',
 'next28_credit':'next24_credit'
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/editorial_handoff_verification_v2389/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all49_exact_source_current_integrated_references_and_individual_five_gates_checked=True,all_final_evidence_and_handoff_hashes_checked=True,full_goal_complete=False))
