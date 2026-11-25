"""Apply the proven native paragraph planner to the 175 newly reviewed tutorial speeches."""
import linecache
from pathlib import Path
import re
from types import SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import plan_rafael_B141_B160_v3 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B177_B180_contextual_v1 import A, CAPTIONS, CURRENT, IDENTITY, OUT as PROSE

MACROS = A / 'Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json'
FORMATTING = Path('translations/rafael_B177_B180_formatting_manuscript_v1.json')
PREFERENCES = Path('translations/rafael_B177_B180_visual_preferences_v1.json')
TOKEN = re.compile(r'\b(FI|FA|FO|FU)\b')


def prepare():
    assert not FORMATTING.exists() and not PREFERENCES.exists()
    document = load(PROSE)
    identity, macros = map(load, [IDENTITY, MACROS])
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert macros['macro_ascii_lengths'] == dict(FI=6, FA=6, FO=10)
    assert identity['evidence'][str(MACROS)] == sha(MACROS.read_bytes())
    assert identity['runtime'] == document['runtime']
    for key in ['ARM9_sha256', 'COMMON_sha256']:
        assert macros['runtime'][key] == identity['runtime'][key]
    count = 0
    for row in document['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        if row['kind'] == 'typed-choice-label':
            continue
        tokens = TOKEN.findall(row['english'])
        assert tokens == row['native_literal_tokens'] and set(tokens) <= {'FI'}
        count += len(tokens)
        row['english'] = TOKEN.sub(lambda match: '{MACRO:' + match[0] + '}', row['english'])
        row['planned_English_markup'] = '{SPEAKER:' + format(row['source_selector'], '02X') + '}' + row['english']
        row['prior_macro_normalized_comparison'] = None
        if not row['english'].isascii():
            assert row['decision'] == 'retention' and row['deliberate_source_punctuation_retention']
            row['prior_macro_normalized_comparison'] = row['current_comparison_paragraph']
            assert row['prior_macro_normalized_comparison'] == row['english']
        if row['kind'] == 'system-FE':
            assert row['source_complete_preamble_hex'] == '0040ffff00fe'
            row['source_FE_presentation_kind'] = 'extra armor unlock notice'
            row['FE_is_not_an_ordinary_actor_nameplate'] = True
    assert count == 4
    document.update(physical_speech_objects=175, ordinary_speech_objects=175, style_physical_speech_objects=0,
        typed_choice_objects=8, typed_choice_commands=4, marked_FI_substitutions=count,
        manuscript_sha256=sha(PROSE.read_bytes()), scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()),
        reused_macro_proof_sha256=sha(MACROS.read_bytes()), no_prose_changes_or_manual_breaks=True)
    save(FORMATTING, document)
    save(PREFERENCES, dict(records={}, progressive_width_px=216, FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True, author_inserted_ordinary_breaks=0, new_credit=0))


def qualify_source(doc):
    current, objects, identity = map(load, [CURRENT, CAPTIONS, IDENTITY])
    assert doc['blocks'] == [177, 178, 179, 180] and doc['all_individual_four_prose_gates_pass']
    assert doc['runtime'] == current['runtime'] == identity['runtime'] == objects['runtime']
    assert doc['scoped_identity_proof_sha256'] == sha(IDENTITY.read_bytes())
    assert doc['reused_macro_proof_sha256'] == sha(MACROS.read_bytes())
    assert current['all_source_preambles_andcommand_kinds_preserved']
    clean_path, current_path = Path('work/clean.nds'), Path(doc['current_ROM'])
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(current_path.read_bytes()) == doc['current_ROM_sha256'] == current['runtime']['candidate_sha256']
    archive = doc['file_path']
    assert archive == '/data/SC0.DK4'
    image = NdsImage.open(current_path)
    assert sha(image.read_file('/__arm9__.bin')) == current['runtime']['ARM9_sha256']
    raw_current = image.read_file(archive)
    assert sha(raw_current) == doc['current_archive_sha256']
    clean = IlnkContainer.parse(NdsImage.open(clean_path).read_file(archive)).blocks
    bank = IlnkContainer.parse(raw_current).blocks
    originals = {row['id']: row for group in current['groups'] for row in group['records']}
    actors = {row['actor_ID'] for row in identity['name_bindings']}
    zero_bodies, bindings = set(), []
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            continue
        source_ref, current_ref = row['source_reference'], row['current_reference']
        block, selector = row['block'], row['source_selector']
        keys = ['source_reference', 'current_reference', 'source_hex', 'current_hex', 'source_complete_preamble_hex']
        assert all(row[key] == originals[row['id']][key] for key in keys)
        source, stored, preamble = (bytes.fromhex(row[key]) for key in keys[2:])
        assert preamble == bytes.fromhex('0040ffff00') + bytes([selector])
        assert source[0] == stored[0] == selector and selector in actors | {254}
        assert all(b'\0' not in body[1:] for body in [source, stored])
        for archive_blocks, ref, body in [(clean, source_ref, source), (bank, current_ref, stored)]:
            assert archive_blocks[block][ref['header_offset']:ref['offset'] + len(body) + 1] == preamble[:5] + body + b'\0'
        if selector == 0:
            zero_bodies.add(source)
        bindings.append(dict(id=row['id'], source_reference=source_ref, current_reference=current_ref,
            complete_source_preamble_hex=preamble.hex(), source_body_sha256=sha(source),
            selector00_owned_by_complete_preamble=selector == 0,
            scoped_identity_binding=str(IDENTITY), scoped_identity_binding_sha256=doc['scoped_identity_proof_sha256']))
    assert len(bindings) == 175 and {row['id'] for row in bindings} == set(originals)
    return zero_bodies, bindings


parameters = vars(previous.env['previous']).copy()
parameters['PAIRS'] = parameters['PAIRS'] | {
    ('fernando', 'dias'), ('manuel', 'almeida'), ('cargo', 'holds'), ('supply', 'holds'),
    ('jigger', 'spanker'), ('square', 'sail'), ('lateen', 'sail'), ('two', 'masts'),
    ('three', 'masts'), ('first', "mate's"), ("mate's", 'office'), ('lumber', 'room'),
    ('rear', 'quarter'), ('trade', 'route'), ('naval', 'battle'), ('one', 'percent'),
}
source = previous.source
env = {**previous.env, 'previous': SimpleNamespace(**parameters), 'qualify_source': qualify_source, '__file__': __file__}
filename = __file__ + '::same-validated-native-geometry-with-175-new-source-bindings'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)

if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        env['main']()
