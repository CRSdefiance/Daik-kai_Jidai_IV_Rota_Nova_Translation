"""Complete source-locked sea and sailor data HELP with original native links."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.city_help_release import compile_pages
from dk4tool.patch.grand_race_menu_release import sha

TOPICS = set(range(153, 181))


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-sailor-data-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Sailor-data HELP parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed sailor-data manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source, topics=TOPICS)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 208 or before[203] != b'\0':
        raise ValueError('Existing HELP identities/history differ')
    for page in pages:
        while len(container.blocks) <= page['topic_id']:
            container.blocks.append(b'\0')
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != block for i, block in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned HELP topic changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256'] or len(container.blocks) != config['target_topic_count']:
        raise ValueError('Reviewed sailor-data output differs')
    return target, {'pages': pages, 'all180_unselected_existing_topics_exact': True,
                    'all208_existing_IDs_and203_sentinel_preserved': True,
                    'new_continuation_IDs': [r['topic_id'] for r in pages if r['topic_id'] >= 208],
                    'all_original_links_and_complete_prose_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{r["topic_id"]}' for r in pages]}
