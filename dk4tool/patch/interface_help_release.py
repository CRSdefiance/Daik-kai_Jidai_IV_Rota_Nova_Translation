"""Complete source-locked interface/ship explanations and original navigation."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.city_help_release import compile_pages
from dk4tool.patch.grand_race_menu_release import sha

TOPICS = {135, 136, 137, 138, 139, 140, 141, 142, 195, 196, 197, 198, 199, 200, 201}


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-interface-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Interface Help parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed interface Help manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source, topics=TOPICS)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 210 or before[203] != b'\0':
        raise ValueError('Existing Help identities/history differ')
    for page in pages:
        while len(container.blocks) <= page['topic_id']:
            container.blocks.append(b'\0')
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != old for i, old in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned Help article changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256'] or len(container.blocks) != config['target_topic_count']:
        raise ValueError('Complete reviewed interface Help differs')
    return target, {'pages': pages, 'all195_unselected_existing_articles_exact': True,
                    'all210_existing_IDs_and203_sentinel_and208_209_continuations_preserved': True,
                    'crew_assignment_continuation': 210,
                    'all_original_links_and_complete_prose_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{r["topic_id"]}' for r in pages]}
