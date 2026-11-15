"""Final scoped audit of76 fresh retentions and the zero-credit Gunnery/Deck packet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_editorial_handoff_v2342.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'scripts.work_comments_layout_v843 import compiled as cook_compiled':'scripts.bridge_duties_layout_v869 import compiled as bridge_compiled',
 'scripts.livestock_prayer_layout_v854 import compiled as livestock_compiled':'scripts.survey_lookout_layout_v875 import compiled as survey_compiled',
 'scripts.planning_finance_layout_v860 import compiled as planning_compiled':'scripts.sails_boarding_layout_v881 import compiled as sails_compiled',
 'editorial_handoff_verification_v2342':'editorial_handoff_verification_v2370',
 "('cooking',cook_compiled,range(1410,1423)),('livestock_prayer',livestock_compiled,range(1423,1447)),('planning_finance',planning_compiled,range(1447,1471))":"('bridge_duties',bridge_compiled,range(1471,1499)),('survey_lookout',survey_compiled,range(1499,1523)),('sails_boarding',sails_compiled,range(1523,1547))",
 'set(range(1410,1471))':'set(range(1471,1547))',
 '[1419,1432,1444,1456,1468]':'[1472,1484,1496,1508,1520,1532,1544]',
 '1495':'1571',
 "':839":"':915",
 'bridge_duties_handoff_v2341':'gunnery_deck_handoff_v2369',
 'completed_this_turn\']==61':'completed_this_turn\']==76',
 'planning_finance_completion_v2339':'sails_boarding_completion_v2367',
 '648':'572',
 '647':'571',
 'V2342-audit-of-V2341':'V2370-audit-of-V2369',
 'completed_this_turn=61,retained=61':'completed_this_turn=76,retained=76',
 'all61':'all76',
 'next28_packet_credit':'next24_packet_credit',
 'next28_credit':'next24_credit'
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/editorial_handoff_verification_v2370/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all76_source_current_integrated_references_and_five_gate_reviews_checked=True,all_final_evidence_and_handoff_hashes_checked=True,full_goal_complete=False))
