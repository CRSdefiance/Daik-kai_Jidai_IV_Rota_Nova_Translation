"""Seven complete HELP topics with character-aware original link preservation."""

import json
from pathlib import Path

from dk4tool.dialogue.help_source_links import source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.trade_help_release import compile_pages

TOPICS = {21, 23, 103, 105, 127, 134, 144}


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] not in ('dk4-general-help-release-v1', 'dk4-general-help-release-v2') or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Complete general-help parent/config lock differs')
    topics = TOPICS if config['format'] == 'dk4-general-help-release-v1' else TOPICS | {11}
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('General HELP manuscript changed')
    manuscript = json.loads(path.read_text(encoding='utf-8'))
    pages = compile_pages(manuscript, clean, canonical, source,
                          topics=topics, source_link_reader=source_links)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 206 or before[203] != b'\0':
        raise ValueError('Parent HELP topics/history sentinel differ')
    for page in pages:
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != block for i, block in enumerate(before) if i not in topics):
        raise ValueError('Unowned HELP topic changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256']:
        raise ValueError('Reviewed general-help bytes differ')
    return target, {'source_HELP_sha256': sha(source), 'target_HELP_sha256': sha(target),
                    'pages': pages, 'all_unselected_topics_exact': True,
                    'unselected_topic_count': len(before) - len(topics),
                    'topic_count_preserved': 206, 'history203_preserved': True,
                    'all_original_binary_link_IDs_preserved_including_map_labels': True,
                    'changed_records': [f'HELP_TOPIC_{p["topic_id"]}' for p in pages]}
