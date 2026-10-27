"""Source-locked natural English HELP articles with original binary links."""

import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_help_pages_v281 import encoded_line, wrap

TOPICS = {143, 148, 152, 191, 192, 193}
SOURCE_LINK = re.compile(rb'\{([^{}]*):(.)\}', re.DOTALL)


def compile_pages(manuscript, clean, canonical, current, *, topics=TOPICS, source_link_reader=None):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Reviewed natural-dialogue-v2 en-US HELP prose required')
    if manuscript['source_clean_HELP_sha256'] != sha(clean) or manuscript['source_canonical_HELP_sha256'] != sha(canonical):
        raise ValueError('Clean/canonical HELP source lock differs')
    original = IlnkContainer.parse(clean).blocks
    baseline = IlnkContainer.parse(canonical).blocks
    parent = IlnkContainer.parse(current).blocks
    records = manuscript['records']
    if len(records) != len(topics) or {r['topic_id'] for r in records} != topics:
        raise ValueError('All unique reviewed HELP articles required')
    pages = []
    for row in records:
        topic = row['topic_id']
        if any(not row.get('review', {}).get(gate) for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')):
            raise ValueError('Every HELP record requires all five review gates')
        if any(not row.get(field) for field in ('speaker', 'context', 'source_meaning', 'localization_note')):
            raise ValueError('HELP editorial context/gloss missing')
        for key, source in [('clean_source_hex', original), ('canonical_source_hex', baseline), ('current_source_hex', parent)]:
            if bytes.fromhex(row[key]) != source[topic]:
                raise ValueError('Complete HELP article source differs')
        title, text = row['heading'], row['english']
        for value in (title, text):
            if not value.isascii() or value != value.strip() or '\n' in value or '\r' in value or '  ' in value or '{' in value or '}' in value:
                raise ValueError('HELP prose must be natural unpositioned ASCII paragraphs')
        expected_links = ([m[2][0] for m in SOURCE_LINK.finditer(original[topic])]
                          if source_link_reader is None else
                          [link['topic_id'] for link in source_link_reader(original[topic])])
        rows = wrap(title) + wrap(text)
        if len(rows) > 10:
            raise ValueError('HELP article exceeds the native ten-row window')
        data, visible, links = bytearray(), [], []
        for n, tokens in enumerate(rows):
            encoded, plain, selected = encoded_line(tokens)
            data.extend(encoded + b'\n')
            visible.append(plain)
            links.extend({**link, 'row': n} for link in selected)
        data.append(0)
        if len(data) >= 1024 or [r['id'] for r in links] != expected_links or row['original_link_IDs'] != expected_links:
            raise ValueError('HELP buffer bounds or original link identity differs')
        plain = re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]', r'\1', text)
        if ' '.join(visible) != title + ' ' + plain:
            raise ValueError('Formatted HELP omits or changes prose')
        pages.append({'topic_id': topic, 'encoded_hex': data.hex(),
                      'visible_lines': visible, 'links': links, 'bytes': len(data)})
    return pages


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-trade-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('Complete parent HELP/config lock differs')
    manuscript_path = Path(config['manuscript'])
    if sha(manuscript_path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed HELP manuscript changed')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    pages = compile_pages(manuscript, clean, canonical, source)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 206 or before[203] != b'\0':
        raise ValueError('Parent HELP topics/history sentinel differ')
    for page in pages:
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != block for i, block in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned HELP topic changed')
    target = container.to_bytes()
    if sha(target) != config['target_HELP_sha256']:
        raise ValueError('Deterministic reviewed HELP result differs')
    return target, {'source_HELP_sha256': sha(source), 'target_HELP_sha256': sha(target),
                    'pages': pages, 'original_topic_count_preserved': 206,
                    'all200_unselected_topics_exact': True, 'history203_preserved': True,
                    'all_original_binary_link_destinations_preserved': True,
                    'changed_records': [f'HELP_TOPIC_{p["topic_id"]}' for p in pages]}
