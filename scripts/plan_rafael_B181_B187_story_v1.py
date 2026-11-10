"""Use the qualified progressive and FE formatter for the B181–B187 story exchanges."""
import inspect
import sys
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts import plan_rafael_B188_B200_town_v1 as town
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B181_B187_contextual_v1 import OUT as PROSE, BLOCKS


ROOT, CURRENT, IDENTITY, MACROS = town.ROOT, town.CURRENT, town.IDENTITY, town.MACROS
FORMATTING = ROOT / 'story_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'story_visual_preferences_v1.json'
NAMES = ROOT / 'all_scoped_names_manuscript_v1.json'
TERMS = ('Silla Gold Crown', 'Tomb of King Muryeong', 'Aziza Nurennahar', 'Taoist arts')


def prepare():
    assert not FORMATTING.exists() and not PREFERENCES.exists() and not NAMES.exists()
    doc, identity = map(load, (PROSE, IDENTITY))
    assert identity['runtime'] == doc['runtime'] and identity['exact_prior_ARM9_COMMON_actor_root_and_font']
    assert identity['macro_ascii_lengths'] == dict(FI=6, FA=6, FO=10, FU=13)
    assert identity['evidence'][str(MACROS)] == sha(MACROS.read_bytes())
    assert doc['source_F_literal_token_counts'] == dict(FI=8, FA=1, FO=1)
    prefs = {}
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        tokens = town.previous.TOKEN.findall(row['english'])
        assert tokens == row['native_literal_tokens']
        row['english'] = town.previous.TOKEN.sub(lambda match: '{MACRO:' + match[0] + '}', row['english'])
        row['planned_English_markup'] = f"{{SPEAKER:{row['source_selector']:02X}}}" + row['english']
        row['prior_macro_normalized_comparison'] = None
        if not row['english'].isascii():
            assert row['decision'] == 'retention' and row['deliberate_source_punctuation_retention']
            assert row['english'] == row['current_comparison_paragraph']
            row['prior_macro_normalized_comparison'] = row['english']
        if row['kind'] == 'system-FE':
            assert row['block'] == 187 and row['semantic_speaker_actor_ID'] == 27
            assert row['source_complete_preamble_hex'] == '0040ffff00fe'
            row['FE_is_not_an_ordinary_actor_nameplate'] = True
            row['source_FE_presentation_kind'] = 'Aziza exchange with original FE selector and source events'
        phrases = [term for term in TERMS if term in row['english']]
        if phrases:
            prefs[row['id']] = dict(line_phrases=phrases, reason='Keep the named identity, item, site, or art together.',
                bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    assert len(doc['records']) == 227
    doc.update(physical_speech_objects=227, typed_choice_objects=0, manuscript_sha256=sha(PROSE.read_bytes()),
        scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()), reused_macro_proof_sha256=sha(MACROS.read_bytes()),
        no_prose_changes_or_manual_breaks=True)
    save(FORMATTING, doc)
    save(PREFERENCES, dict(records=prefs, progressive_width_px=216, FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True, author_inserted_ordinary_breaks=0, new_credit=0))
    from scripts.write_rafael_B181_B187_contextual_v1 import LABELS as story_labels
    from scripts.write_rafael_B188_B200_contextual_v1 import LABELS as town_labels
    first, second = map(load, (story_labels, town_labels))
    assert first['runtime'] == second['runtime'] == doc['runtime']
    names = first['records'] + second['records']
    assert len(names) == len({r['actor_ID'] for r in names}) == 29
    assert {r['actor_ID'] for r in names} == set(identity['actors'])
    save(NAMES, dict(format=first['format'], translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=names, runtime=doc['runtime'], all_name_formatting_gates_pending=True,
        no_global_name_table_changes=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in (story_labels,town_labels,IDENTITY)}))


source = checked_text(inspect.getsource(town.previous.qualify_source), {
    "doc['blocks']==[166,167]": "doc['blocks']==BLOCKS",
    'len(bindings)==164': 'len(bindings)==227',
})
scope = {**town.previous.qualify_source.__globals__, 'CURRENT': CURRENT, 'IDENTITY': IDENTITY, 'BLOCKS': BLOCKS}
exec(compile(source, __file__ + '::exact-source-and-current-story-scope', 'exec'), scope)

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FunctionType(town.previous.env['main'].__code__,
            {**town.previous.env, 'qualify_source': scope['qualify_source'], '__file__': __file__})()
