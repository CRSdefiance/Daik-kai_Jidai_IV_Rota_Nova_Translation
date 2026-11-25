"""Seal all 556 reviews against stored bytes and the observed emulator sample."""
from collections import Counter
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B301_B320_research_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B321_B342_name_planes_v1 import NAMES, RETAINED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.rebuild_rafael_B321_B342_reviewed_v1 import COMPOUNDS, MENU, VISUAL
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B321_B342_visual_v1 import FORMATTING as MANUSCRIPT, FINAL as NATIVE, PLAN, ROOT


REBUILT = ROOT / 'rebuilt_v1/reconstruction.json'
STORED = ROOT / 'stored_v1/stored_native_verification.json'
LOOKUP = ROOT / 'stored_catalogue_all_v1/all540_stored_effective_body_bindings.json'
LOADERS = ROOT / 'loaders_v1/verification.json'
FIXTURE = ROOT / 'fixtures_v2/rafael_visits_trials_and_villages_fixture.json'
TERMINAL = ROOT / 'actual_run_v1/terminal.json'
LIVE = ROOT / 'actual_body_v1/focused_actual_pixels.json'
LIVE_MENUS = ROOT / 'actual_menus_v2/menu_actual_pixels.json'
ACTUAL_VISUAL = ROOT / 'actual_visual_approval_v1.json'
RESEARCH = ROOT / 'research_final_v1'
FINAL = Path('translations/rafael_B321_B342_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B321_B342_scoped_names_final_v1.json')
READY = RESEARCH / 'research_completion.json'

source = checked_text(previous.source, {
    "    assert stored['reconstruction_sha256']":
        """    viewed = load(ACTUAL_VISUAL)
    assert viewed['all_actual_body_andmenu_sheets_directly_viewed']
    assert viewed['body_proof_sha256'] == digest(LIVE) and viewed['menu_proof_sha256'] == digest(LIVE_MENUS)
    assert all(digest(row['path']) == row['sha256'] for row in viewed['sheets'])
    assert stored['reconstruction_sha256']""",
    "all442_ordinary_and_style_bodies_checked": "all540_ordinary_and_style_bodies_checked",
    '(444, 156, 288, 630)': '(552, 133, 419, 650)',
    '(343, 40, 646)': '(343, 44, 642)',
    'list(range(301, 321))': 'list(range(321, 343))',
    "rebuilt['relative_sites'] == 126": "rebuilt['relative_sites'] == 130",
    '== len(layouts) == 442': '== len(layouts) == 540',
    "len(captions) == 11 and len(menu['menus']) == len(live_menus['menus']) == 5":
        "len(captions) == 16 and len(menu['menus']) == len(live_menus['menus']) == 7",
    "styles['native_target_slot_cases'] == 152 and len(styles['objects']) == 19":
        "styles['native_target_slot_cases'] == 384 and len(styles['objects']) == 48",
    '== [[0]] * 5': '== [[0]] * 7',
    '(17441, 45, 47)': '(24881, 72, 76)',
    """    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 17} == {'Al Shin'}
    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 197} == {'Safia'}""":
        """    assert {row['expected_actor_ID'] for row in live['headers']} == {row['actor_ID'] for row in names['records']}
    expected_names = {row['actor_ID']: row['english'] for row in names['records']}
    assert all(row['text'] == expected_names[row['expected_actor_ID']] for row in live['headers'])""",
    "retained['scoped_actors'] == len(names['records']) == 19":
        "retained['scoped_actors'] == len(names['records']) == 16",
    'len(seen) == 45 and len(actors) == 10': 'len(seen) == 72 and len(actors) == 16',
    "fixture['source_personality_tables_copied_complete'] == 7": "fixture['source_personality_tables_copied_complete'] == 6",
    """    assert {'DK4_MES_B306_R0034', 'DK4_MES_B309_R0047', 'DK4_MES_B310_R0057',
            'DK4_MES_B316_R0030', 'DK4_MES_B318_R0198'} <= seen
    for ident in ('DK4_MES_B309_R0059', 'DK4_MES_B313_R0050'):""":
        """    assert {'DK4_MES_B321_R0006', 'DK4_MES_B328_R0006', 'DK4_MES_B325_R0188',
            'DK4_MES_B329_R0212', 'DK4_MES_B337_R0095'} <= seen
    for ident in ('DK4_MES_B322_R0044', 'DK4_MES_B335_R0013', 'DK4_MES_B342_R0014', 'DK4_MES_B342_R0075'):""",
    "{'revision': 397, 'retention': 56}": "{'revision': 364, 'retention': 192}",
    'Rafael B301–B320 exchanges.': 'Rafael B321–B342 exchanges.',
    '(*paths, capture, Path(__file__))': '(*paths, ACTUAL_VISUAL, capture, Path(__file__))',
    'total_frames=17441': 'total_frames=24881',
    'source_speech_variants_observed=45': 'source_speech_variants_observed=72',
    'native_body_pages_observed=47': 'native_body_pages_observed=76',
    'actual_choice_labels=11': 'actual_choice_labels=16',
    'offline_only_speech_variants=397': 'offline_only_speech_variants=468',
    'actual_headers_Al_Shin_and_Safia=True': 'all16_scoped_name_headers_observed=True',
    'seven_complete_style_commands_observed': 'six_complete_style_commands_observed',
    'all_five_menu_instances_default_cursor_and_following_fixture_speech_observed':
        'all_seven_menu_instances_default_cursor_and_following_fixture_speech_observed',
    'body_pages=444': 'body_pages=552',
    'observed_pages=47': 'observed_pages=76',
    'scoped_public_names=19': 'scoped_public_names=16',
    'typed_labels=11': 'typed_labels=16',
    "    names.update(encoder='dialogue-relocatable-v1',":
        "    names.update(translation_policy='natural-dialogue-v2', target_locale='en-US', review_gates=doc['review_gates'], encoder='dialogue-relocatable-v1',",
    'actual_source_speech_variants=45': 'actual_source_speech_variants=72',
    'actual_body_pages=47': 'actual_body_pages=76',
    'offline_only_source_speech_variants=397': 'offline_only_source_speech_variants=468',
    'records=453, revisions=397, retentions=56': 'records=556, revisions=364, retentions=192',
    'actual_source_variants=45, actual_pages=47': 'actual_source_variants=72, actual_pages=76',
    'actual_menus=5, actual_name_headers=10': 'actual_menus=7, actual_name_headers=16',
    'offline_only_source_variants=397': 'offline_only_source_variants=468',
    'Sealed 453 reviews, 444 stored pages, and 47 focused emulator pages.':
        'Sealed 556 reviews, 552 stored pages, and 76 focused emulator pages.',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-five-gate-stored-native-and-observed-scope-seal', 'exec'), globals())
    main()
