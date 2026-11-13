"""Complete source-faithful faction HELP and distinct faction/fleet navigation."""

import json
from pathlib import Path

from dk4tool.dialogue.help_source_links import source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.trade_help_release import compile_pages

TOPICS = {143, *range(181, 191)}


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-faction-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Faction-help parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed faction manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source,
                          topics=TOPICS, source_link_reader=source_links)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 208 or before[203] != b'\0':
        raise ValueError('Existing topic identities/history differ')
    for page in pages:
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != block for i, block in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned HELP topic changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256']:
        raise ValueError('Complete reviewed faction-help output differs')
    return target, {'pages': pages, 'all197_unselected_topics_exact': True,
                    'all208_topic_IDs_and203_sentinel_preserved': True,
                    'faction_and_individual_fleet_information_distinct': True,
                    'all_original_link_IDs_and_complete_prose_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{r["topic_id"]}' for r in pages]}
