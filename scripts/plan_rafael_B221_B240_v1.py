"""Format B221–B240 on the qualified Rafael geometry, keeping four staged records separate."""
from pathlib import Path
import re
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import plan_rafael_B121_B140_withstyles_v1 as planner
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import MACROS
from scripts.write_rafael_B221_B240_contextual_v1 import BLOCKS, OUT as PROSE, ROOT, digest

CURRENT = ROOT / 'current_effective.json'
OBJECTS = ROOT / 'objects/current_objects.json'
GETTERS = ROOT / 'names_and_terms_v1.json'
ROLES = ROOT / 'roles.json'
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_layouts_v1.json'
IDENTITY = ROOT / 'scoped_runtime_v1.json'
CLEAN = Path('work/clean.nds')
TOKEN = re.compile(r'\b(FI|FA|FO|FU)\b')
KEYS = ('source_reference', 'current_reference', 'source_hex', 'current_hex')
STYLE = '4100-style-alternative'


def prepare():
    assert not any(path.exists() for path in (IDENTITY, FORMATTING, PREFERENCES, STAGED))
    doc, names, roles, macros = map(load, (PROSE, GETTERS, ROLES, MACROS))
    assert doc['runtime'] == names['runtime'] == roles['runtime']
    assert names['exact_prior_ARM9_COMMON_actor_root_and_font']
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert all(macros['runtime'][key] == names['runtime'][key] for key in ('ARM9_sha256', 'COMMON_sha256'))
    assert names['macro_ascii_lengths'] == dict(FI=6, FA=6, FO=10, FU=13)
    names.update(actors=[row['actor_ID'] for row in names['name_bindings']],
                 exact_unchanged_actor0_macro_dependencies=True, dynamic_selectors=[208])
    names['evidence'].update({str(path): digest(path) for path in (MACROS, ROLES)})
    save(IDENTITY, names)

    ordinary, staged, choices = [], [], []
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        if row['kind'] == 'typed-choice-label':
            choices.append(row)
            continue
        tokens = TOKEN.findall(row['english'])
        assert tokens == row['native_literal_tokens']
        row['english'] = TOKEN.sub(lambda match: '{MACRO:' + match[0] + '}', row['english'])
        row['planned_English_markup'] = f"{{SPEAKER:{row['source_selector']:02X}}}" + row['english']
        row['prior_macro_normalized_comparison'] = None
        if not row['english'].isascii():
            assert row['decision'] == 'retention' and row['deliberate_source_punctuation_retention']
            assert row['current_comparison_paragraph'] == row['english']
            row['prior_macro_normalized_comparison'] = row['english']
        if row.get('source_signature_presentation_pending') or row.get('source_staged_effect_rows_pending'):
            assert not tokens
            staged.append(row)
        else:
            ordinary.append(row)
    assert tuple(map(len, (ordinary, staged, choices))) == (259, 4, 7)
    assert sum(row.get('native_object_kind') == STYLE for row in ordinary) == 29
    assert sum(len(row['native_literal_tokens']) for row in ordinary) == 6
    assert sum(row['kind'] == 'system-FE' for row in ordinary) == 2
    proof = dict(manuscript_sha256=digest(PROSE), scoped_identity_proof_sha256=digest(IDENTITY),
                 reused_macro_proof_sha256=digest(MACROS), no_prose_changes_or_manual_breaks=True)
    save(FORMATTING, {**doc, **proof, 'records': ordinary + choices, 'physical_speech_objects': len(ordinary),
         'ordinary_speech_objects': 230, 'style_physical_speech_objects': 29, 'style_command_objects': 4,
         'pending_staged_merge': [row['id'] for row in staged]})
    save(STAGED, {**proof, 'runtime': doc['runtime'], 'records': staged,
                  'source_staging_only_no_display_approval': True})
    save(PREFERENCES, dict(records={}, progressive_width_px=216, FE_physical_width_px=228,
         no_old_record_specific_guard_orsemantic_preference_inherited=True, author_inserted_ordinary_breaks=0,
         new_credit=0))


def qualify_source(doc):
    current, objects, identity, roles, staged = map(load, (CURRENT, OBJECTS, IDENTITY, ROLES, STAGED))
    assert doc['runtime'] == current['runtime'] == objects['runtime'] == identity['runtime'] == roles['runtime']
    assert doc['all_individual_four_prose_gates_pass'] and doc['blocks'] == BLOCKS
    assert doc['scoped_identity_proof_sha256'] == digest(IDENTITY)
    assert doc['reused_macro_proof_sha256'] == digest(MACROS)
    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert digest(CLEAN) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    path = Path(doc['current_ROM'])
    image = NdsImage.open(path)
    assert digest(path) == doc['current_ROM_sha256'] == current['runtime']['candidate_sha256']
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(image.read_file('/__arm9__.bin')) == current['runtime']['ARM9_sha256']
    archive = doc['file_path']
    assert archive == '/data/SC0.DK4' and sha(image.read_file(archive)) == doc['current_archive_sha256']
    clean = IlnkContainer.parse(NdsImage.open(CLEAN).read_file(archive)).blocks
    bank = IlnkContainer.parse(image.read_file(archive)).blocks
    source_ordinary = {row['id']: row for group in current['groups'] for row in group['records']}
    source_styles = {row['id']: row for row in objects['style_records']}
    source_roles = {row['id']: row for row in roles['source_records']}
    zeros, bindings = set(), []
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            continue
        ident, block, selector = row['id'], row['block'], row['source_selector']
        sr, cr = row['source_reference'], row['current_reference']
        raw, stored = map(bytes.fromhex, (row['source_hex'], row['current_hex']))
        if row.get('native_object_kind') == STYLE:
            keys = (*KEYS, 'source_header_hex', 'source_choice_object_hex', 'current_style_object_hex',
                    'source_style_indices', 'current_style_indices')
            assert all(row[key] == source_styles[ident][key] for key in keys)
            assert source_roles[ident] == row['native_role_source_binding']
            head = bytes.fromhex(row['source_header_hex'])
            assert len(head) == 20 and head[:2] == b'\0A' and head[-2:] == bytes([0, selector])
            assert clean[block][sr['command_offset']:sr['command_offset'] + 20] == head
            assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
            header_bytes = b''
            binding = OBJECTS
        else:
            assert all(row[key] == source_ordinary[ident][key] for key in (*KEYS, 'source_complete_preamble_hex'))
            head = bytes.fromhex(row['source_complete_preamble_hex'])
            assert head == bytes.fromhex('0040ffff00') + bytes([selector])
            assert raw[0] == stored[0] == selector and selector in set(identity['actors']) | {254}
            assert b'\0' not in raw[1:] and b'\0' not in stored[1:]
            if selector == 0:
                zeros.add(raw)
            if selector == 254:
                assert row['source_FE_presentation_kind'] and row['FE_is_not_an_ordinary_actor_nameplate']
            header_bytes = head[:5]
            binding = CURRENT
        for archive_blocks, ref, payload in ((clean, sr, raw), (bank, cr, stored)):
            start = ref['header_offset'] if header_bytes else ref['offset']
            assert archive_blocks[block][start:ref['offset'] + len(payload) + 1] == header_bytes + payload + b'\0'
        bindings.append(dict(id=ident, source_reference=sr, current_reference=cr,
                             complete_source_header_hex=head.hex(), source_body_sha256=sha(raw),
                             scoped_identity_binding=str(IDENTITY), source_object_binding=str(binding),
                             source_object_binding_sha256=digest(binding)))
    expected = (set(source_ordinary) | set(source_styles)) - set(doc.get('pending_staged_merge', []))
    assert set(doc.get('pending_staged_merge', [])).issubset({row['id'] for row in staged['records']})
    assert {row['id'] for row in bindings} == expected and len(bindings) == len(expected)
    return zeros, bindings


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FunctionType(planner.main.__code__, {**planner.env, 'qualify_source': qualify_source, '__file__': __file__})()

