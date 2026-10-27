"""Help terminology consistent with actual compact skill labels; owned IDs reused."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.city_help_release import compile_pages
from dk4tool.patch.grand_race_menu_release import sha

TOPICS = {116, 117, 118, 121, 126, 128, 133, 158, 168, 170, 175, 177, 178}
CONTINUATIONS = {208, 209}


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-skill-terms-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Skill Help parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed skill terminology manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source, topics=TOPICS)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 211 or before[203] != b'\0':
        raise ValueError('Existing Help identity/history differs')
    if {p['topic_id'] for p in pages} != TOPICS | CONTINUATIONS:
        raise ValueError('Existing owned continuation IDs not preserved')
    for page in pages:
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != raw for i, raw in enumerate(before) if i not in TOPICS | CONTINUATIONS):
        raise ValueError('Unowned Help article changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256']:
        raise ValueError('Complete terminology output differs')
    return target, {'pages': pages, 'all196_unselected_articles_and211_IDs_and203_210_exact': True,
                    '208_HP_and209_requirements_continuations_reused_with_exact_source_locks': True,
                    'physical_Health_condition_and_all_original_facts_links_numbers_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{p["topic_id"]}' for p in pages]}
