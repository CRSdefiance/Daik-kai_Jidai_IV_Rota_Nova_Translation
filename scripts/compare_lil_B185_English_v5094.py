"""Expose the entire predecessor exchange after clean context and terms are bound."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B185_comparison_v5094')
SOURCE=Path('work/analysis/lil_B185_source_v5087/all8_clean_current_complete_context.json')
TERMS=Path('work/analysis/lil_B185_terms_v5093/two_couple_roles_Stockholm_Furs_and_reported_sales_prices_reconciliation.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);terms=read(TERMS)
    assert terms['source_context_sha256']==sha(SOURCE.read_bytes())
    proofs=[Path('work/analysis/lil_B185_voices_v5088/current207_catalog_eight_voices_and_two_source_selectors.json'),
        Path('work/analysis/lil_B185_dispatches_v5089/all8_source_current_dispatches_no_macros_and3_control_leaves.json'),
        Path('work/analysis/lil_B185_names_v5092/four_original_progressive_and_catalogue_name_consumers.json'),
        Path('work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json'),TERMS]
    for p in proofs:assert read(p)['source_context_sha256']==sha(SOURCE.read_bytes())
    rows=[]
    for r in packet['records']:
        old=bytes.fromhex(r['current_hex']);assert old[0]==r['source_selector']
        body=old[1:].decode('cp932');row=deepcopy(r)
        row.update(previous_display_body=body,previous_paragraph=' '.join(body.split()),previous_bytes_retained_for_exact_comparison=True)
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'all8_complete_clean_and_predecessor_exchange.json',dict(candidate=packet['current_ROM'],
        candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        terms=str(TERMS),terms_sha256=sha(TERMS.read_bytes()),records=rows,
        prior_complete_Japanese_glosses_names_voices_controls_and_terms_bound=True,
        predecessor_is_comparison_material_not_translation_source=True,
        individual_contextual_editorial_decisions_and_native_layout_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,*proofs]},new_editorial_credit=0,full_goal_complete=False))
    for r in rows:
        print(r['id'],r['source_selector'])
        print('JP:',r['source_Japanese'].replace('\n',' / '))
        print('CURRENT:',repr(r['previous_paragraph']))
