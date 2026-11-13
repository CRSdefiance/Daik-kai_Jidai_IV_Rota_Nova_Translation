"""Seal the stored and representative emulator evidence for all 453 records."""
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B281_B300_research_v1 as previous
from scripts.checkpoint_rafael_B301_B320_display_v1 import LOADERS, LOOKUP, REBUILT, STORED
from scripts.check_rafael_B301_B320_name_planes_v1 import NAMES, RETAINED
from scripts.rebuild_rafael_B301_B320_reviewed_v1 import COMPOUNDS, MENU, VISUAL
from scripts.refine_rafael_B301_B320_plan_v1 import MANUSCRIPT, ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B301_B320_visual_delta_v1 import FINAL as NATIVE, PLAN


FIXTURE = ROOT / 'fixtures_v1/rafael_ruins_rituals_and_crossings_fixture.json'
TERMINAL = ROOT / 'actual_run_v1/terminal.json'
LIVE = ROOT / 'actual_body_v1/focused_actual_pixels.json'
LIVE_MENUS = ROOT / 'actual_menus_v1/menu_actual_pixels.json'
RESEARCH = ROOT / 'research_final_v2'
READY = RESEARCH / 'research_completion.json'
FINAL = Path('translations/rafael_B301_B320_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B301_B320_scoped_names_final_v1.json')


source = checked_text(previous.source, {
    'MANUSCRIPT, PLAN, NATIVE, MENU, COMPOUNDS, VISUAL, NAMES, RETAINED, NAME_PROOF, PROPOSAL)':
        'MANUSCRIPT, PLAN, NATIVE, MENU, COMPOUNDS, VISUAL, NAMES, RETAINED)',
    'visual, names, retained, corrected, proposal = map(load, paths)':
        'visual, names, retained = map(load, paths)',
    "native['runtime'] == proposal['runtime']": "native['runtime'] == retained['runtime']",
    'all240_ordinary_and_style_bodies_checked': 'all442_ordinary_and_style_bodies_checked',
    '(248, 89, 159, 800)': '(444, 156, 288, 630)',
    'list(range(281, 301))': 'list(range(301, 321))',
    "rebuilt['relative_sites'] == 160": "rebuilt['relative_sites'] == 126",
    '== 240 and speech.keys()': '== 442 and speech.keys()',
    "len(captions) == 5 and len(menu['menus']) == len(live_menus['menus']) == 2":
        "len(captions) == 11 and len(menu['menus']) == len(live_menus['menus']) == 5",
    "styles['native_target_slot_cases'] == 88 and len(styles['objects']) == 11":
        "styles['native_target_slot_cases'] == 152 and len(styles['objects']) == 19",
    '== [[0], [0]]': '== [[0]] * 5',
    '(12881, 27, 31)': '(17441, 45, 47)',
    """    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 70} == {'Zaganos Bey'}
    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 65} == {'Plett Perrault'}
    assert fixture['proposed_surname_fields_applied'] and fixture['surname_proof_sha256'] == digest(NAME_PROOF)
    assert corrected['proposal_sha256'] == digest(PROPOSAL) and corrected['original_progressive_andfull_name_getters_pass']
    assert {(row['actor_ID'], row['text']) for row in corrected['versions'][1]['names']['rows']} == {
        (70, 'Zaganos Bey')}""":
        """    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 17} == {'Al Shin'}
    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 197} == {'Safia'}
    assert fixture['all_unowned_files_components_andserialized_parent_inverse_exact']
    assert retained['scoped_actors'] == len(names['records']) == 19""",
    """    arm = Path(corrected['proposed_ARM9']).read_bytes()
    assert sha(arm) == corrected['versions'][1]['ARM9_sha256']""":
        """    assert digest(fixture['research_ROM']) == fixture['research_ROM_sha256']
    arm = NdsImage.open(fixture['research_ROM']).read_file('/__arm9__.bin')
    assert sha(arm) == native['runtime']['ARM9_sha256']""",
    r"""    field, = proposal['fields']
    start = field['physical_offset']
    pointer = field['table_field_offset']
    assert ram[start:start+4] == arm[start:start+4] == b'Bey\0'
    assert ram[pointer:pointer+4] == arm[pointer:pointer+4] == field['pointer'].to_bytes(4, 'little')
""": "",
    " + [live_menus['review_sheet']] + retained['review_sheets']":
        " + [live_menus['review_sheet']]",
    "assert len(sheets) >= 20 and all": "assert len(sheets) >= 30 and all",
    'len(seen) == 27 and len(actors) == 9': 'len(seen) == 45 and len(actors) == 10',
    "ident.startswith('SC0_B293_STYLE_')": "'_STYLE_' in ident",
    "fixture['source_personality_tables_copied_complete'] == 9": "fixture['source_personality_tables_copied_complete'] == 7",
    """    assert {'DK4_MES_B284_R0054', 'DK4_MES_B290_R0008', 'DK4_MES_B292_R0006',
            'DK4_MES_B294_R0006', 'DK4_MES_B300_R0009'} <= seen
    for ident in ('DK4_MES_B293_R0396', 'DK4_MES_B296_R0013', 'DK4_MES_B298_R0046'):""":
        """    assert {'DK4_MES_B306_R0034', 'DK4_MES_B309_R0047', 'DK4_MES_B310_R0057',
            'DK4_MES_B316_R0030', 'DK4_MES_B318_R0198'} <= seen
    for ident in ('DK4_MES_B309_R0059', 'DK4_MES_B313_R0050'):""",
    "{'revision': 202, 'retention': 43}": "{'revision': 397, 'retention': 56}",
    'Rafael B281–B300 exchanges.': 'Rafael B301–B320 exchanges.',
    'total_frames=12881': 'total_frames=17441',
    'source_speech_variants_observed=27': 'source_speech_variants_observed=45',
    'native_body_pages_observed=31': 'native_body_pages_observed=47',
    'actual_choice_labels=5': 'actual_choice_labels=11',
    'offline_only_speech_variants=213': 'offline_only_speech_variants=397',
    """actual_header_Zaganos_Bey=True, actual_header_Plett_Perrault=True,
        proposed_Zaganos_slot_and_pointer_read_back_from_actual_fixture_RAM=True,
        nine_complete_style_commands_observed_under_unmodified_default_roles=True,""":
        """actual_headers_Al_Shin_and_Safia=True, unchanged_ARM9_exact_to_registered_parent=True,
        seven_complete_style_commands_observed_under_unmodified_default_roles=True,""",
    'all_two_menu_instances_default_cursor_and_following_fixture_speech_observed':
        'all_five_menu_instances_default_cursor_and_following_fixture_speech_observed',
    'body_pages=248, observed_pages=31, scoped_public_names=17, typed_labels=5':
        'body_pages=444, observed_pages=47, scoped_public_names=19, typed_labels=11',
    'names.update(all_name_formatting_gates_pending=False':
        "names.update(encoder='dialogue-relocatable-v1', all_name_formatting_gates_pending=False",
    'native_body_pages=248, actual_source_speech_variants=27, actual_body_pages=31, offline_only_source_speech_variants=213':
        'native_body_pages=444, actual_source_speech_variants=45, actual_body_pages=47, offline_only_source_speech_variants=397',
    'records=245, revisions=202, retentions=43, body_pages=248, typed_labels=5, scoped_public_names=17':
        'records=453, revisions=397, retentions=56, body_pages=444, typed_labels=11, scoped_public_names=19',
    'actual_source_variants=27, actual_pages=31, actual_choice_labels=5, actual_menus=2, actual_name_headers=9':
        'actual_source_variants=45, actual_pages=47, actual_choice_labels=11, actual_menus=5, actual_name_headers=10',
    'offline_only_source_variants=213': 'offline_only_source_variants=397',
    'Sealed 245 reviews, 248 stored pages, the corrected surname and 31 focused emulator pages.':
        'Sealed 453 reviews, 444 stored pages, and 47 focused emulator pages.',
})


if __name__ == '__main__':
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::exact-stored-and-initialized-453-object-scope', 'exec'), env)
    env['main']()
