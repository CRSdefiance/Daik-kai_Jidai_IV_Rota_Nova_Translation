"""Bind typed options to canonical clean-source NUL-selection IDs and prove all sixteen units are uncredited."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_choice_binding_v8387b')
CURRENT=Path('work/analysis/Hodram_B49_current_v8387/current_effective.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();original=read(CURRENT);packet=deepcopy(original);ledger=read(LEDGER);assert ledger['records_editorially_completed']==7205 and len(packet['records'])==14 and len(packet['typed_choices'])==1
    group=packet['groups'][0];clean,current=[bytes.fromhex(group[k]) for k in ['clean_block_hex','current_block_hex']];keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']};menu=packet['typed_choices'][0]
    for row in menu['records']:
        sr,cr=row['source_reference'],row['current_reference'];si=clean[:sr['offset']].count(b'\0');ci=current[:cr['offset']].count(b'\0');raw=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex']);assert clean[sr['offset']:sr['offset']+len(raw)+1]==raw+b'\0' and current[cr['offset']:cr['offset']+len(old)+1]==old+b'\0'
        row.update(previous_inventory_alias=row['id'],id=f'DK4_MES_B49_R{si:04d}',source_record_index=si,current_record_index=ci,kind='typed-choice',source_kind='typed-choice',source_typed_command_hex=menu['source_command']['whole_command_hex'],current_typed_command_hex=menu['current_command']['whole_command_hex'],source_choice_command_offset=sr['command_offset'],current_choice_command_offset=cr['command_offset'],current_raw_storage_English=row['current_English'],current_effective_paragraph=' '.join(row['current_English'].split()),current_storage_trailing_ASCII_spaces=len(row['current_English'])-len(row['current_English'].rstrip(' ')),source_prose_orcompletion_credit_added=False)
        sr.update(file_path='/data/SC1.DK4',record_index=si,header_offset=sr['command_offset'],option_index=row['option_index']);cr.update(file_path='/data/SC1.DK4',record_index=ci,header_offset=cr['command_offset'],option_index=row['option_index'])
    assert [r['id'] for r in menu['records']]==['DK4_MES_B49_R0048','DK4_MES_B49_R0050'];allrows=packet['records']+menu['records'];assert len(allrows)==len({historical_key(r) for r in allrows})==16 and not keys&{historical_key(r) for r in allrows}
    packet.update(previous_packet=str(CURRENT),previous_packet_sha256=sha(CURRENT.read_bytes()),typed_choices_canonical_clean_record_IDs_bound=True,all16_source_units_uncredited_in_current_ledger=True,physical_speeches=14,typed_choice_labels=2,total_editorial_objects=16,ledger_sha256=sha(LEDGER.read_bytes()),canonical_choice_IDs_not_new_alias_coverage_credit=True,new_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(ROOT/'current_with_choices.json',packet);save(ROOT/'binding.json',dict(previous=str(CURRENT),previous_sha256=sha(CURRENT.read_bytes()),current=str(ROOT/'current_with_choices.json'),current_sha256=sha((ROOT/'current_with_choices.json').read_bytes()),canonical_choice_IDs=[r['id'] for r in menu['records']],all16_uncredited=True,all14_speech_records_dispatches_controls_andnative_results_unchanged=packet['records']==original['records'] and packet['groups']==original['groups'] and packet['all28_source_current_dispatches_in_new_own8377_context']==original['all28_source_current_dispatches_in_new_own8377_context'],new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('B49:14speeches+2canonical choices R0048/R0050=16disjoint uncredited units;old inventoryaliases preserved.ChoiceNo. has3storage-only spaces;logical wording unchanged.')
