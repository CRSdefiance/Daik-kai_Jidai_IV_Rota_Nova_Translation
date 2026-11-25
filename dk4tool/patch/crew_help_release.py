"""Source-locked ship workrooms, officer policies and consistent role Help."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.city_help_release import compile_pages
from dk4tool.patch.grand_race_menu_release import sha

TOPICS = (set(range(106, 134)) - {127}) | {160, 172, 173, 175, 176, 178, 179}


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-crew-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Crew Help parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed crew manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source, topics=TOPICS)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 209 or before[203] != b'\0':
        raise ValueError('Existing topic IDs/history differ')
    for page in pages:
        while len(container.blocks) <= page['topic_id']:
            container.blocks.append(b'\0')
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != block for i, block in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned existing article changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256'] or len(container.blocks) != config['target_topic_count']:
        raise ValueError('Complete reviewed crew Help output differs')
    return target, {'pages': pages, 'all175_unselected_existing_articles_exact': True,
                    'all209_existing_IDs_and203_sentinel_and208_HP_continuation_preserved': True,
                    'requirements_continuation': 209, 'all16_whole_requirement_entries_preserved': True,
                    'all_original_links_and_complete_prose_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{r["topic_id"]}' for r in pages]}
