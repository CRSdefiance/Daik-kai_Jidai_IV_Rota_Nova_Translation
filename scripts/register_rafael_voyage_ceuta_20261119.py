"""Register Rafael's revised first voyage and Ceuta tutorial as one candidate."""

from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_voyage_ceuta_20261119 as game
from scripts import prepare_all_routes_promotion_20261111 as runtime
from scripts import register_rafael_tavern_lesson_20261119 as parent
from scripts import review_rafael_voyage_ceuta_20261119 as staged
from scripts import stage_inn_numerals_20261119 as shared_source
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = parent.base, parent.native, parent.workflow
stage = SimpleNamespace(ROOT=staged.STAGED, ROM=staged.ROM, PROOF=staged.PROOF, review=staged, ARM=native.ARM)
PROFILE = 'all-routes-rafael-voyage-ceuta-v1-20261119'
ROOT = Path('out/rafael_voyage_ceuta_registered_20261119_v1')
ROM = ROOT / 'Translation_DS_Rafael_Voyage_Ceuta_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_voyage_ceuta_candidate')
VERIFY, PATCH = PACKAGE / 'verification', PACKAGE / 'translation.xdelta'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_voyage_ceuta_20261119.md')
STARTUP, QA = game.STARTUP, stage.ROOT / 'registered_qa.xml'
verified = SimpleNamespace(PROOF=game.OFFLINE, LIVE=game.PROOF)
CHECKPOINT = 'Rafael’s first-voyage and Ceuta tutorial revisions passed native display checks and ordinary gameplay through the wind question.'
SC0, COMMON = '/data/SC0.DK4', '/COMMON/MESFILE.DK4'
ROW_NOTES = {
    'DK4_MES_B42_R0095': 'Four lines keep the warning, the loan reminder and the final request distinct within one page.',
    'DK4_MES_B127_R0013': 'The complete heading instruction fits a single line.',
    'DK4_MES_B127_R0016': 'The instruction to the crew starts the panel and the steering explanation follows across two lines.',
    'DK4_MES_B127_R0070': 'The first line states the risk and the next line holds all three examples.',
}


def verify(registry, previous, viewed):
    stored, draft, live, layouts, startup = map(base.load, (stage.PROOF, staged.OUTPUT, game.PROOF, game.OFFLINE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == layouts['candidate_sha256'] == startup['candidate_sha256']
    assert stored['predecessor_sha256'] == live['predecessor_sha256'] == previous['candidate_sha256']
    assert stored['manuscript_sha256'] == base.digest(staged.OUTPUT) and stored['whole_parent_inverse']
    assert layouts['stage_proof_sha256'] == base.digest(stage.PROOF) and len(layouts['exact_retentions']) == 35
    assert all(base.digest(p) == digest for proof in (live, startup) for p,digest in proof['evidence'].items())
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert live['ordinary_gameplay_existing_save'] and not live['hardware'] and len(live['panels']) == 44
    assert live['wind_choice_native_result'] == [2,1] and live['unvisited_confident_branch_records'] == ['DK4_MES_B127_R0044']
    assert viewed == {s['path']:s['sha256'] for s in live['sheets']}
    assert all(base.digest(p) == digest for p,digest in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key,0)) for key in ('tests','failures','errors','skipped')] == [51,0,0,2]
    assert (stage.ROOT/'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    old,new = map(native.files,(before,after))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {SC0}
    arm = new[native.ARM]
    assert native.digest(arm) == previous['target_ARM9_sha256']
    runtime.verify_runtime(arm,previous)
    a,b = [native.IlnkContainer.parse(files[SC0]).blocks for files in (old,new)]
    assert stored['changed_blocks'] == {SC0:[42,127]}
    assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x != y] == [42,127]
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    after.replace_file(SC0,old[SC0])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    shared = shared_source.workflow
    directory = native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[COMMON],arm,directory)
    pending = base.load(parent.parent.parent.stage.PENDING)['records']
    assert len(pending) == 276
    assert all(r['current_reference'] == shared.reference(entries[r['message_ID']]) and
               r['current_hex'] == entries[r['message_ID']].text.hex() for r in pending)

    observed = {r['id']:r for r in live['panels']}
    page_proofs = {r['id']:r for r in layouts['revisions']}
    retained = {r['id']:r for r in layouts['exact_retentions']}
    commands = {ident: (c,g['plans'].get(ident)) for g in stored['groups'] for c in g['commands'] for ident in c['record_ids']}
    sha = native.digest(new[SC0])
    assert draft['counts'] == dict(prose=11, wrap=1, retention=35)
    for row in draft['records']:
        ident, block = row['id'], row['block']
        command, plan = commands[ident]
        at, raw = command['stored_offset'],bytes.fromhex(command['stored'])
        assert b[block][at:at+len(raw)] == raw
        if row['source_selector'] is None:
            idx, = row['native_slots']
            count, header = count_and_base(raw)
            assert count == 2 and raw == bytes.fromhex(command['current'])
            value = labels(raw)[idx]
            assert value.hex() == row['current_hex']
            offset = header+unpack_from('<H',raw,2+2*idx)[0]
            row['ordinary_gameplay_verified'] = live['seen_native_choice_labels']
        else:
            offset = 5
            value = raw[5:raw.index(0,6)]
            assert value[0] == row['source_selector']
            if ident in observed:
                row['ordinary_gameplay_verified'] = observed[ident]
            else:
                assert ident in live['unvisited_confident_branch_records'] and ident in retained
                row['focused_offline_reuse'] = retained[ident]
        reference = row['registered_reference'] = dict(candidate_sha256=candidate,file_path=SC0,block=block,
            command_offset=at,offset=at+offset,archive_sha256=sha,exact_stored_hex=value.hex())
        assert b[block][reference['offset']:reference['offset']+len(value)] == value
        if row['decision'] == 'revision':
            assert ident in observed and value.hex() == page_proofs[ident]['target_hex']
            warnings = {issue['code'] for issue in plan.get('diagnostics',())}
            assert warnings == ({'line-break-count'} if ident in ROW_NOTES else set())
            row['compiled_lines'] = plan['lines']
            if warnings:
                row['qa_waivers'] = ['line-break-count']
                row['qa_waiver_reason'] = ROW_NOTES[ident]
        else:
            assert ident in retained and row['current_hex'] == value.hex()
        row['review']['formatting'] = True
    draft.update(candidate_sha256=candidate,formatting_and_registration_pending=False,checked_story_format_guard=controls,
        observed_gameplay=live,direct_visual_review=viewed,shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored,draft,{SC0:sha}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 925 and len(manifest["checks"]) == 260':
        'len(manifest["batches"]) == 926 and len(manifest["checks"]) == 261',
    'verified_deck_after_trade_predecessor': 'verified_tavern_lesson_predecessor',
    'previously_localized_records=7': 'previously_localized_records=47',
    'prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=2':
        'prose_revisions=11, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=35',
    'text_display_revisions=5': 'text_display_revisions=12',
    'for source in (stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,':
        'for source in (stage.PROOF, STARTUP, QA, verified.PROOF, verified.LIVE, args.visual_review,',
    'ordinary_Rafael_Tavern_recruitment_and_assignment=True': 'ordinary_Rafael_voyage_and_Ceuta_wind_choice=True',
    'rafael_tavern_lesson': 'rafael_voyage_ceuta',
    'Preserve the Rafael Tavern Lesson ROM or reconstruction': 'Preserve the Rafael Voyage and Ceuta ROM or reconstruction',
    'glob("staged_tavern_v*")': 'glob("staged_v*")',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael first voyage and Ceuta test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised first-voyage and Ceuta tutorials and earlier candidate fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's first voyage and Ceuta tutorials

The full first-voyage and Ceuta exchanges received 47 source-bound decisions. Eleven prose revisions and one wrap-only revision keep the Port invitation and Julio’s Mediterranean and North Sea advice together, clarify the steering controls, and retain both choice captions and 33 other records exactly. [Source and current references](../{REVIEW.as_posix()})

Ordinary gameplay from the preserved Lisbon save exercised all 28 first-voyage panels and 16 Ceuta panels, selected Rafael's wind question and returned from the tutorial. All 12 revised pages passed a fresh native check and direct visual review. Both choice captions appeared. The confident branch response was retained and checked offline. The comparison ROM has identical voyage and Ceuta script blocks and differs from the immediate parent in the earlier Tavern lesson. [Replay evidence](../{VERIFY.as_posix()}/native_and_ordinary_gameplay.json)

The clean-input patch reconstructs the candidate exactly. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger remains at 27,700 credited reviews and 276 shared entries open. Hardware testing remains open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
exec(compile(program, __file__+'::register', 'exec'),env)


if __name__ == '__main__':
    env['main']()
