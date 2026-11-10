"""Record all contextual decisions and exact name-consumer findings for Rafael B241–B260."""
import inspect
from pathlib import Path

from scripts import write_rafael_B221_B240_contextual_v1 as prior
from scripts.draft_rafael_B249_B260_clean_v1 import OUT as ROOT
from scripts.seal_rafael_B241_B260_clean_v1 import BLOCKS, OUT as SEALED
from scripts.source_locked_derivation_v5118 import checked_text

DRAFTS = SEALED/'sealed_drafts.json'
OUT = Path('translations/rafael_B241_B260_contextual_review_v1.json')
LABELS = Path('translations/rafael_B241_B260_scoped_names_review_v1.json')
DECISIONS = [Path(f'translations/rafael_{part}_contextual_decisions_v1.txt') for part in (
    'B241_B245','B247_B248','B249_B250','B251_B252','B253_B256','B257_B260')]
SIGNATURES = {(247,'50'):'Charles Jean Rochefort',(248,'49'):'Jam Jack Ludwyan'}
FE = {
    (253,'19'):'System handover notice',
    (254,'171'):'System Spirit notice',
    (260,'73'):'Figurehead voice',
    (260,'95'):'System Luck notice', (260,'99'):'System Luck notice',
    (260,'125'):'System Charm notice', (260,'129'):'System Charm notice',
}
GLYPH = 'DK4_MES_B259_R0006'
PUNCTUATION = 'DK4_MES_B251_R0033'
NAMES = {
    0: ('Rafael Castor','Keep the approved name and native FI address.'),
    4: ('Janus Pasar','Keep the approved name in the injured-hand exchange.'),
    5: ('Claudio Manaus','Keep the approved public name for the crewmate who doubts the lead and confronts the swindler.'),
    6: ('Julio Erneco','Keep the approved public name for the reluctant figurehead helper.'),
    11: ('Jam Ludwyan','Keep his approved short public name and distinct full signature.'),
    13: ('Cesare Tony','Keep his established name, including the short stat-notice form.'),
    18: ('Charles Rochefort','Keep his approved short public name and complete letter signature with Jean.'),
    19: ('Carlo Sinat','Keep the approved name for the speaker in the medical-book conversation.'),
    20: ('Fernando Dias','Keep the approved full name and Jam’s familiar Fernando address in prose.'),
    22: ('Samwell Khan','Keep his short public name and separate full catalogue form with da.'),
    23: ('Manuel Almeida','Keep his approved name in the chisel exchange.'),
    67: ('Gabriel Cardocci','Keep the bound character identity in the tavern encounter.'),
    92: ('Barkeep','Keep the tavern role without assigning a family relationship to Francisca.'),
    113: ('Port Worker','Keep the source occupational role for the man with the gloves.'),
    139: ('Priest','Keep the public role and Father as Julio’s direct address in speech.'),
    186: ('Francisca','Keep the approved spelling and correct the full-width initial F in both name consumers.'),
    188: ('Margrete','Keep the source-bound name for the returning visitor’s gold-dust conversation.'),
    193: ('Myrine','Keep the name across the jar rumor and the separate hilltop-ruins exchange.'),
    195: ('Nelly','Keep the established name for the woman who recommends visiting the pyramid.'),
    196: ('Hatra','Keep the name and original FI address in the ruins invitation.'),
}
FULL = {11:'Jam Jack Ludwyan',18:'Charles Jean Rochefort',22:'Samwell da Khan'}

record_source = checked_text(inspect.getsource(prior.review_record),{
    '            assert block == 223\n            kind, speaker = \'system-FE\', FE[key]':
        "            kind, speaker = 'system-FE', FE[block,key]",
    "previous.count('Ｉ') == 2": "previous.count('Ｉ') == 1",
    """    if ident == UNTRANSLATED:
        assert any('\\u3040' <= char <= '\\u9fff' for char in previous) and not retained
        row['current_effective_Japanese_requires_localization'] = True
""": '',
    """    if (block, key) == (223, '17'):
        assert len(draft['source_Japanese'].splitlines()) == 3
        row['source_staged_effect_rows_pending'] = draft['source_Japanese'].splitlines()
""": '',
})
name_source = checked_text(inspect.getsource(prior.name_rows),{
    """        assert forms['progressive-nameplate']['text'] == label
        assert forms['full-catalogue']['text'] == FULL.get(actor, label)""":
        """        if actor == 186:
            assert all(form['text'] == 'Ｆrancisca' for form in forms.values())
        else:
            assert forms['progressive-nameplate']['text'] == label
            assert forms['full-catalogue']['text'] == FULL.get(actor, label)""",
    'RAFAEL221_240_NAME':'RAFAEL241_260_NAME',
    'Rafael SC0 B221–B240':'Rafael SC0 B241–B260',
    "decision='retention', retention_reason=reason, finding=reason, localization_note=reason,":
        """decision='revision' if actor == 186 else 'retention',
            **({} if actor == 186 else {'retention_reason':reason}), finding=reason, localization_note=reason,
            fixed_owned_name_width_correction_required=actor == 186,""",
})
main_source = checked_text(inspect.getsource(prior.main), {
    "'current_effective.json'": "'current_effective.json/current_effective.json'",
    '(234, 29, 7)': '(272, 14, 6)',
    '== 32': '== 16',
    '== 270': '== 292',
    "'DK4_MES_B234_R0005', 'DK4_MES_B236_R0011'": "'DK4_MES_B251_R0020', 'DK4_MES_B251_R0039'",
    """    assert [row['id'] for row in records if row['kind'] == 'system-FE'] == [
        'DK4_MES_B223_R0009', 'DK4_MES_B223_R0017', 'DK4_MES_B223_R0024']""":
        """    assert {(row['block'],str(row['source_record_index'])) for row in records if row['kind']=='system-FE'} == set(FE)""",
    "['FI'], ['FA'], ['FI', 'FA'], ['FA'], ['FO']": "['FI'], ['FI'], ['FI'], ['FI'], ['FI'], ['FI']",
    "            row['approved_item_binding'] = item":
        """            row['approved_item_binding'] = item
        for ident in item['descriptive_or_partial_title_ids']:
            by_id[ident]['related_item_catalogue_binding'] = item""",
    'source_objects=270, ordinary_speech_objects=234':'source_objects=292, ordinary_speech_objects=272',
    'physical_style_alternatives=29, style_objects=4, native_style_slots=32':
        'physical_style_alternatives=14, style_objects=2, native_style_slots=16',
    'typed_choice_objects=7, typed_choice_commands=3, control_only_blocks=[231]':
        'typed_choice_objects=6, typed_choice_commands=3, control_only_blocks=[244], prior_reviewed_context_only_blocks=[246]',
    'untranslated_current_records=[UNTRANSLATED]':'untranslated_current_records=[]',
    "no_global_name_table_changes=True": "one_scoped_name_field_correction_pending=True",
    '270 contextual decisions':'292 contextual decisions',
})
env = {**vars(prior), **globals(), '__file__': __file__}
for name, source in (('read_decisions',inspect.getsource(prior.read_decisions)),
                     ('review_record',record_source),('name_rows',name_source),('main',main_source)):
    exec(compile(source,__file__+'::'+name,'exec'),env)

if __name__ == '__main__':
    env['main']()

