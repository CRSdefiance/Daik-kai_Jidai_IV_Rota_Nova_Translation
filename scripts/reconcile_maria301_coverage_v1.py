"""Extend the exact SC3 census with the301 newly registered bindings; no native inventory replay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.reconcile_rafael_source_coverage_v1 import source_location

ROOT = Path('work/story_source_coverage_20261109_SC3_v2')
PRIOR = Path('work/story_source_coverage_20261109_SC3_v1/coverage.json')
FINAL = Path('translations/maria301_integrated_final_review_v1.json')
RELEASE = Path('work/maria301_release_v1/registered_release_verification.json')
LEDGER = Path('translations/editorial_review_current_v1.json')


def main():
    assert not ROOT.exists()
    prior,doc,release,ledger = map(load,[PRIOR,FINAL,RELEASE,LEDGER])
    assert digest('translations/release_stack.json') == release['registry_sha256']
    assert len(prior['records']) == 5129 and len(prior['missing']) == 4932
    assert not prior['inventory_failures'] and not prior['legacy_source_bindings_not_exact']
    assert doc['target_ROM_sha256'] == release['candidate_sha256'] and doc['all301_individual_five_gates_pass']
    clean = NdsImage.open(prior['source_ROM']); archive = clean.read_file('/data/SC3.DK4')
    assert digest(prior['source_ROM']) == prior['source_ROM_sha256'] and sha(archive) == prior['source_archive_sha256']
    blocks = IlnkContainer.parse(archive).blocks
    keys = {(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys'] if r['file_path']=='/data/SC3.DK4'}
    family = ledger['Maria_SC3_B0_B32_clean_20261109']['completed_in_combined_family']
    fresh = {source_location(r):r for r in doc['records']};assert len(fresh) == 301
    records = deepcopy(prior['records']);added = []
    for row in records:
        ref = row['source_reference'];location = (row['block'],ref['offset'],row['source_hex'])
        raw = bytes.fromhex(row['source_hex'])
        assert blocks[row['block']][ref['offset']:ref['offset']+len(raw)] == raw
        if location in fresh:
            new = fresh[location];assert not row['covered']
            assert new['file_path'] == row['file_path'] and new['id'] == row['id'] and all(new['review'].values())
            row['exact_credited_source_bindings'] = [dict(id=new['id'],family=family,block=row['block'],offset=ref['offset'],source_hex=row['source_hex'])]
            row['covered'] = True;added.append(new['id'])
        assert all((row['file_path'],r['id']) in keys for r in row['exact_credited_source_bindings'])
    assert len(added) == len(set(added)) == 301
    missing = [r for r in records if not r['covered']]
    matched = {(r['file_path'],b['id']) for r in records for b in r['exact_credited_source_bindings']}
    assert matched == keys and len(keys) == 498 and len(missing) == 4631
    old_packet_path = PRIOR.with_name('residual_clean_source_packet.json');packet = load(old_packet_path)
    bypos = {(r['block'],r['source_reference']['offset'],r['source_hex']):r for r in records}
    groups = []
    for g in packet['groups']:
        rows = [deepcopy(bypos[(r['block'],r['source_reference']['offset'],r['source_hex'])]) for r in g['records']]
        assert bytes.fromhex(g['clean_block_hex']) == blocks[g['block']]
        if any(not r['covered'] for r in rows):
            assert all(not r['covered'] for r in rows),'Next intake must account for a partially credited exchange'
            groups.append({**g,'records':rows,'missing_source_objects':len(rows)})
    assert sum(len(g['records']) for g in groups) == len(missing)
    ROOT.mkdir()
    save(ROOT/'coverage.json',dict(source_ROM=prior['source_ROM'],source_ROM_sha256=prior['source_ROM_sha256'],
        source_archive_sha256=prior['source_archive_sha256'],release=str(RELEASE),release_sha256=digest(RELEASE),
        ledger=str(LEDGER),ledger_sha256=digest(LEDGER),blocks=len(blocks),object_counts=prior['object_counts'],
        records=records,missing=missing,inventory_failures=[],legacy_source_bindings_not_exact=[],
        previous_exact_bindings_reused=197,new_exact_bindings=301,
        prior_census=str(PRIOR),prior_census_sha256=digest(PRIOR),
        all_clean_source_positions_rechecked=True,native_inventory_exact_clean_dependency_reuse_not_replayed=True,
        dialogue_typed_styles_only_not_full_player_facing_or_reachability_census=True,
        numeric_adjacency_not_conversation_chronology=True,no_credit_or_ROM_mutation=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [PRIOR,old_packet_path,FINAL,RELEASE,LEDGER,Path(__file__)]}))
    save(ROOT/'residual_clean_source_packet.json',{**packet,'groups':groups,'records':len(missing),
        'complete_native_inventory_reused_not_rerun':True,'new_credit':0})
    print('SC3 census:498 exact reviewed objects,4631 remaining; all5129 source positions checked,zero duplicate credit.')
    print('First remaining exchanges:',[(g['block'],len(g['records'])) for g in groups[:16]])


if __name__ == '__main__':main()
