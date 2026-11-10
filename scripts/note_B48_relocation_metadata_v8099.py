"""Preserve a stale historical metadata label as a scoped later-re-audit lead,no ROM changes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_relocation_metadata_v8099')
MAP=Path('work/analysis/Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json')
PRODUCTION=Path('work/analysis/Rafael_B48_atomic_positive_v8063/positive_reconstruction.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,source,production=map(read,[MAP,SOURCE,PRODUCTION]);before=sha(MAP.read_bytes());group=mapping['groups'][0]
    key='all15_six_byte_preambles_zero_macros_selectors_complete_terminal_andseparate_tails_preserved'
    assert mapping[key] is True and len(group['text_records'])==91
    macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in source['groups'][0]['records']) for m in ['FI','FA','FO']}
    assert macro_counts==dict(FI=1,FA=0,FO=0) and len(production['changed_records'])==91
    assert production['one_files_list_commit_after_all_gates'] and production['all91_preambles163_commands28_relatives_five_predicates_two_queries_andfull_end_preserved']
    ROOT.mkdir(parents=True)
    save(ROOT/'historical_root_label_stale_actual91_records_oneFI_authoritative_arrays_unchanged.json',dict(
        historical_mapping=str(MAP),historical_mapping_sha256=before,stale_label=key,stale_label_value=True,
        finding='The inherited root key still names15/zero macros. Actual arrays andsource-bound production prove91 B48 speeches andone FI. Treat that key as a stale diagnostic label,not an accurate numeric summary.',
        corrected_record_count=91,corrected_source_macro_counts=macro_counts,authoritative_production=str(PRODUCTION),authoritative_production_sha256=sha(PRODUCTION.read_bytes()),
        no_historical_file_code_contract_orROM_mutated=True,no_release_correctness_claim_from_stale_label=True,
        retain_for_later_older_record_technical_reaudit_without_replaying_B48=True,
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,SOURCE,PRODUCTION,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    assert sha(MAP.read_bytes())==before
    print('HistoricalB48 root label preserved asstale diagnostic;actual91records/oneFI andindependent production checks bound. Latertechnicalre-audit lead;no rerun/credit/ROM change.')
