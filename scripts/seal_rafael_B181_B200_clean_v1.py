"""Seal all 384 clean-first drafts before opening the registered English."""
from pathlib import Path
import re

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B181_B200_clean_20261105')
PACKET = ROOT / 'clean_source_packet.json'
DRAFTS = [ROOT / f'{name}_clean_drafts_v1.json' for name in (
    'B181_B182', 'B183', 'B184_B185', 'B186_B188', 'B189_B195', 'B196_B200',
)]
IDENTITY = Path('translations/hodram_B171_B190_scoped_names_final_v1.json')
CENSUS = ROOT / 'clean_source_census_v1.json'
OUT = ROOT / 'sealed_all_clean_first_v1'
AMENDMENTS = {
    'DK4_MES_B186_R0079': "What are you so shy about now? You said it right in front of Julian: \"I'll give it to her myself!\"",
    'DK4_MES_B186_R0121': 'Anyway, you were quick. I was worn out by the time I got to Seoul.',
    'DK4_MES_B186_R0202': "I'll find something even lovelier than the Silla Gold Crown and come straight back. Then let's go on that date!",
    'DK4_MES_B187_R0047': "Well, well. Look who's scared stiff. You gave us quite a beating last time, didn't you?",
    'DK4_MES_B192_R0005': 'Did you notice that lovely scent they were wearing?',
    'DK4_MES_B192_R0028': 'Next time we see them, shall we work up the nerve to ask?',
    'DK4_MES_B195_R0061': 'What was all that commotion about?',
}


def digest(path):
    return sha(Path(path).read_bytes())


def key(row):
    return row['file_path'], row['id']


def main():
    assert not OUT.exists()
    packet, census = map(load, (PACKET, CENSUS))
    drafts = list(map(load, DRAFTS))
    blocks = list(range(181, 201))
    assert census['clean_speeches'] == packet['records'] == 384
    assert [d['records_count'] for d in drafts] == [58, 37, 43, 99, 91, 56]
    assert [b for d in drafts for b in d['complete_blocks']] == blocks
    assert [g['block'] for g in packet['groups']] == blocks
    assert all(d['no_current_English_extracted_for_this_intake_before_drafts'] and d['all_five_gates_pending'] for d in drafts)
    assert all(digest(p) == h for d in drafts for p, h in d['evidence'].items())
    identity = next(row for row in load(IDENTITY)['records'] if row['actor_ID'] == 201)
    assert identity['english'] == 'Mihwa' and identity['source_meaning'].startswith('美華')
    assert all(identity['review'].values()) and {c['text'] for c in identity['current_consumers']} == {'Mihwa'}
    contexts = {b: context for d in drafts for b, context in d['source_contexts'].items()}
    records = [r for d in drafts for r in d['records']]
    source_rows = [r for g in packet['groups'] for r in g['records']]
    assert len(set(map(key, records))) == len(records) == 384
    assert set(AMENDMENTS) <= {r['id'] for r in records}
    assert len([c for g in packet['groups'] for c in g['all_source_commands'] if c['word'] == 0x2000]) == 2
    assert all(c['word'] not in (0x2100, 0x2200, 0x4100) for g in packet['groups'] for c in g['all_source_commands'])
    alignments = []
    for row, source in zip(records, source_rows, strict=True):
        assert all(row[k] == v for k, v in source.items()) and not any(row['review'].values())
        prior = row['independent_English']
        aligned = AMENDMENTS.get(row['id'], prior).replace('Meihua', identity['english'])
        row['independent_English'] = aligned
        row['source_meaning'] = row['source_meaning'].replace('Meihua', identity['english'])
        row['context'] = row['context'].replace('Meihua', identity['english']).split(' Mihwa is the working Hangzhou')[0]
        assert aligned and '\n' not in aligned
        assert all(aligned.count(token) == count for token, count in row['native_literal_token_counts'].items())
        if aligned != prior:
            alignments.append(dict(id=row['id'], clean_first_original=prior, aligned_draft=aligned,
                reason='Use the reviewed shared actor 201 spelling.' if 'Meihua' in prior
                    else 'Resolve an assumption or refine dialogue against the complete clean exchange.'))
    contexts = {b: c.replace('Meihua', identity['english']).split(' Mihwa is the working Hangzhou')[0] for b, c in contexts.items()}
    OUT.mkdir()
    sealed = OUT / 'sealed_drafts.json'
    proof = {str(p): digest(p) for p in (PACKET, CENSUS, *DRAFTS, IDENTITY, Path(__file__))}
    save(sealed, dict(records=records, records_count=384, complete_blocks=blocks, source_contexts=contexts,
        all_five_gates_pending=True, source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        no_blanket_prior_English_exposure_claim=True,
        disclosed_prior_user_screenshot_reference='B196 R0022 tea request, referenced for comparison and role review.',
        source_selector_FE_records=[r['id'] for r in records if r['source_selector'] == 254],
        clean_first_alignment=alignments, source_proof=proof, new_credit=0))
    save(OUT / 'current_binding_meanings.json', dict(source_packet=str(PACKET), source_packet_sha256=digest(PACKET),
        records=[{**r, 'current_ROM_English_unconsulted': True} for r in records], meanings=384,
        all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    print('Sealed all 384 clean meanings and drafts across 20 blocks with exact source references and preserved substitutions.')


if __name__ == '__main__':
    main()
