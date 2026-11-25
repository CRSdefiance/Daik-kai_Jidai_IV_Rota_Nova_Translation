"""Seal the contextual, stored, and focused emulator evidence for registration."""
import inspect
from collections import Counter
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts import finalize_rafael_B261_B280_research_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B281_B300_retained_name_planes_v1 import NAMES, RETAINED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B281_B300_v1 import FORMATTING as MANUSCRIPT, ROOT
from scripts.prepare_rafael_B281_B300_actual_v1 import NAME_PROOF, PROPOSAL
from scripts.rebuild_rafael_B281_B300_reviewed_v1 import COMPOUNDS, MENU, VISUAL
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B281_B300_visual_delta_v1 import FINAL as NATIVE, PLAN


REBUILT = ROOT / 'rebuilt_v1/reconstruction.json'
STORED = ROOT / 'stored_v2/stored_native_verification.json'
LOOKUP = ROOT / 'stored_catalogue_all_v1/all240_stored_effective_body_bindings.json'
LOADERS = ROOT / 'loaders_v1/verification.json'
FIXTURE = ROOT / 'fixtures_v1/rafael_bear_ruins_and_bounties_fixture.json'
TERMINAL = ROOT / 'actual_run_v1/terminal.json'
LIVE = ROOT / 'actual_body_v1/focused_actual_pixels.json'
LIVE_MENUS = ROOT / 'actual_menus_v1/menu_actual_pixels.json'
RESEARCH = ROOT / 'research_final_v1'
READY = RESEARCH / 'research_completion.json'
FINAL = Path('translations/rafael_B281_B300_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B281_B300_scoped_names_final_v1.json')


source = checked_text(inspect.getsource(previous.main), {
    'all130_ordinary_and_style_bodies_checked': 'all240_ordinary_and_style_bodies_checked',
    '(131, 47, 84, 390)': '(248, 89, 159, 800)',
    'list(range(261, 281))': 'list(range(281, 301))',
    "rebuilt['relative_sites'] == 78": "rebuilt['relative_sites'] == 160",
    '== 130 and speech.keys()': '== 240 and speech.keys()',
    "styles['native_target_slot_cases'] == 16 and len(styles['objects']) == 2":
        "styles['native_target_slot_cases'] == 88 and len(styles['objects']) == 11",
    '(15761, 42, 43)': '(12881, 27, 31)',
    "    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 68} == {'Jacob Portunto'}":
        """    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 70} == {'Zaganos Bey'}
    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 65} == {'Plett Perrault'}""",
    "(65, 'Plett Perrault'), (68, 'Jacob Portunto')": "(70, 'Zaganos Bey')",
    """    assert ram[1184676:1184680] == arm[1184676:1184680]
    assert ram[1424360:1424376] == arm[1424360:1424376]
    assert ram[1432020:1432033] == arm[1432020:1432033]""":
        """    assert ram[1184676:1184680] == arm[1184676:1184680]
    assert ram[1424360:1424376] == arm[1424360:1424376]
    assert ram[1432020:1432033] == arm[1432020:1432033]
    field, = proposal['fields']
    start = field['physical_offset']
    pointer = field['table_field_offset']
    assert ram[start:start+4] == arm[start:start+4] == b'Bey\\0'
    assert ram[pointer:pointer+4] == arm[pointer:pointer+4] == field['pointer'].to_bytes(4, 'little')""",
    "[live_menus['review_sheet'], corrected['review_sheet']]": "[live_menus['review_sheet']]",
    "assert len(sheets) == 16 and all": "assert len(sheets) >= 20 and all",
    "len(seen) == 42 and len(actors) == 10": "len(seen) == 27 and len(actors) == 9",
    """    assert {'SC0_B261_STYLE_342_176', 'SC0_B261_STYLE_852_176', 'DK4_MES_B276_R0047',
            'DK4_MES_B262_R0007', 'DK4_MES_B263_R0006', 'DK4_MES_B264_R0006'} <= seen
    assert {row['page'] for row in live['body_pages'] if row['id'] == 'DK4_MES_B277_R0009'} == {1, 2}""":
        """    assert {row['id'] for row in fixture['selected_records']} == seen
    styles_seen = {ident for ident in seen if ident.startswith('SC0_B293_STYLE_')}
    assert len(styles_seen) == fixture['source_personality_tables_copied_complete'] == 9
    assert {'DK4_MES_B284_R0054', 'DK4_MES_B290_R0008', 'DK4_MES_B292_R0006',
            'DK4_MES_B294_R0006', 'DK4_MES_B300_R0009'} <= seen
    for ident in ('DK4_MES_B293_R0396', 'DK4_MES_B296_R0013', 'DK4_MES_B298_R0046'):
        assert {row['page'] for row in live['body_pages'] if row['id'] == ident} == {1, 2}""",
    "{'revision': 118, 'retention': 17}": "{'revision': 202, 'retention': 43}",
    'Rafael B261–B280 exchanges.': 'Rafael B281–B300 exchanges.',
    'total_frames=15761': 'total_frames=12881',
    'source_speech_variants_observed=42': 'source_speech_variants_observed=27',
    'native_body_pages_observed=43': 'native_body_pages_observed=31',
    'offline_only_speech_variants=88': 'offline_only_speech_variants=213',
    """actual_header_Jacob_Portunto=True,
        proposed_Plett_slot_and_pointer_read_back_from_actual_fixture_RAM=True, actual_Plett_header_unvisited=True,
        both_complete_style_commands_observed_under_unmodified_default_roles=True,""":
        """actual_header_Zaganos_Bey=True, actual_header_Plett_Perrault=True,
        proposed_Zaganos_slot_and_pointer_read_back_from_actual_fixture_RAM=True,
        nine_complete_style_commands_observed_under_unmodified_default_roles=True,""",
    'body_pages=131, observed_pages=43, scoped_public_names=18': 'body_pages=248, observed_pages=31, scoped_public_names=17',
    'native_body_pages=131, actual_source_speech_variants=42, actual_body_pages=43, offline_only_source_speech_variants=88':
        'native_body_pages=248, actual_source_speech_variants=27, actual_body_pages=31, offline_only_source_speech_variants=213',
    'records=135, revisions=118, retentions=17, body_pages=131, typed_labels=5, scoped_public_names=18':
        'records=245, revisions=202, retentions=43, body_pages=248, typed_labels=5, scoped_public_names=17',
    'actual_source_variants=42, actual_pages=43, actual_choice_labels=5, actual_menus=2, actual_name_headers=10':
        'actual_source_variants=27, actual_pages=31, actual_choice_labels=5, actual_menus=2, actual_name_headers=9',
    'offline_only_source_variants=88': 'offline_only_source_variants=213',
    'Sealed 135 reviews, 131 stored pages, both surnames and 43 focused emulator pages.':
        'Sealed 245 reviews, 248 stored pages, the corrected surname and 31 focused emulator pages.',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::exact-stored-and-initialized-245-object-scope', 'exec'), globals())
    main()
