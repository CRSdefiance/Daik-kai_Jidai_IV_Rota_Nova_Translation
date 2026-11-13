"""Reviewed trade-help prose, source links, automatic layout and native previews."""

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_help_pages_v281 import encoded_line, wrap
from scripts.verify_help_parser_v281 import verify

ROOT = Path('work/analysis/trade_help_v429')
MANUSCRIPT = Path('translations/trade_help_manuscript_v1.json')
LINK = re.compile(rb'\{([^{}]*):(.)\}', re.DOTALL)
PROSE = {
    143: ('Data Guide',
          "This guide explains the game's data. See [[144|City Info]], [[153|Sea Info]], [[158|Sailor Info]], [[181|Fleet Info]], [[191|Trade Goods]] and [[195|Ship Info]].",
          'Introduces data explanations and six original topic links.',
          'Use existing screen labels for linked data categories; keep all six destinations.'),
    148: ('Growth',
          "Growth measures how developed a city is. It increases when you make [[23|commercial investments]] at the market. As Growth rises, the city may offer more specialties. The number of sailors you can recruit and the types of cannon you can equip also change.",
          'City development increases with commercial investment; higher development may expand specialties and changes recruitable sailors and available cannon types.',
          'Growth matches the town panel. Preserve the uncertainty about new specialties and do not invent a fixed recruitment or cannon threshold.'),
    152: ('Specialties',
          'Specialties are the trade goods sold in a city. A city may offer more as it develops or when source items are delivered. Stock is replenished each [[24|arrival month]]. See [[194|Source Items]].',
          'Goods sold in a city; development or source items may expand the selection; replenishment occurs in arrival months, with a link to source items.',
          'Source Items distinguishes the specialty-producing items from ordinary raw-material commodities. Preserve may and the arrival-month rule.'),
    191: ('Trade Goods',
          'Trade goods are bought and sold at markets. The goods sold in each city are its specialties, and each city offers a different selection. Prices vary by city and change with market conditions. Base prices also vary by cultural region. See [[192|Types]] and [[193|Quality Grades]].',
          'Defines trade goods and specialties; city selection and prices vary; market conditions affect prices; base prices differ between cultural regions; links to types and grades.',
          'Retain all distinct pricing factors rather than reducing the article to generic trading advice.'),
    192: ('Types of Trade Goods',
          'Trade goods fall into 18 categories. Goods in the same category share the effects of market conditions. Buying or selling a good causes prices to rise or fall for every good in the same category.',
          'There are18 categories. Trade changes prices for all goods in the same category.',
          'Keep18 and the category-wide effect; do not claim every good in the market changes price.'),
    193: ('Quality Grades',
          "Trade goods have quality grades from 1 to 5, with grade 1 being the best. As a city's [[148|Growth]] increases, the quality of its [[152|specialties]] improves. Higher-quality goods earn greater profits when traded.",
          'Grades1 through5;1 highest. City development improves specialty quality. Better quality goods yield greater trading profit.',
          'Express improved quality without implying that a larger numeric grade is better. Preserve the two original links.'),
}


def readable(raw):
    return LINK.sub(lambda m: b'[[' + str(m[2][0]).encode() + b'|' + m[1] + b']]',
                    raw.rstrip(b'\0')).decode('cp932')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    current = NdsImage.open('out/all_routes_combined_v414_candidate.nds')
    original_raw = clean.read_file('/COMMON/HELP.DK4')
    original = IlnkContainer.parse(original_raw).blocks
    baseline = IlnkContainer.parse(canonical.read_file('/COMMON/HELP.DK4')).blocks
    source = current.read_file('/COMMON/HELP.DK4')
    container = IlnkContainer.parse(source)
    before = list(container.blocks)
    assert len(before) == 206 and before[203] == b'\0'
    records, pages, checks = [], [], []
    for topic, (heading, english, meaning, note) in PROSE.items():
        source_links = [m[2][0] for m in LINK.finditer(original[topic])]
        assert '\n' not in english and '  ' not in english and english == english.strip()
        rows = wrap(heading) + wrap(english)
        assert len(rows) <= 10, (topic, len(rows))
        data, lines, links = bytearray(), [], []
        for line_number, tokens in enumerate(rows):
            raw, visible, line_links = encoded_line(tokens)
            data.extend(raw + b'\n')
            lines.append(visible)
            links.extend({**link, 'row': line_number} for link in line_links)
        data.append(0)
        assert len(data) < 1024
        assert [link['id'] for link in links] == source_links
        plain = re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]', r'\1', english)
        assert ' '.join(lines) == heading + ' ' + plain
        page = {'topic_id': topic, 'source_article_id': topic, 'page_number': 1,
                'page_count': 1, 'visible_lines': lines, 'links': links,
                'encoded_hex': data.hex(), 'bytes': len(data)}
        proof, picture = verify(current.read_file('/__arm9__.bin'), page)
        image_path = ROOT / f'topic_{topic}_native.png'
        picture.save(image_path)
        proof['preview'] = str(image_path)
        proof['preview_sha256'] = sha(image_path.read_bytes())
        checks.append(proof)
        records.append({'id': f'HELP_TOPIC_{topic}', 'topic_id': topic,
                        'speaker': 'Game help', 'heading': heading, 'english': english,
                        'context': 'Data Guide and trade-quality help; explanatory interface prose.',
                        'source_meaning': meaning, 'localization_note': note,
                        'review': {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')},
                        'clean_source_hex': original[topic].hex(),
                        'canonical_source_hex': baseline[topic].hex(),
                        'current_source_hex': before[topic].hex(),
                        'source_Japanese_with_link_IDs': readable(original[topic]),
                        'original_link_IDs': source_links,
                        'clean_neighbors': [{'topic_id': n, 'source': readable(original[n])}
                                            for n in (topic - 1, topic + 1)]})
        pages.append(page)
        container.blocks[topic] = bytes(data)
    assert all(container.blocks[i] == block for i, block in enumerate(before) if i not in PROSE)
    manuscript = {'format': 'dk4-structured-help-editorial-manuscript-v1',
                  'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                  'not_a_release_batch': True, 'formatting_owned_by_compiler': True,
                  'source_clean_HELP_sha256': sha(original_raw),
                  'source_canonical_HELP_sha256': sha(canonical.read_file('/COMMON/HELP.DK4')),
                  'records': records}
    MANUSCRIPT.write_text(json.dumps(manuscript, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    target = container.to_bytes()
    assert IlnkContainer.parse(target).blocks == container.blocks
    (ROOT / 'HELP_research_only.bin').write_bytes(target)
    plan = {'format': 'dk4-trade-help-page-proposal-v429', 'candidate_source': str(current.source),
            'source_ROM_sha256': sha(current.source.read_bytes()),
            'source_HELP_sha256': sha(source), 'target_HELP_sha256': sha(target),
            'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
            'pages': pages, 'native_parser_proofs': checks,
            'all200_unrelated_topics_byte_exact': True,
            'topic_count_unchanged': 206, 'history203_preserved': True,
            'all_original_link_IDs_preserved': True,
            'native_link_child_creation_is_observed_contract': True,
            'actual_navigation_and_registered_ROM_integration_pending': True,
            'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    (ROOT / 'page_proposal.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    sheet = Image.new('RGB', (504, 432), '#333333')
    draw = ImageDraw.Draw(sheet)
    for n, page in enumerate(pages):
        x, y = n % 2 * 252, n // 2 * 144
        draw.text((x + 4, y + 4), f"Topic {page['topic_id']}", fill='white')
        with Image.open(ROOT / f"topic_{page['topic_id']}_native.png") as picture:
            sheet.paste(picture, (x, y + 24))
    sheet.save(ROOT / 'native_preview_sheet.png')
    print(json.dumps({'reviewed_articles': len(records), 'native_parser_pages': len(checks),
                      'rows': {p['topic_id']: len(p['visible_lines']) for p in pages},
                      'all_source_link_destinations_preserved': True, 'ROM_changed': False}))


if __name__ == '__main__':
    main()
