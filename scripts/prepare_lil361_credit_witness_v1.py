"""Freeze the complete current credit-key set before the B294 context reconstruction."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil361_B283_B298_clean_20261110')


def main():
    out = ROOT / 'preintegration_credit_witness_v1.json'
    assert not out.exists()
    ledgerpath = Path('translations/editorial_review_current_v1.json')
    releasepath = Path('work/lil269_B243_B282_release_v1/registered_release_verification.json')
    ledger, release = map(load, [ledgerpath, releasepath])
    assert ledger['records_editorially_completed'] == 24744 and not ledger['full_goal_complete']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    assert digest(release['candidate']) == release['candidate_sha256']
    keys = ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    credited = {(r['file_path'], r['id']) for r in keys}
    assert len(keys) == len(credited) == 24744
    packetpath = ROOT / 'current_inputs_v1/source_packet.json'
    packet = load(packetpath)
    new = {(r['file_path'], r['id']) for g in packet['groups'] for r in g['records']}
    assert len(new) == 361 and not new.intersection(credited)
    context = next(g for g in packet['groups'] if g['block'] == 294)
    old = [r for r in context['complete_clean_context_records'] if r['covered']]
    assert len(old) == 1 and old[0]['id'] == 'DK4_MES_B294_R0073'
    assert (old[0]['file_path'], old[0]['exact_credited_source_bindings'][0]['id']) in credited
    save(out, dict(format='dk4-preintegration-credit-key-witness-v1',
        contextual_story_natural_dialogue_pass_v1871=dict(integrated_record_keys=keys),
        records_editorially_completed=24744, source_ledger=str(ledgerpath), source_ledger_sha256=digest(ledgerpath),
        source_packet=str(packetpath), source_packet_sha256=digest(packetpath),
        registered_parent=str(releasepath), registered_parent_sha256=digest(releasepath),
        registered_parent_ROM_sha256=release['candidate_sha256'], registry_sha256=release['registry_sha256'],
        exact_complete_credit_key_projection=True, all361_pending_keys_disjoint=True,
        preserved_B294_context=old, new_credit=0, full_goal_complete=False))
    assert load(out)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys'] == keys
    print('PASS frozen24,744 credit keys;361 pending keys disjoint;one B294 context line retained.')


if __name__ == '__main__':
    main()
