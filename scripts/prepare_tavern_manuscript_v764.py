"""Correct a provider-role label without changing the reviewed English drafts."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

SOURCE = Path('translations/tavern_conversations_editorial_manuscript_v1.json')
TARGET = Path('translations/tavern_conversations_editorial_manuscript_v2.json')


def main():
    assert not TARGET.exists()
    before = read(SOURCE); doc = deepcopy(before)
    inventory = Path('work/analysis/tavern_storage_v764/actual_native_person_arguments.json')
    evidence = read(inventory)
    assert evidence['source_ROM_sha256'] == doc['current_ROM_sha256']
    for row in doc['records']:
        if row['message_id'] not in (820, 821): continue
        assert row['runtime_argument_contract'][0] == 'person_full_name'
        row['runtime_argument_contract'][0] = 'native_person_name'
        row['localization_note'] += ' Original virtual+24 supplies the native person name: the ordinary implementation reads the surname table member+4. Preserve the actual class getter and current-admiral special-object resolution; do not synthesize a full name.'
        row['native_binding']['person_name_provider_evidence'] = str(inventory)
    doc['provider_role_correction'] = {'prior_manuscript': str(SOURCE), 'sha256': sha(SOURCE.read_bytes()),
        'evidence': str(inventory), 'evidence_sha256': sha(inventory.read_bytes()),
        'all31_English_paragraphs_unchanged': True,
        'note': 'Correct the V763 full-name metadata assumption. Actual current20 company leader names are surnames. Unclassified ordinary/generic table slots do not establish rumor eligibility.'}
    assert [r['english'] for r in doc['records']] == [r['english'] for r in before['records']]
    assert all(not r['review']['formatting'] for r in doc['records'])
    save(TARGET, doc)
    print('V2: actual native person-name contract recorded;31 English drafts unchanged;formatting approval still false.', flush=True)


if __name__ == '__main__': main()
