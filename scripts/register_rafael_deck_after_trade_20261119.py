"""Register the three revised Deck lines and ordinary post-Trade verification."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_deck_after_trade_20261119 as game
from scripts import stage_inn_numerals_20261119 as shared_source
from scripts import stage_rafael_deck_after_trade_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent,base,native = stage.parent,stage.base,stage.native
workflow = parent.workflow
PROFILE = 'all-routes-rafael-deck-after-trade-v1-20261119'
ROOT = Path('out/rafael_deck_after_trade_registered_20261119_v1')
ROM = ROOT/'Translation_DS_Rafael_Deck_After_Trade_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_deck_after_trade_candidate')
VERIFY,PATCH = PACKAGE/'verification',PACKAGE/'translation.xdelta'
REVIEW,RELEASE = VERIFY/'registered_review.json',VERIFY/'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_deck_after_trade_20261119.md')
STARTUP,QA = game.STARTUP,stage.ROOT/'registered_qa.xml'
CHECKPOINT = 'Julio’s three revised Deck lines and all 12 panels pass the ordinary replay from Market Trade.'
verified = SimpleNamespace(PROOF=game.PROOF,LIVE=game.PROOF)
SC0,ARM,COMMON = game.SC0,native.ARM,'/COMMON/MESFILE.DK4'
ROW_COUNT_NOTES = {
    7: 'The question and the spoken lead fill the first line. The description of what navigators do fits on the second.',
    20: 'The sail angle and its relation to the wind stay clear. The one-per-mast rule ends the third line as a whole sentence.',
    23: 'The first line gives the maneuver. The second keeps Julio’s recommendation together.',
}


def verify(registry,previous,viewed):
    stored,live,boot,draft = map(base.load,(stage.PROOF,game.PROOF,STARTUP,stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == boot['candidate_sha256']
    assert stored['predecessor_sha256'] == live['predecessor_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['whole_parent_inverse'] and stored['manuscript_sha256'] == base.digest(stage.review.OUTPUT)
    assert all(base.digest(p) == digest for receipt in (live,boot) for p,digest in receipt['evidence'].items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert live['ordinary_gameplay_existing_save'] and live['native_lesson_event_after_Trade'] and not live['hardware']
    assert live['fully_displayed_live_name_and_regular_F'] and live['speakerless_system_page_exact']
    assert len(live['pairs']) == 12 and live['command_count'] == 16
    assert viewed == {s['path']:s['sha256'] for s in live['sheets']}
    assert all(base.digest(p) == digest for p,digest in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key,0)) for key in ('tests','failures','errors','skipped')] == [51,0,0,2]
    assert (stage.ROOT/'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    assert base.digest(native.CLEAN) == previous['clean_input_sha256']
    clean,predecessor,target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    old,new = map(native.files,(predecessor,target))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {SC0}
    arm = new[ARM]
    assert native.digest(arm) == previous['target_ARM9_sha256']
    parent.stage.parent.stage.verify_runtime(arm,previous)
    assert stored['changed_blocks'] == {SC0:[43]}
    a,b = [native.IlnkContainer.parse(files[SC0]).blocks for files in (old,new)]
    assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x != y] == [43]
    controls = bind_registered_story_percent_guard(registry['profiles'][previous['profile']]['source25_multiarchive_guard'])(native.files(clean),new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    target.replace_file(SC0,old[SC0])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    shared = shared_source.workflow
    directory = native.digest(arm[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[COMMON],arm,directory)
    pending = base.load(parent.stage.PENDING)['records']
    assert len(pending) == 276
    assert all(row['current_reference'] == shared.reference(entries[row['message_ID']]) and
               row['current_hex'] == entries[row['message_ID']].text.hex() for row in pending)

    observed = {r['id']:r for r in live['pairs']}
    assert sum(row['decision'] == 'revision' for row in draft['records']) == 3
    sha = native.digest(new[SC0])
    for r in draft['records']:
        pair = observed[r['id']]
        cmd = pair['command']
        at, raw = cmd['stored_offset'],bytes.fromhex(cmd['stored'])
        assert b[43][at:at+len(raw)] == raw and raw[5] == r['source_selector']
        assert pair['revision'] == (r['decision'] == 'revision')
        r['registered_reference'] = dict(candidate_sha256=candidate,file_path=SC0,block=43,
            command_offset=at,offset=at+5,archive_sha256=sha,exact_stored_hex=raw[5:raw.index(0,6)].hex())
        r['ordinary_gameplay_verified'] = pair['current']
        if pair['revision']:
            plan = stored['groups'][0]['plans'][r['id']]
            assert {item['code'] for item in plan['diagnostics']} == {'line-break-count'}
            r['compiled_lines'] = plan['lines']
            r['qa_waivers'] = ['line-break-count']
            r['qa_waiver_reason'] = ROW_COUNT_NOTES[r['source_reference']['record_index']]
        r['review']['formatting'] = True
    draft.update(candidate_sha256=candidate,formatting_and_registration_pending=False,checked_story_format_guard=controls,
        observed_gameplay=live,direct_visual_review=viewed,shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'])
    validate_natural_dialogue_batch(draft)
    return stored,draft,{SC0:sha}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish,{
    'len(manifest["batches"]) == 923 and len(manifest["checks"]) == 258':
        'len(manifest["batches"]) == 924 and len(manifest["checks"]) == 259',
    'verified_town_summary_predecessor':'verified_town_shortage_predecessor',
    'for source in (stage.PROOF, STARTUP, QA, verified.LIVE, ORDINARY, args.visual_review,':
        'for source in (stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,',
    'if row["display_changed"]':'if row["decision"] == "revision"',
    'owned_label_records':'owned_story_records',
    'target_ARM9_sha256=archives[stage.ARM]':'target_ARM9_sha256=previous["target_ARM9_sha256"]',
    'ARM9_sha256=archives[stage.ARM]':'ARM9_sha256=previous["target_ARM9_sha256"]',
    'reviewed_UI_labels=1':'reviewed_UI_labels=0',
    'previously_localized_records=1':'previously_localized_records=12',
    'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1':
        'prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=9',
    'text_display_revisions=1':'text_display_revisions=3',
    'initialized_Lisbon_Town_and_Trade_Shortage=True, ordinary_Trade_return_and_tutorial=True':
        'ordinary_Rafael_Trade_exit_and_complete_Deck_lesson=True',
    'natural_activation=False, hardware=False':'natural_activation=True, hardware=False',
    'town_shortage':'rafael_deck_after_trade',
    'Preserve Town Shortage ROM or reconstruction':'Preserve Deck After Trade ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael Deck After Trade test candidate

The [local ROM](../../{ROM.as_posix()}) includes three revised Deck tutorial lines after leaving Market Trade.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's Deck lesson after Market Trade

All 12 turns were reread against the clean Japanese. Julio now introduces what he and the other navigators do in his familiar teaching voice. The Sail Handler's sail-angle explanation keeps the one-per-mast rule as a complete clause. The Helmsman line keeps turning the ship quickly in one phrase before Julio gives the battle example. The other nine records retain their exact wording with individual reasons. [Exact source, current and registered references](../{REVIEW.as_posix()})

Paired cold boots with the established Lisbon battery save used ordinary input to exit Trade and reach the original Deck lesson. Both runs verified all 16 commands, 12 complete page masks, 11 Julio nameplates, the speakerless Deck View instruction and the return to Lisbon. The capital F in First uses the regular font and the game substituted Rafael's name. Hardware remains unvisited. [Before and after](../{VERIFY.as_posix()}/ordinary_deck_comparison.png)

Only the Rafael archive's Deck lesson changes. The clean-input patch reconstructs the candidate exactly. Six startup frames, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The registered ASCII right bound, prior Trade and Town fixes and the 276 pending shared records carry forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env|globals()
exec(compile(program,__file__+'::register','exec'),env)


if __name__ == '__main__':
    env['main']()
