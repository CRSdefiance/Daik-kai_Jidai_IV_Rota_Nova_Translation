"""Complete source-locked city HELP with compiler-owned continuation topics."""

import json
import re
from pathlib import Path

from dk4tool.dialogue.help_layout import wrap_body
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_help_pages_v281 import encoded_line, wrap

TOPICS = {145, 146, 147, 149, 150, 151, 194}


def compile_pages(manuscript, clean, canonical, source, *, topics=TOPICS):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Reviewed natural English city HELP required')
    if manuscript['source_clean_HELP_sha256'] != sha(clean) or manuscript['source_canonical_HELP_sha256'] != sha(canonical):
        raise ValueError('Clean/canonical HELP locks differ')
    original, baseline, parent = [IlnkContainer.parse(raw).blocks for raw in (clean, canonical, source)]
    records = manuscript['records']
    if len(records) != len(topics) or {r['topic_id'] for r in records} != topics:
        raise ValueError('All unique reviewed paginated HELP articles required')
    pages, next_id = [], len(parent)
    for row in records:
        topic = row['topic_id']
        if any(not row.get('review', {}).get(k) for k in ('source', 'context', 'localization', 'naturalness', 'formatting')):
            raise ValueError('Per-article review gates missing')
        if any(not row.get(k) for k in ('speaker', 'context', 'source_meaning', 'localization_note')):
            raise ValueError('Article editorial context missing')
        for key, blocks in [('clean_source_hex', original), ('canonical_source_hex', baseline), ('current_source_hex', parent)]:
            if bytes.fromhex(row[key]) != blocks[topic]:
                raise ValueError('Complete article source differs')
        title, english = row['heading'], row['english']
        for value in (title, english):
            if not value.isascii() or value != value.strip() or any(ord(c) < 32 for c in value) or '  ' in value or '{' in value or '}' in value:
                raise ValueError('Unpositioned ASCII paragraphs required')
        body = wrap_body(english, row.get('semantic_layout', 'paragraph-v1'))
        batches = []
        if len(wrap(title)) + len(body) <= 10:
            batches = [wrap(title) + body]
        else:
            remaining = list(body)
            while remaining:
                heading = wrap(title if not batches else title + ' (continued)')
                take = 9 - len(heading)
                if take <= 0:
                    raise ValueError('Heading leaves no room for prose')
                batches.append(heading + remaining[:take])
                remaining = remaining[take:]
        ids = [topic]
        reused = row.get('continuation_sources')
        if reused is not None:
            if len(reused) != len(batches) - 1:
                raise ValueError('Reviewed continuation count differs')
            for continuation in reused:
                n = continuation['topic_id']
                if not 202 < n < len(parent) or n == 203 or bytes.fromhex(continuation['current_source_hex']) != parent[n]:
                    raise ValueError('Owned continuation source differs')
                ids.append(n)
        else:
            for _ in batches[1:]:
                if next_id == 203 or next_id > 255:
                    raise ValueError('Continuation topic exceeds native ID bounds')
                ids.append(next_id)
                next_id += 1
        semantic, actual_links = [], []
        for index, rows in enumerate(batches):
            header = wrap(title if index == 0 else title + ' (continued)')
            semantic.extend(encoded_line(tokens)[1] for tokens in rows[len(header):])
            if len(batches) > 1:
                target = ids[index + 1] if index + 1 < len(batches) else topic
                rows = rows + [[{'label': 'Continue reading' if index + 1 < len(batches) else 'Back to article start',
                                  'id': target, 'navigation': True}]]
            data, visible, links = bytearray(), [], []
            for line, tokens in enumerate(rows):
                encoded, text, selected = encoded_line(tokens)
                data.extend(encoded + b'\n')
                visible.append(text)
                links.extend({**r, 'row': line} for r in selected)
            data.append(0)
            if len(data) >= 1024 or len(rows) > 10:
                raise ValueError('Native HELP page bounds exceeded')
            actual_links.extend(r['id'] for r in links if not r['navigation'])
            pages.append({'topic_id': ids[index], 'source_article_id': topic,
                          'page_number': index + 1, 'page_count': len(batches),
                          'visible_lines': visible, 'links': links, 'bytes': len(data),
                          'encoded_hex': data.hex()})
        expected = [r['topic_id'] for r in source_links(original[topic])]
        if actual_links != expected or row['original_link_IDs'] != expected:
            raise ValueError('Original link destinations/order differ')
        plain = re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]', r'\1', english)
        if ' '.join(semantic) != plain:
            raise ValueError('Pagination omits or changes prose')
    return pages


def apply_release(source, clean, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-city-help-release-v1' or sha(source) != config['source_HELP_sha256']:
        raise ValueError('City-help parent/config differs')
    path = Path(config['manuscript'])
    if sha(path.read_bytes()) != config['manuscript_sha256']:
        raise ValueError('Reviewed city HELP manuscript changed')
    pages = compile_pages(json.loads(path.read_text(encoding='utf-8')), clean, canonical, source)
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    if len(before) != 206 or before[203] != b'\0':
        raise ValueError('Parent topic identities/history differ')
    for page in pages:
        while len(container.blocks) <= page['topic_id']:
            container.blocks.append(b'\0')
        container.blocks[page['topic_id']] = bytes.fromhex(page['encoded_hex'])
    if any(container.blocks[i] != raw for i, raw in enumerate(before) if i not in TOPICS):
        raise ValueError('Unowned existing HELP topic changed')
    target = container.to_bytes()
    if len(container.blocks) != 208 or sha(target) != config['target_HELP_sha256']:
        raise ValueError('Reviewed complete HELP target differs')
    return target, {'pages': pages, 'all199_unselected_existing_topics_exact': True,
                    'history203_preserved': True, 'target_topic_count': 208,
                    'complete_prose_and_original_links_retained': True,
                    'changed_records': [f'HELP_TOPIC_{r["topic_id"]}' for r in pages]}
