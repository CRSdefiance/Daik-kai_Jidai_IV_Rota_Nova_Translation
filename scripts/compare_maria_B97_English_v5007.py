"""Compare all32 current outputs only after clean-first glosses and native bindings."""
from pathlib import Path
import unicodedata
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_comparison_v5007')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
GLOSS=Path('work/analysis/maria_B97_clean_glosses_v4996/all32_clean_exchange_and_fresh_glosses.json')
DISPATCH=Path('work/analysis/maria_B97_dispatches_v5001/all32_clean_current_Maria_dispatches_FE_and_FO.json')
TERMS=Path('work/analysis/maria_B97_terms_v5006/bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,gloss,dispatch,terms=map(read,[SOURCE,GLOSS,DISPATCH,TERMS]);byindex={r['source_record_index']:r for r in gloss['records']};cases={r['id']:r for r in dispatch['speech_dispatch_cases'] if r['version']=='current-English'};assert len(byindex)==len(cases)==32 and gloss['read_no_predecessor_English'];rows=[];text=[]
    for r in packet['records']:
        c=cases[r['id']];boundary=[b for b in c['boundaries'] if 'text_hex' in b];assert len(boundary)==1
        raw=bytes.fromhex(r['current_hex'])[1:];effective=bytes.fromhex(boundary[0]['text_hex']);stored=raw.decode('cp932');runtime=effective.decode('cp932');paragraph=' '.join(unicodedata.normalize('NFKC',runtime).split())
        rows.append(dict(r,current_raw_storage_English=stored,current_effective_runtime_English=runtime,effective_predecessor_paragraph=paragraph,current_effective_hex=effective.hex(),registered_runtime_catalog_entry=c['registered_catalog_match'],source_gloss_precedes_predecessor_comparison=True,whole_exchange_progression=gloss['complete_exchange_progression']))
        text.append(r['id']+' /selector'+format(r['source_selector'],'02X')+'\nJP: '+r['source_Japanese']+'\nFresh gloss: '+byindex[r['source_record_index']]['fresh_source_gloss']+'\nCurrent effective: '+paragraph+'\n')
    assert sum(r['registered_runtime_catalog_entry'] is not None for r in rows)==0
    ROOT.mkdir(parents=True);tp=ROOT/'B97_complete_source_and_current_effective.txt';tp.write_text('\n'.join(text),encoding='utf-8')
    save(ROOT/'all32_current_effective_comparison_packet.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fresh_glosses=str(GLOSS),fresh_glosses_sha256=sha(GLOSS.read_bytes()),records=rows,registered_runtime_catalog_replacement_count=0,complete_comparison_text=str(tp),complete_comparison_text_sha256=sha(tp.read_bytes()),macro_template_and_native_expanded_current_Li_Clan_output_distinguished=True,editorial_decisions_and_all_display_release_gates_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,DISPATCH,TERMS,Path(__file__)]},new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('32 complete source/current comparisons;one real FO expanded by current native consumer,no runtime catalogue replacement,zero credit.')
