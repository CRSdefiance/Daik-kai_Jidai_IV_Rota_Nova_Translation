"""Register the verified captain-name glyph correction on the cumulative ROM."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import captain_name_latin
from dk4tool.patch.main_pool_cache_visibility import BASE, cache_plan
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_deck_view_guidance_20261119 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_captain_name_latin_20261119 import ARM, CLEAN, PROOF_NAME, ROM_NAME

base, native = parent.base, parent.native
PROFILE = 'all-routes-captain-name-latin-v1-20261119'
ROOT = Path('out/captain_name_latin_registered_20261119_v2')
ROM = ROOT / 'Translation_DS_Captain_Name_Latin_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_captain_name_latin_candidate_v2')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_captain_name_latin_registered_20261119.md')
CHECKPOINT = 'The captain-name glyph correction is registered after the New Game, Continue, Save and Gallery replays.'
STAGE_ROOT = Path('E:/Rota Nova translations/Generated/work/captain_name_latin_20261119_autoload_v2')
SOURCE_REVIEW = Path('work/rafael_custom_name_20261119/custom_name_evidence.json')
stage = SimpleNamespace(ROOT=STAGE_ROOT, ROM=STAGE_ROOT / ROM_NAME, PROOF=STAGE_ROOT / PROOF_NAME, ARM=ARM)
STARTUP, QA = STAGE_ROOT / 'own_startup_verification.json', STAGE_ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=STAGE_ROOT / 'clean_reconstruction.json',
                           LIVE=STAGE_ROOT / 'ordinary_glyph_verification.json')
RUNTIME_IDS = ['DK4_CAPTAIN_NAME_INPUT_LATIN', 'DK4_CAPTAIN_NAME_RESTORED_LATIN', 'DK4_SAVED_SLOT_NAME_LATIN']


def verify(registry, previous, viewed):
    stored, played, boot, reconstruction = map(base.load, (stage.PROOF, verified.LIVE, STARTUP, verified.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == played['candidate_sha256'] == boot['candidate_sha256']
    assert candidate == reconstruction['candidate_sha256']
    assert stored['whole_parent_inverse'] and stored['parent_sha256'] == previous['candidate_sha256']
    assert stored['late_copy_payload_bytes_preserved'] == 123264 and len(stored['field_cases']) == 287
    assert stored['route_cases'] == {'editor_titles': 6, 'key_cases': 18, 'actor_fields': 4, 'slot_display_fields': 1}
    assert len(played['cases']) == 9 and played['battery_saves_unchanged'] and not played['hardware_verified']
    assert all(base.digest(p) == sha for proof in (played['reports'], boot['evidence']) for p, sha in proof.items())
    assert viewed == {played['sheet']: played['sheet_sha256']}
    assert all(base.digest(p) == sha for p, sha in viewed.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert len(boot['gallery_exact_matching_frames']) == 7 and boot['gallery_overlay_and_adjacent_autoload_exact_in_live_itcm']
    (suite,) = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [51, 0, 0, 2]
    assert base.digest(CLEAN) == reconstruction['clean_sha256'] == stored['clean_input_sha256'] == previous['clean_input_sha256']
    assert base.digest(STAGE_ROOT / 'translation_research.xdelta') == reconstruction['patch_sha256']
    assert reconstruction['byte_exact'] and (STAGE_ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds').read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (CLEAN, parent.ROM, stage.ROM))
    old, new = map(native.files, (before, after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {ARM}
    assert before.rom.arm9OverlayTable == after.rom.arm9OverlayTable
    arm = new[ARM]
    recompiled, plan = captain_name_latin.stage(old[ARM], clean.read_file(ARM), before.rom.arm9OverlayTable)
    assert arm == recompiled and plan['target_arm9_sha256'] == stored['target_arm9_sha256']
    assert {str(site): entry for site, entry in plan['hooks'].items()} == stored['hooks']
    assert cache_plan(old[ARM]) == cache_plan(arm)
    inherited_sections = MainCodeFile(arm, BASE)
    assert len(inherited_sections.sections) == 7
    assert inherited_sections.sections.pop().ramAddress == plan['autoload_span'][0]
    # Check the original runtime contract on all six inherited sections and the current main-code bytes.
    verify_runtime(bytes(inherited_sections.save()), previous)
    after.replace_file(ARM, old[ARM])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())

    source_review = base.load(SOURCE_REVIEW)
    assert source_review['candidate_sha256'] == previous['candidate_sha256']
    assert source_review['clean_sha256'] == reconstruction['clean_sha256']
    gates = ['source', 'context', 'localization', 'naturalness', 'formatting']
    context = 'Claudio asks what Rafael thinks of men who go to sea. Rafael hesitates before he answers.'
    rows = []
    for i, row in enumerate(source_review['story_records']):
        assert native.digest(old[row['current']['file_path']]) == row['current']['archive_sha256']
        rows.append(row | {'file_path': row['current']['file_path'], 'speaker': ('Claudio Manaus', 'Rafael')[i],
            'decision': 'retention', 'context': context,
            'source_meaning': ('Claudio asks for Rafael’s opinion of men who sail.', 'Rafael has no ready answer.')[i],
            'localization_note': row['retention_or_revision_reason'], 'review': dict.fromkeys(gates, True),
            'source_reference': row['source'], 'current_reference': row['current'],
            'registered_reference': row['current'] | {'candidate_sha256': candidate}})
    assert [row['id'] for row in rows] == ['DK4_MES_B44_R0017', 'DK4_MES_B44_R0021']
    draft = {'candidate_sha256': candidate, 'translation_policy': 'natural-dialogue-v2', 'encoder': 'dialogue-relocatable-v1',
        'target_locale': 'en-US', 'review_gates': gates, 'records': rows, 'new_contextual_credit': 0,
        'runtime_ids': RUNTIME_IDS, 'autoload_span': plan['autoload_span'], 'observed_gameplay': played,
        'checked_story_format_guard': controls, 'direct_visual_review': viewed,
        'shared_storage_scope': base.load(parent.REVIEW)['shared_storage_scope']}
    validate_natural_dialogue_batch(draft)
    return stored, draft, {ARM: native.digest(arm)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 933 and len(manifest["checks"]) == 268':
        'len(manifest["batches"]) == 934 and len(manifest["checks"]) == 269',
    'verified_artifact_rumor_wraps_predecessor': 'verified_deck_view_guidance_predecessor',
    'previously_localized_records=5': 'previously_localized_records=2',
    'reviewed_UI_labels=5': 'reviewed_UI_labels=0',
    'prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3':
        'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2',
    'text_display_revisions=2': 'text_display_revisions=3',
    'ordinary_Deck_View_and_Filter=True': 'ordinary_custom_name_opening_and_save_lists=True, paired_Gallery=True',
    'deck_view_guidance_release=str(REVIEW)': 'captain_name_latin_release=str(REVIEW), captain_name_autoload=stored["autoload_span"]',
    'deck_view_guidance': 'captain_name_latin',
    '''    for row in draft["records"]:
        ids = manifest["changed_records"][row["file_path"]]
        if row["decision"] == "revision" and row["id"] not in ids:
            ids.append(row["id"])
''': '''    ids = manifest["changed_records"][stage.ARM]
    assert all(ident not in ids for ident in draft["runtime_ids"])
    ids.extend(draft["runtime_ids"])
''',
    'owned_UI_records=[row["registered_reference"] for row in draft["records"] if row["decision"] == "revision"]':
        'owned_runtime_calls=stored["hooks"], autoload_span=stored["autoload_span"]',
    'stage.ROOT / "clean_input.xdelta"': 'stage.ROOT / "translation_research.xdelta"',
    'stage.ROOT / "clean_rebuilt.nds"': 'stage.ROOT / "clean_reconstruction_RESEARCH_ONLY.nds"',
    '*(p for directory in stage.ROOT.parent.glob("staged_v*")\n                    for p in directory.rglob("*.nds"))':
        '*(p for folder in (stage.ROOT.with_name("captain_name_latin_20261119"), '
        'ROOT.with_name("captain_name_latin_registered_20261119_v1")) for p in folder.glob("*.nds") '
        'if p.stat().st_size)',
    'Preserve the Deck View guidance ROM or reconstruction': 'Preserve the captain-name glyph ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Captain-name glyph test candidate

The [local ROM](../../{ROM.as_posix()}) renders Latin letters consistently in edited and previously saved captain names.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing. Hardware testing remains open.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Captain-name glyph correction registered

Rafael’s edited name and the older saved name both use regular-width Latin letters in the tested editor, dialogue, nameplate and Save and Continue menus. The original field sizes, kana, story controls and wording remain intact. The two games loaded from copied saves without changing those copies. [Ordinary replay](../{VERIFY.as_posix()}/ordinary_glyph_verification.json) · [Before and after](../{VERIFY.as_posix()}/name_glyph_comparison.png)

The four hook sites and the new SDK autoload preserve the original late-copy payload and arena reservations. Six startup holds, 24 protected name getters and seven paired Gallery frames matched. Live ITCM confirmed both the overlay and the adjacent autoload remained exact during Gallery navigation. Forty-nine focused repository tests passed, with two optional historical fixtures skipped. [Startup and Gallery checks](../{VERIFY.as_posix()}/own_startup_verification.json)

The clean-input patch reconstructs the candidate byte for byte. The ledger still credits 27,700 reviews, with 276 shared keys open. Hardware testing and promotion acceptance remain open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)  # noqa: S102 -- replay the source-locked release transaction


if __name__ == '__main__':
    env['main']()
