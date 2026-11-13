"""Prepare and plan the reviewed B201–B220 paragraphs, captions, and letter signature."""
import inspect
import sys
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B166_B167_ordinary_v1 as planner
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B201_B220_contextual_v1 import BLOCKS, CURRENT, IDENTITY as GETTERS, OBJECTS, OUT as PROSE, ROOT


IDENTITY = ROOT / 'scoped_runtime_v1.json'
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_FE_inputs_v1.json'
TWO = ROOT / 'two_choice_inputs_v1.json'
THREE = ROOT / 'three_choice_inputs_v1.json'
MACROS = planner.MACROS
STAGED_ID = 'DK4_MES_B216_R0074'
TWO_MENUS = {(208, offset) for offset in (218,582,832,1156,1370,1588)} | {(213,860),(218,836),(218,1006)}


def digest(path):
    return sha(path.read_bytes())


def prepare():
    assert not any(path.exists() for path in (IDENTITY, FORMATTING, PREFERENCES, STAGED, TWO, THREE))
    doc, ident, current, objects, macros = map(load, (PROSE, GETTERS, CURRENT, OBJECTS, MACROS))
    assert doc['runtime'] == ident['runtime'] == current['runtime'] == objects['runtime']
    assert ident['exact_prior_ARM9_COMMON_actor_root_and_font']
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert all(macros['runtime'][key] == ident['runtime'][key] for key in ('ARM9_sha256','COMMON_sha256'))
    assert ident['macro_ascii_lengths'] == dict(FI=6,FA=6,FO=10,FU=13)
    ident.update(actors=[row['actor_ID'] for row in ident['name_bindings']], exact_unchanged_actor0_macro_dependencies=True)
    ident['evidence'][str(MACROS)] = digest(MACROS)
    save(IDENTITY, ident)

    ordinary, staged, two, three = [], [], [], []
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        if row['kind'] == 'typed-choice-label':
            assert row['source_count'] in (2,3) and row['english'].isascii()
            (two if row['source_count'] == 2 else three).append(row)
            continue
        tokens = planner.TOKEN.findall(row['english'])
        assert tokens == row['native_literal_tokens'] and set(tokens) <= {'FI'}
        row['english'] = planner.TOKEN.sub(lambda match: '{MACRO:' + match[0] + '}', row['english'])
        row['planned_English_markup'] = f"{{SPEAKER:{row['source_selector']:02X}}}" + row['english']
        row['prior_macro_normalized_comparison'] = None
        if not row['english'].isascii():
            assert row['decision'] == 'retention' and row['deliberate_source_punctuation_retention']
            assert row['current_comparison_paragraph'] == row['english']
            row['prior_macro_normalized_comparison'] = row['english']
        if row['kind'] == 'system-FE':
            assert row['source_complete_preamble_hex'] == '0040ffff00fe'
            assert row['FE_is_not_an_ordinary_actor_nameplate']
        if row['id'] == STAGED_ID:
            assert row['kind'] == 'system-FE' and not tokens
            assert '\n\u3000\u3000\u3000' in row['source_Japanese']
            assert row['english'] == 'Take care now. Jam Jack Ludwyan'
            row.update(localized_letter_farewell='Take care now.', localized_signature='Jam Jack Ludwyan')
            staged.append(row)
            continue
        ordinary.append(row)
    assert tuple(map(len, (ordinary,staged,two,three))) == (381,1,18,3)
    assert sum(len(r['native_literal_tokens']) for r in ordinary) == 6
    assert sum(r['kind']=='system-FE' for r in ordinary) == 33
    assert {(r['block'],r['source_command_offset']) for r in two} == TWO_MENUS
    assert {(r['block'],r['source_command_offset']) for r in three} == {(209,230)}
    assert len(objects['choice_objects']) == 10 and not objects['style_objects']
    proof = dict(manuscript_sha256=digest(PROSE),scoped_identity_proof_sha256=digest(IDENTITY),
        reused_macro_proof_sha256=digest(MACROS),no_prose_changes_or_manual_breaks=True)
    save(FORMATTING,{**doc,**proof,'records':ordinary+two+three,'physical_speech_objects':381,
        'ordinary_speech_objects':381,'typed_choice_objects':21,'pending_staged_FE_merge':STAGED_ID})
    save(STAGED,{**proof,'runtime':doc['runtime'],'records':staged,'source_staging_only_no_display_approval':True})
    for path, rows in ((TWO,two),(THREE,three)):
        save(path,{**doc,**proof,'records':rows,'typed_choice_objects':len(rows),
            'typed_choice_commands':len({(r['block'],r['source_command_offset']) for r in rows}),
            'physical_speech_objects':0,'ordinary_speech_objects':0})
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))


source = checked_text(inspect.getsource(planner.qualify_source), {
    "doc['blocks']==[166,167]": "doc['blocks']==BLOCKS",
    "c['word'] not in (0x2100,0x2200,0x4100)": "c['word'] != 0x4100",
    "    for row in doc['records']:\n        sr,cr=": "    for row in doc['records']:\n        if row['kind']=='typed-choice-label':\n            continue\n        sr,cr=",
    '    assert len(bindings)==164': "    assert len(bindings)==381 and {r['id'] for r in bindings} == set(originals)-{STAGED_ID}",
})
scope = {**planner.qualify_source.__globals__, 'CURRENT':CURRENT,'IDENTITY':IDENTITY,'BLOCKS':BLOCKS,'STAGED_ID':STAGED_ID}
exec(compile(source,__file__+'::exact-source-and-current-body-bindings','exec'),scope)

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FunctionType(planner.env['main'].__code__,
            {**planner.env,'qualify_source':scope['qualify_source'],'__file__':__file__})()

