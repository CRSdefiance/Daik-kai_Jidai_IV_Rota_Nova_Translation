"""Current code/text/pixel binding of8 historical Galley/Livestock holds and4 returns."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/rebind_battle_repair_medical_history_v2394.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'dk4tool.patch.battle_repair_medical_editorial':'dk4tool.patch.battle_cooking_livestock_editorial',
 'scripts.battle_repair_medical_flags_v905':'scripts.battle_cooking_livestock_flags_v911',
 'from scripts.verify_battle_repair_medical_gameplay_v905 import CASES':"from scripts.verify_battle_cooking_livestock_gameplay_v911 import SPECS\nfrom scripts.verify_village_wrap_v608 import read as plan_read\nPLAN=plan_read('work/analysis/battle_cooking_livestock_v911/actual_sample_frame_plan.json')['cases']\nCASES={label:(n,actor,role,PLAN[label]['baseline'],tuple(PLAN[label]['holds']),PLAN[label]['first_back'],PLAN[label]['end'])for label,(n,actor,role,owned)in SPECS.items()}",
 'scripts.battle_repair_medical_layout_v902':'scripts.battle_cooking_livestock_layout_v908',
 'battle_repair_medical_history_v2394':'battle_cooking_livestock_history_v2401',
 'battle_repair_medical_v905/actual_gameplay_verification.json':'battle_cooking_livestock_v911/actual_gameplay_verification.json',
 'translations/battle_repair_medical_contextual':'translations/battle_cooking_livestock_contextual',
 'synthetic_battle_repair_medical_Cabin_assignment_fixtures':'synthetic_battle_cooking_livestock_Cabin_assignment_fixtures',
 "label in('CaptainRepair','ManuelMedical')":"SPECS[label][3]",
 "label=='ManuelMedical'":"label=='CaptainGalley'",
 'V904':'V910',
 "cells={'ClaudioRepair':[(0,35,'deleted-final-period-at-full36')],'CaptainRepair':[(1,0,'deleted-leading-I-after-odd25')],'CamilleMedical':[(0,0,'deleted-initial-ASCII-I')],'ManuelMedical':[(0,35,'deleted-final-period-at-full36'),(1,0,'deleted-leading-C-continuation')]}[label]":"lines=layout(row['english']);cells=[(0,0,'deleted-initial-glyph'),(len(lines)-1,len(lines[-1])-1,'deleted-final-punctuation')]+([(1,0,'deleted-continuation-I')]if label=='Voice1Livestock'else[])",
 '{1600,1605,1610,1615}':'{1629,1632,1634,1639}',
 '[1600,1605,1610,1615]':'[1629,1632,1634,1639]',
 'len(controls)==9':'len(controls)==13',
 'historical_battle_repair_medical8_sheet.png':'historical_battle_cooking_livestock8_sheet.png',
 'all24_complete_payloads_exact_to_historical_V910':'all25_complete_payloads_exact_to_historical_V910',
 'nine_negative_controls_current_reexecution_on_offline_clones':'thirteen_negative_controls_current_reexecution_on_offline_clones',
 'all24_current_native_fonts_separate':'all25_current_native_fonts_separate',
 'work/analysis/battle_repair_medical_fonts_v2393/all24_current_native_fonts.json':'work/analysis/battle_cooking_livestock_fonts_v2400/all25_current_native_fonts.json',
 'negative_controls=9':'negative_controls=13'
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_cooking_livestock_history_v2401/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all8_current_native_selector_parent_bitmap_RGB_checks_on_historical_RAM_preserved=True,all4_returns_and13_negative_controls_checked=True,registered_v2_parser_binds_preserved_V910_input=True,no_new_current_battle_gameplay_claim=True,full_goal_complete=False))
