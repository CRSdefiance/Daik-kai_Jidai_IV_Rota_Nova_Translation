"""Run the qualified native formatter on the 157 reviewed town speeches and notices."""
import inspect
import sys
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts import plan_rafael_B166_B167_ordinary_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B181_B200_names_v1 import ROOT, CURRENT, OUT as NAMES, PRIOR
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B188_B200_contextual_v1 import OUT as PROSE, BLOCKS


IDENTITY = ROOT / 'town_scoped_runtime_v1.json'
FORMATTING = ROOT / 'town_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'town_visual_preferences_v1.json'
MACROS = previous.MACROS


def prepare():
    assert not any(p.exists() for p in (FORMATTING, PREFERENCES, IDENTITY))
    doc, ident, prior = map(load, (PROSE, NAMES, PRIOR[0]))
    assert ident['runtime'] == doc['runtime'] and ident['exact_prior_ARM9_COMMON_actor_root_and_font']
    assert ident['macro_ascii_lengths'] == prior['macro_ascii_lengths'] == dict(FI=6, FA=6, FO=10, FU=13)
    assert prior['evidence'][str(MACROS)] == sha(MACROS.read_bytes())
    ident.update(actors=[r['actor_ID'] for r in ident['name_bindings']], exact_unchanged_actor0_macro_dependencies=True)
    ident['evidence'][str(MACROS)] = prior['evidence'][str(MACROS)]
    save(IDENTITY, ident)
    for row in doc['records']:
        assert not row['review']['formatting'] and not row['native_literal_tokens'] and row['english'].isascii()
        row['editorial_logical_English'] = row['english']
        row['planned_English_markup'] = f"{{SPEAKER:{row['source_selector']:02X}}}" + row['english']
        row['prior_macro_normalized_comparison'] = None
        if row['kind'] == 'system-FE':
            assert row['source_complete_preamble_hex'] == '0040ffff00fe'
            assert '<' not in row['source_Japanese'] and '＜' not in row['source_Japanese']
            row['FE_is_not_an_ordinary_actor_nameplate'] = True
            row['source_FE_presentation_kind'] = 'Standalone sound effect' if row['source_Japanese'] == 'バタンッ！' else 'Commodity-fashion forecast'
    assert len(doc['records']) == 157
    doc.update(physical_speech_objects=157, typed_choice_objects=0, manuscript_sha256=sha(PROSE.read_bytes()),
        scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()), reused_macro_proof_sha256=sha(MACROS.read_bytes()),
        no_prose_changes_or_manual_breaks=True)
    save(FORMATTING, doc)
    save(PREFERENCES, dict(records={}, progressive_width_px=216, FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True, author_inserted_ordinary_breaks=0, new_credit=0))


source = checked_text(inspect.getsource(previous.qualify_source), {
    "doc['blocks']==[166,167]": "doc['blocks']==BLOCKS",
    'len(bindings)==164': 'len(bindings)==157',
})
scope = {**previous.qualify_source.__globals__, 'CURRENT': CURRENT, 'IDENTITY': IDENTITY, 'BLOCKS': BLOCKS}
exec(compile(source, __file__ + '::source-and-current-town-scope', 'exec'), scope)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1] == '--native':
        del sys.argv[1]
        FunctionType(native.env['main'].__code__, {**native.env, 'IDENTITY': IDENTITY, '__file__': __file__})()
    else:
        FunctionType(previous.env['main'].__code__,
                     {**previous.env, 'qualify_source': scope['qualify_source'], '__file__': __file__})()
