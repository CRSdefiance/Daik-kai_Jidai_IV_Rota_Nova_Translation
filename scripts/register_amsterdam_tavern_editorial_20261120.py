"""Register the source-bound Amsterdam Tavern follow-up on the current cumulative ROM."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_amsterdam_tavern_editorial_20261120 as tavern
from scripts import register_captain_name_latin_20261119 as parent
from scripts.check_captain_name_release_20261119 import BASE, POOL, START_FRAMES, cache_plan, equal_screens
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_town_shortage_20261119 import PENDING
from scripts.verify_release_baseline import files


base, native, workflow = parent.base, parent.native, parent.env['workflow']
stage = SimpleNamespace(ROOT=tavern.ROOT, ROM=tavern.ROOT / 'candidate.nds',
                        PROOF=tavern.ROOT / 'staging.json', ARM=tavern.ARM)
verified = SimpleNamespace(PROOF=tavern.NATIVE, LIVE=tavern.MANUSCRIPT)
PROFILE = 'all-routes-amsterdam-tavern-editorial-v1-20261120'
ROOT = Path('out/amsterdam_tavern_editorial_registered_20261120_v1')
ROM = ROOT / 'Translation_DS_Amsterdam_Tavern_20261120_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261120_amsterdam_tavern_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_amsterdam_tavern_registered_20261120.md')
STARTUP, QA = tavern.ROOT / 'own_startup_verification.json', tavern.ROOT / 'qa_retry.xml'
STARTUP_CAPTURE = tavern.REPLAY.parent / 'release_startup/capture/capture_report.json'
VISUAL = tavern.ROOT / 'visual_review.json'
CHECKPOINT = 'Two Wanda lines are revised and registered. Both drink responses and two Tavern rumors were verified in ordinary Amsterdam gameplay.'


def startup_proof(previous, candidate, arm):
    prior_proof_path = Path(previous['own_registered_startup'])
    assert base.digest(prior_proof_path) == previous['own_registered_startup_sha256']
    prior_proof = base.load(prior_proof_path)
    old_capture = Path(prior_proof['exact_matching_frames'][0]['path']).parent / 'capture_report.json'
    old, _ = checked_report(old_capture, previous['candidate_sha256'], START_FRAMES[-1])
    new, ram = checked_report(STARTUP_CAPTURE, candidate, START_FRAMES[-1])
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options']
    assert all(old['battery_save_preloaded'][key] == new['battery_save_preloaded'][key]
               for key in ('source', 'source_sha256', 'copied_byte_exact_before_cold_boot'))
    holds = equal_screens(old, new, START_FRAMES)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == cache_plan(arm)['payload_bytes'] == 123264
    assert ram[POOL - BASE:POOL - BASE + len(payload)] == payload
    assert ram[DIRECTORY_OFFSET:TABLE_END] == arm[DIRECTORY_OFFSET:TABLE_END]
    getters_path = Path('work/ship_command_label_release_v1/own_registered_name_getters_v1.json')
    original = base.load(getters_path)['own_name_consumers']['rows']
    cpu, get = tavern.get_machine(arm, ram)
    assert get(0x7F244) == 3
    rows = []
    for row in original:
        value = bytes.fromhex(row['text_hex'])
        ptr = get(row['getter'] - BASE, row['actor_object'])
        assert bytes(cpu.mem_read(ptr, len(value) + 1)) == value + b'\0'
        rows.append({key: row[key] for key in ('actor_ID', 'consumer', 'getter', 'text', 'text_hex')})
    assert rows == prior_proof['original_protected_name_getters'] and len(rows) == 24
    result = dict(candidate_sha256=candidate, cold_boot=True, savestate=False, exact_matching_frames=holds,
                  complete_deployed_payload_exact=True, actual_captain_getter=3,
                  original_protected_name_getters=rows, read_only_snapshot=new['read_only_RAM_snapshot'],
                  original_ARM9_and_overlay_preserved=True, hardware=False,
                  evidence={str(path): base.digest(path) for path in (prior_proof_path, old_capture, STARTUP_CAPTURE, getters_path)})
    if STARTUP.exists():
        assert base.load(STARTUP) == result
    else:
        base.save(STARTUP, result)


def verify_editorial(registry, previous, viewed):
    stored, draft = map(base.load, (stage.PROOF, verified.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['target'] == draft['candidate_sha256']
    assert base.digest(parent.ROM) == stored['parent'] == previous['candidate_sha256'] == draft['parent_sha256']
    clean_path = Path('work/clean.nds')
    assert base.digest(clean_path) == draft['clean_input_sha256'] == previous['clean_input_sha256']
    assert stored['complete_inverse'] and stored['verified_table_entries'] == 3668
    assert {int(n) for n in stored['allocations']} == set(tavern.EDITS)
    assert viewed == {str(path): base.digest(path) for path in (tavern.SHEET, tavern.ROOT / 'tavern_comparison.png')}
    assert viewed[str(tavern.SHEET)] == draft['viewed_native_sheet']
    assert {number for _, number, _ in tavern.EVENTS} == tavern.DECISIONS.keys() - {657}
    assert len(draft['records']) == 11 and len(draft['native_formatting']['cases']) == 35
    assert all(base.digest(path) == sha for path, sha in draft['capture_reports'].items())
    for row in draft['records']:
        for event in row['observed_gameplay']:
            assert all(base.digest(value['image']) == value['sha256']
                       for key, value in event.items() if key in ('previous', 'staged'))
    for frame in (21250, 23890):
        # Compare the complete Yes and No button region independently of the body.
        pair = [tavern.Image.open(tavern.path_at(path, frame)).convert('RGB')
                for path in (tavern.PREVIOUS, tavern.REPLAY)]
        assert pair[0].crop((100, 340, 250, 380)).tobytes() == pair[1].crop((100, 340, 250, 380)).tobytes()
    assert draft['tavern_menu_stock_return_frames'] == [19560, 22240, 24550]
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key, 0)) for key in ('tests', 'failures', 'errors', 'skipped')] == [32, 0, 0, 2]
    assert (stage.ROOT / 'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, old, new = map(base.NdsImage.open, (clean_path, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {tavern.COMMON}
    arm, common = after[tavern.ARM], after[tavern.COMMON]
    assert native.digest(arm) == previous['target_ARM9_sha256'] and native.digest(common) == stored['common']
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    new.replace_file(tavern.COMMON, before[tavern.COMMON])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    entries = tavern.owned_entries(common, arm, native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    pending = base.load(PENDING)['records']
    assert len(pending) == 276
    assert all(tavern.reference(entries[row['message_ID']]) == row['current_reference']
               and entries[row['message_ID']].text.hex() == row['current_hex'] for row in pending)
    for row in draft['records']:
        entry = entries[row['message_ID']]
        assert row['staged_hex'] == entry.text.hex() and row['staged_reference'] == tavern.reference(entry)
        row['registered_reference'] = row['staged_reference'] | dict(candidate_sha256=candidate)
    draft.update(checked_story_format_guard=controls, direct_visual_review=viewed, preserved_pending_shared_rows=276,
                 shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {tavern.COMMON: native.digest(common)}


def verify(registry, previous, viewed):
    result = verify_editorial(registry, previous, viewed)
    startup_proof(previous, result[1]['candidate_sha256'], base.NdsImage.open(stage.ROM).read_file(tavern.ARM))
    return result


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 934 and len(manifest["checks"]) == 269':
        'len(manifest["batches"]) == 935 and len(manifest["checks"]) == 270',
    'verified_deck_view_guidance_predecessor=predecessor, captain_name_latin_release=str(REVIEW), captain_name_autoload=stored["autoload_span"]':
        'verified_captain_name_latin_predecessor=predecessor, amsterdam_tavern_release=str(REVIEW)',
    'release_stack_before_captain_name_latin.json': 'release_stack_before_amsterdam_tavern.json',
    'release_stack_with_captain_name_latin.json': 'release_stack_with_amsterdam_tavern.json',
    'registered_captain_name_latin_and_complete_parent_inverse': 'registered_amsterdam_tavern_and_complete_parent_inverse',
    'manifest["captain_name_latin_pipeline"]': 'manifest["amsterdam_tavern_pipeline"]',
    '''    ids = manifest["changed_records"][stage.ARM]
    assert all(ident not in ids for ident in draft["runtime_ids"])
    ids.extend(draft["runtime_ids"])
''': '''    assert all((row["file_path"], row["id"]) in credited for row in draft["records"])
    ids = manifest["changed_records"][tavern.COMMON]
    for row in draft["records"]:
        if row["decision"] == "revision" and row["id"] not in ids:
            ids.append(row["id"])
''',
    'owned_runtime_calls=stored["hooks"], autoload_span=stored["autoload_span"], target_ARM9_sha256=archives[stage.ARM]':
        'owned_shared_allocations=stored["allocations"], target_COMMON_sha256=archives[tavern.COMMON]',
    'changed_components=1, target_ARM9_sha256=archives[stage.ARM]':
        'changed_components=1, target_COMMON_sha256=archives[tavern.COMMON]',
    'ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous["target_COMMON_sha256"]':
        'ARM9_sha256=previous["target_ARM9_sha256"], MESFILE_sha256=archives[tavern.COMMON]',
    'ledger["captain_name_latin_20261119"]': 'ledger["amsterdam_tavern_editorial_20261120"]',
    'previously_localized_records=2': 'previously_localized_records=11',
    'repository_tests=49': 'repository_tests=30',
    'text_display_revisions=3': 'text_display_revisions=0',
    'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2':
        'prose_revisions=2, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=9',
    'ordinary_custom_name_opening_and_save_lists=True, paired_Gallery=True':
        'ordinary_Amsterdam_drink_offer_both_responses=True, ordinary_tavern_rumors=True',
    'translation_research.xdelta': 'translation.xdelta',
    'clean_reconstruction_RESEARCH_ONLY.nds': 'clean_rebuilt.nds',
    '*(p for folder in (stage.ROOT.with_name("captain_name_latin_20261119"), ROOT.with_name("captain_name_latin_registered_20261119_v1")) for p in folder.glob("*.nds") if p.stat().st_size)':
        'stage.ROOT.with_name("amsterdam_tavern_editorial_20261120_v1") / "candidate.nds"',
    'Preserve the captain-name glyph ROM or reconstruction': 'Preserve the Amsterdam Tavern ROM or reconstruction',
    '# Current editorial checkpoint - 2026-11-19': '# Current editorial checkpoint - 2026-11-20',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Amsterdam Tavern test candidate

Wanda now asks “How about one more drink?” Her toast reads “Lil, huh? Cheers! Glad we met.” The name comes from the current captain.
The [local ROM](../../{ROM.as_posix()}) includes the registered corrections from the preceding candidate.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Amsterdam Tavern conversation review

Wanda’s offer is a question that matches the Yes and No choices. The toast keeps her quick name check and the friendly intent of getting acquainted. The revised invitation and toast fit on one line for Lil. Longer tested names carry “Glad we met.” intact onto a second line. Nine existing records have individual reasons for retaining their wording. [Source and current references](../{REVIEW.as_posix()})

The ordinary Lil replay exercised both drink responses, two local rumors and the returns to the Tavern menu. The registered predecessor also showed the whole Jewelry Shop referral with “aren’t you?” together. Offline native checks covered 35 pages, including ASCII and mixed-width name substitutions. Unvisited Tavern options and hardware remain open. [Native pages](../{(VERIFY / tavern.SHEET.name).as_posix()}) · [Before and after](../{(VERIFY / "tavern_comparison.png").as_posix()})

Six startup holds and 24 protected name getters passed. Thirty focused tests passed and two optional historical cases skipped. The patch rebuilds the candidate exactly from clean input. The existing review count is still 27,700 with 276 mapped shared entries open. [Registered candidate](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__ + '::register', 'exec'), env)  # Replay the checked cumulative release transaction.


if __name__ == '__main__':
    env['main']()
