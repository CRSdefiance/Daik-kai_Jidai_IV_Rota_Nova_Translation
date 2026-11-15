"""Source-locked natural Tavern round announcement without a Japanese address."""

import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries


def apply_release(common, arm9, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-round-announcement-v1'
    assert sha(common) == config['source_common_sha256']
    assert sha(arm9) == config['arm9_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    assert len(document['records']) == 1
    row = document['records'][0]
    assert row['message_id'] == 872 and row['english'] == "This round's on %s. Enjoy!{PAD}"
    target = Path(config['target_file']).read_bytes()
    assert sha(target) == config['target_common_sha256'] and len(target) == len(common)
    before = common_message_entries(common, arm9, clean=False)
    after = common_message_entries(target, arm9, clean=False)
    assert [i for i in range(3668) if before[i].text != after[i].text] == [872]
    assert all((a.block, a.block_offset, a.start, a.end, a.copy_end) ==
               (b.block, b.block_offset, b.start, b.end, b.copy_end) for a, b in zip(before, after))
    assert after[872].text.rstrip() == b"This round's on %s. Enjoy!"
    return target, {'changed_records': ['COMMON_MESSAGE_872'],
                    'original_callers_and_both_arguments_preserved': True,
                    'gendered_address_omitted_by_reviewed_localization': True,
                    'all3668_native_offsets_and_other_messages_exact': True,
                    'no_growth_or_runtime_code_changes': True, 'status': 'experimental'}
