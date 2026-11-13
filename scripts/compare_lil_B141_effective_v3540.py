"""Produce complete source/current comparisons only after all14 fresh glosses exist."""
from pathlib import Path
import unicodedata
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_comparison_v3540')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B141_clean_context_v3534/all14_complete_clean_context_and_fresh_glosses.json')
DISPATCH=Path('work/analysis/lil_B141_controls_v3538b/all14_source_current_dispatches_FI_C200_and630A_contract.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,gloss,dispatch=map(read,[SOURCE,GLOSS,DISPATCH]);byid={r['id']:r for r in gloss['records']};cases={r['id']:r for r in dispatch['speech_dispatch_cases'] if r['version']=='current-English'};assert len(byid)==len(cases)==14;rows=[];text=[]
    for r in packet['records']:
        c=cases[r['id']];raw=bytes.fromhex(r['current_hex'])[1:];effective=bytes.fromhex(c['boundaries'][1]['text_hex']);stored=raw.decode('cp932');runtime=effective.decode('cp932');paragraph=' '.join(unicodedata.normalize('NFKC',runtime).split())
        rows.append({**r,'fresh_source_gloss':byid[r['id']]['fresh_source_gloss'],'whole_exchange_context':gloss['whole_exchange_context'],'current_raw_storage_English':stored,'current_effective_runtime_English':runtime,'effective_predecessor_paragraph':paragraph,'registered_runtime_catalog_entry':c['registered_catalog_match'],'current_effective_hex':effective.hex(),'source_gloss_precedes_older_English_comparison':True})
        text.append(r['id']+' /selector'+format(r['source_selector'],'02X')+'\nJP: '+r['source_Japanese']+'\nFresh gloss: '+byid[r['id']]['fresh_source_gloss']+'\nCurrent effective: '+paragraph+'\n')
    ROOT.mkdir(parents=True);tp=ROOT/'B141_complete_source_and_current_effective.txt';tp.write_text('\n'.join(text),encoding='utf-8')
    save(ROOT/'all14_current_effective_comparison_packet.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fresh_glosses=str(GLOSS),fresh_glosses_sha256=sha(GLOSS.read_bytes()),records=rows,registered_runtime_catalog_replacement_count=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),complete_comparison_text=str(tp),complete_comparison_text_sha256=sha(tp.read_bytes()),meaning_tone_localization_and_retention_decisions_still_pending=True,source_million_threshold_and900000_payment_separate_from_opaque630A=True,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(complete_comparison_records=14,runtime_catalog_replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows),new_credit=0))
