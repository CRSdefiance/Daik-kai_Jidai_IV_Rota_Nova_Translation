"""Bind8 historical Chapel/Planning holds,4 returns and14 glyph/header controls."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/rebind_battle_repair_medical_history_v2394.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'dk4tool.patch.battle_repair_medical_editorial':'dk4tool.patch.battle_chapel_planning_editorial',
 'scripts.battle_repair_medical_flags_v905':'scripts.battle_chapel_planning_flags_v917',
 'from scripts.verify_battle_repair_medical_gameplay_v905 import CASES':"from scripts.verify_battle_chapel_planning_gameplay_v917 import SPECS\nfrom scripts.verify_village_wrap_v608 import read as plan_read\nPLAN=plan_read('work/analysis/battle_chapel_planning_v917/actual_sample_frame_plan.json')['cases']\nCASES={label:(n,actor,role,PLAN[label]['baseline'],tuple(PLAN[label]['holds']),PLAN[label]['first_back'],PLAN[label]['end'])for label,(n,actor,role,owned)in SPECS.items()}",
 'scripts.battle_repair_medical_layout_v902':'scripts.battle_chapel_planning_layout_v914',
 'battle_repair_medical_history_v2394':'battle_chapel_planning_history_v2410',
 'battle_repair_medical_v905/actual_gameplay_verification.json':'battle_chapel_planning_v917/actual_gameplay_verification.json',
 'translations/battle_repair_medical_contextual_editorial_manuscript_v1.json':'translations/battle_chapel_planning_contextual_editorial_manuscript_v1b.json',
 'synthetic_battle_repair_medical_Cabin_assignment_fixtures':'synthetic_battle_chapel_planning_Cabin_assignment_fixtures',
 "label in('CaptainRepair','ManuelMedical')":"SPECS[label][3]",
 "(0x0C04 if label=='ManuelMedical'else 0x0E04)":"0x0E04 ",
 'V904':'V916',
 "cells={'ClaudioRepair':[(0,35,'deleted-final-period-at-full36')],'CaptainRepair':[(1,0,'deleted-leading-I-after-odd25')],'CamilleMedical':[(0,0,'deleted-initial-ASCII-I')],'ManuelMedical':[(0,35,'deleted-final-period-at-full36'),(1,0,'deleted-leading-C-continuation')]}[label]":"lines=layout(row['english']);cells=[(0,0,'deleted-initial-glyph'),(len(lines)-1,len(lines[-1])-1,'deleted-final-punctuation')]+([(2,0,'deleted-third-row-M')]if label=='EmilioPlanning'else[(1,0,'deleted-Marine-request-initial-A')]if label=='CaptainPlanning'else[])",
 '{1600,1605,1610,1615}':'{1648,1654,1663,1666}',
 '[1600,1605,1610,1615]':'[1648,1654,1663,1666]',
 'len(controls)==9':'len(controls)==14',
 'historical_battle_repair_medical8_sheet.png':'historical_battle_chapel_planning8_sheet.png',
 'nine_negative_controls':'fourteen_negative_controls',
 'work/analysis/battle_repair_medical_fonts_v2393':'work/analysis/battle_chapel_planning_fonts_v2409',
 'negative_controls=9':'negative_controls=14',
 "flags_preserved=['0E04','0C04']":"flags_preserved=['0E04']",
 'observed0E04_and0C04_flags_preserved_low_byte4_not_rewritten':'observed0E04_flags_preserved_low_byte4_not_rewritten'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_chapel_planning_history_v2410/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all8_historical_holds_and4_returns_freshly_checked_with_current_code_and_text=True,all14_offline_negative_controls_rejected=True,no_new_current_battle_emulator_run_claim=True,full_goal_complete=False))
