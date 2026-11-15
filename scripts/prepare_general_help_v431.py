"""Seven source-faithful HELP articles and automatically paginated native previews."""

import json
import re
from pathlib import Path

from dk4tool.dialogue.help_layout import wrap_body
from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_help_pages_v281 import encoded_line, wrap
from scripts.verify_help_parser_v281 import verify

ROOT = Path('work/analysis/general_help_v431')
MANUSCRIPT = Path('translations/general_help_manuscript_v1.json')
PARENT = Path('out/all_routes_combined_v430_candidate.nds')
PARENT_TOPIC_COUNT = 206
LAYOUT_BY_TOPIC = {}
REUSED_CONTINUATIONS = {}
PROSE = {
    21: ('Market',
         "The market lets you buy and sell trade goods and gather information. If you bring a [[194|Source Item]] to a city's market, you may be asked to hand it over. Doing so adds to that city's [[152|specialties]]. See [[22|Trade]], [[23|Commercial Investment]] and [[24|Market Prices]].",
         'Trade and information at the market. A source item may be requested; giving it expands local specialties. Links to Trade, Commercial Investment and Market Prices.',
         'Retain the request as a possibility rather than an automatic loss of the item.'),
    23: ('Commercial Investment',
         "Invest to develop a city's commerce. You can invest 1 to 20 units at a time. Each unit costs gold equal to half the city's Growth. Investment raises Growth. Your market share also increases if the city's total [[150|market share]] is below 100 percent or a faction you are [[187|at war with]] holds a share there. Higher Growth may add new [[152|specialties]].",
         'Invest1-20 units; each costs gold equal to50 percent of city development. Investment raises development and may increase specialties. Own share increases when total share is below100 percent or a warring faction owns share.',
         'Use Growth consistently. Half preserves50 percent; retain both share conditions and may for specialties.'),
    103: ('Shared Commands',
          'These commands are available both in cities and at sea. Press X on the city or sailing screen to open the menu. See [[104|Route Map]], [[105|Deck]], [[134|Info]], [[138|Items]], [[139|Assign Sailors]] and [[140|Functions]].',
          'Shared commands are usable in both city and sea screens; the source menu-button symbol opens them. Six command destinations.',
          'Localize the menu symbol to DS X, supported by ordinary city input and the documented V328 sea Menu sequence. Preserve Route Map104 despite a brace-valued Shift-JIS trail byte.'),
    105: ('Deck',
          "You can assign officers to jobs from the Deck screen. Choose an officer and place them in a room; the room's type determines their job. Each job has [[133|ability requirements]]. An officer who does not meet them cannot take that job. Higher abilities make the assignment more effective. See [[106|Personnel]], [[110|Workrooms]] and [[127|Holds]].",
          'Deck assigns navigator roles by rooms. Roles have required abilities; insufficient abilities prevent assignment. Higher abilities improve effects. Personnel, workrooms and holds links.',
          'Keep the eligibility rule and scaling benefit as distinct facts; do not turn assigned rooms into unrestricted jobs.'),
    127: ('Holds',
          "The ship's holds are divided into five types according to their purpose. You can assign officers to the Marine Barracks and Gun Batteries. See [[128|Marine Barracks]], [[129|Gun Batteries]], [[130|Rowers' Quarters]], [[131|Supply Hold]] and [[132|Cargo Hold]].",
          'Five types of ship holds; navigators can be assigned to marine quarters and armed batteries. Preserve all five links.',
          'Use readable full room names while retaining the restriction to the two assignable combat spaces.'),
    134: ('Info',
          'View [[135|Sailor Info]], [[136|Ship Info]], [[137|Fleet Info]], [[141|Golden Route Records]] and [[142|Ancient Maps]].',
          'Shows character, ship, fleet, golden-route record and ancient-map information.',
          'Use established Info screen labels. Preserve Ancient Maps142 despite the Japanese map glyph containing a brace-valued trail byte.'),
    144: ('City Info',
          'Select a city you have visited on the Route Map to view its information. See [[145|City or Port]], [[146|Cultural Region]], [[147|Status]], [[148|Growth]], [[149|Arms]], [[150|Market Share]] and [[152|Specialties]].',
          'City data is displayed by selecting a previously visited city on the route map. Seven original field links.',
          'Retain the visited-city condition and match existing Growth, Arms, Status and Share terminology.'),
}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    current = NdsImage.open(PARENT)
    raw_clean, raw_base, source = [r.read_file('/COMMON/HELP.DK4') for r in (clean, canonical, current)]
    original, baseline, container = [IlnkContainer.parse(raw) for raw in (raw_clean, raw_base, source)]
    before = list(container.blocks)
    assert len(before) == PARENT_TOPIC_COUNT and before[203] == b'\0'
    records, pages, checks, articles = [], [], [], []
    next_id = len(before)
    for topic, (title, english, meaning, note) in PROSE.items():
        assert english == english.strip() and '\n' not in english and '  ' not in english
        body = wrap_body(english, LAYOUT_BY_TOPIC.get(topic, 'paragraph-v1'))
        batches = []
        if len(wrap(title)) + len(body) <= 10:
            batches = [wrap(title) + body]
        else:
            remaining = list(body)
            while remaining:
                heading = wrap(title if not batches else title + ' (continued)')
                take = 9 - len(heading)
                batches.append(heading + remaining[:take])
                remaining = remaining[take:]
        ids = [topic]
        if topic in REUSED_CONTINUATIONS:
            reused = REUSED_CONTINUATIONS[topic]
            assert len(reused) == len(batches) - 1
            assert all(202 < n < len(before) and n != 203 for n in reused)
            ids.extend(reused)
        else:
            for _ in batches[1:]:
                assert next_id != 203 and next_id <= 255
                ids.append(next_id)
                next_id += 1
        semantic, preserved_links = [], []
        for page_number, rows in enumerate(batches):
            header = wrap(title if page_number == 0 else title + ' (continued)')
            semantic.extend(encoded_line(tokens)[1] for tokens in rows[len(header):])
            if len(batches) > 1:
                target = ids[page_number + 1] if page_number + 1 < len(batches) else topic
                rows = rows + [[{'label': 'Continue reading' if page_number + 1 < len(batches) else 'Back to article start',
                                  'id': target, 'navigation': True}]]
            assert len(rows) <= 10
            data, visible, links = bytearray(), [], []
            for row_number, tokens in enumerate(rows):
                encoded, line, selected = encoded_line(tokens)
                data.extend(encoded + b'\n')
                visible.append(line)
                links.extend({**link, 'row': row_number} for link in selected)
            data.append(0)
            preserved_links.extend(link['id'] for link in links if not link['navigation'])
            assert len(data) < 1024
            page = {'topic_id': ids[page_number], 'source_article_id': topic,
                    'page_number': page_number + 1, 'page_count': len(batches),
                    'visible_lines': visible, 'links': links, 'encoded_hex': data.hex(),
                    'bytes': len(data)}
            proof, picture = verify(current.read_file('/__arm9__.bin'), page)
            path = ROOT / f"topic_{page['topic_id']}_native.png"
            picture.save(path)
            proof['preview'] = str(path)
            proof['preview_sha256'] = sha(path.read_bytes())
            checks.append(proof)
            pages.append(page)
            while len(container.blocks) <= ids[page_number]:
                container.blocks.append(b'\0')
            container.blocks[ids[page_number]] = bytes(data)
        expected_links = [link['topic_id'] for link in source_links(original.blocks[topic])]
        assert preserved_links == expected_links
        plain = re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]', r'\1', english)
        assert ' '.join(semantic) == plain
        records.append({'id': f'HELP_TOPIC_{topic}', 'topic_id': topic,
                        'speaker': 'Game help', 'heading': title, 'english': english,
                        'context': 'Original market/shared-command/city-data help and its linked neighbors.',
                        'source_meaning': meaning, 'localization_note': note,
                        'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')},
                        'clean_source_hex': original.blocks[topic].hex(),
                        'canonical_source_hex': baseline.blocks[topic].hex(),
                        'current_source_hex': before[topic].hex(),
                        'source_Japanese_with_link_IDs': readable_source(original.blocks[topic]),
                        'original_links': source_links(original.blocks[topic]),
                        'original_link_IDs': expected_links,
                        'clean_neighbors': [{'topic_id': n, 'source': readable_source(original.blocks[n])}
                                            for n in (topic - 1, topic + 1) if 0 <= n < len(original.blocks)]})
        if topic in LAYOUT_BY_TOPIC:
            records[-1]['semantic_layout'] = LAYOUT_BY_TOPIC[topic]
        if topic in REUSED_CONTINUATIONS:
            records[-1]['continuation_sources'] = [{'topic_id': n, 'current_source_hex': before[n].hex()}
                                                  for n in REUSED_CONTINUATIONS[topic]]
        articles.append({'source_topic_id': topic, 'topic_pages': ids,
                         'all_complete_prose_and_original_links_preserved': True})
    owned_continuations = {n for ids in REUSED_CONTINUATIONS.values() for n in ids}
    assert all(container.blocks[i] == raw for i, raw in enumerate(before) if i not in PROSE and i not in owned_continuations)
    manuscript = {'format': 'dk4-structured-help-editorial-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'not_a_release_batch': True, 'formatting_owned_by_compiler': True,
                  'source_clean_HELP_sha256': sha(raw_clean),
                  'source_canonical_HELP_sha256': sha(raw_base), 'records': records}
    MANUSCRIPT.write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    target = container.to_bytes()
    assert IlnkContainer.parse(target).blocks == container.blocks
    (ROOT / 'HELP_research_only.bin').write_bytes(target)
    plan = {'format': 'dk4-general-help-proposal-v431', 'source_ROM_sha256': sha(current.source.read_bytes()),
            'source_HELP_sha256': sha(source), 'target_HELP_sha256': sha(target),
            'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
            'articles': articles, 'pages': pages, 'native_parser_proofs': checks,
            'all_unselected_original_topics_exact': True,
            'unselected_original_topic_count': len(before) - len(PROSE) - len(owned_continuations),
            'history203_preserved': container.blocks[203] == b'\0',
            'target_topic_count': len(container.blocks),
            'source_link_parser_handles_multibyte_brace_trails': True,
            'registered_integration_and_actual_navigation_pending': True,
            'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    (ROOT / 'page_proposal.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'reviewed_articles': len(PROSE), 'native_pages': len(pages),
                      'target_topic_count': len(container.blocks),
                      'articles': articles, 'ROM_changed': False}))


if __name__ == '__main__':
    main()
