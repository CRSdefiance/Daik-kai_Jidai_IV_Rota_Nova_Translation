"""Publish the two verified compact status layouts on the cumulative candidate."""

from json import dumps
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_town_shortage_20261119 as game
from scripts import stage_inn_numerals_20261119 as shared_source
from scripts import stage_town_shortage_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent,base,native = stage.parent,stage.base,stage.native
workflow = parent.workflow
PROFILE = 'all-routes-town-shortage-v1-20261119'
ROOT = Path('out/town_shortage_registered_20261119_v1')
ROM = ROOT/'Translation_DS_Town_Shortage_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_town_shortage_candidate')
VERIFY,PATCH = PACKAGE/'verification',PACKAGE/'translation.xdelta'
REVIEW,RELEASE = VERIFY/'registered_review.json',VERIFY/'registered_release_verification.json'
DOC = Path('docs/editorial_town_shortage_20261119.md')
STARTUP,QA = game.STARTUP_PROOF,stage.ROOT/'registered_qa.xml'
ORDINARY = stage.ROOT/'ordinary_trade_return_verification.json'
CHECKPOINT = 'The full Shortage status appears in Town Summary and both Market Trade views.'
verified = SimpleNamespace(PROOF=stage.PROOF,LIVE=game.PLAYBACK)


def verify(registry,previous,viewed):
    stored,live,boot,ordinary = map(base.load,(stage.PROOF,game.PLAYBACK,STARTUP,ORDINARY))
    candidate = base.digest(stage.ROM)
    assert candidate == stored['candidate_sha256'] == live['candidate_sha256'] == boot['candidate_sha256'] == ordinary['candidate_sha256']
    assert stored['parent_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert stored['clean_input_sha256'] == previous['clean_input_sha256'] == base.digest(stage.CLEAN)
    assert stored['entire_parent_inverse'] and stored['native_status_domain'] == 256 and len(stored['native_statuses']) == 13
    assert stored['added_trade_stack_bytes'] == stage.NEW_BITMAP_BYTES == 288
    assert all(base.digest(p) == sha for evidence in (stored['source_proofs'],live['evidence'],boot['evidence'],ordinary['evidence'])
               for p,sha in evidence.items())
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert live['pixels_outside_status_exact'] and live['ordinary_input_after_one_Lisbon_status_fixture']
    assert not live['hardware'] and not live['natural_shortage_observed']
    assert ordinary['ordinary_input'] and not ordinary['initialized'] and not ordinary['hardware']
    assert [row['view'] for row in ordinary['normal_status_masks']] == ['Town','Local','Cargo','Market']
    assert ordinary['back_to_Market'] < ordinary['following_Rafael_tutorial'] and len(ordinary['complete_following_text']) == 2
    assert {row['view'] for row in live['case_frames']} == {'Town','Local','Cargo'}
    assert all(row['corrected']['text'] == 'Shortage' and row['original']['text'] == 'Shorta' for row in live['case_frames'])
    assert viewed == {r['path']:r['sha256'] for r in live['sheets']}
    assert all(base.digest(p) == sha for p,sha in viewed.items())
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(key,0)) for key in ('tests','failures','errors','skipped')] == [51,0,0,2]
    assert (stage.ROOT/'clean_rebuilt.nds').read_bytes() == stage.ROM.read_bytes()

    clean,predecessor,target = map(base.NdsImage.open,(stage.CLEAN,parent.ROM,stage.ROM))
    old,new = map(native.files,(predecessor,target))
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {stage.ARM}
    assert native.digest(new[stage.ARM]) == stored['target_ARM9_sha256']
    expected,records,_ = stage.transform(clean.read_file(stage.ARM),old[stage.ARM])
    assert expected == new[stage.ARM] and dumps(records,sort_keys=True) == dumps(stored['records'],sort_keys=True)
    assert stage.trade_entry(clean) == stage.trade_entry(predecessor) == stage.trade_entry(target)
    stage.parent.stage.verify_runtime(expected,previous)
    guard = registry['profiles'][previous['profile']]['source25_multiarchive_guard']
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(controls['source_bound_new_command_counts'].values())
    target.replace_file(stage.ARM,old[stage.ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    shared = shared_source.workflow
    directory = native.digest(expected[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[stage.COMMON],expected,directory)
    pending = base.load(stage.PENDING)['records']
    assert len(pending) == 276
    assert all(row['current_reference'] == shared.reference(entries[row['message_ID']]) and
               row['current_hex'] == entries[row['message_ID']].text.hex() for row in pending)

    record, = records
    record['registered_reference'] = record['staged_reference']|dict(candidate_sha256=candidate)
    review = {key:stored[key] for key in ('translation_policy','target_locale','encoder','review_gates')}
    review.update(candidate_sha256=candidate,records=records,checked_story_format_guard=controls,
        new_contextual_credit=0,shared_storage_scope=base.load(parent.REVIEW)['shared_storage_scope'],
        direct_visual_review=viewed,observed_gameplay=live,ordinary_trade_return=ordinary,native_statuses=stored['native_statuses'],
        source_and_native_dependency_proofs=stored['source_proofs'])
    validate_natural_dialogue_batch(review)
    return stored,review,{stage.ARM:native.digest(expected)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish,{
    'len(manifest["batches"]) == 922 and len(manifest["checks"]) == 257':
        'len(manifest["batches"]) == 923 and len(manifest["checks"]) == 258',
    'verified_trade_categories_predecessor':'verified_town_summary_predecessor',
    'for source in (stage.PROOF, STARTUP, QA, verified.LIVE, args.visual_review,':
        'for source in (stage.PROOF, STARTUP, QA, verified.LIVE, ORDINARY, args.visual_review,',
    'if (row["decision"] != "retention" or row["original_geometry"] != row["staged_geometry"]) and row["id"] not in ids:':
        'if row["display_changed"] and row["id"] not in ids:',
    'if row["original_geometry"] != row["staged_geometry"]':'if row["display_changed"]',
    'town_summary':'town_shortage',
    'reviewed_UI_labels=4':'reviewed_UI_labels=1',
    'previously_localized_records=4':'previously_localized_records=1',
    'prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=3':
        'prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=1',
    'ordinary_Lisbon_Town_Summary=True':'initialized_Lisbon_Town_and_Trade_Shortage=True, ordinary_Trade_return_and_tutorial=True',
    'natural_activation=True, hardware=False':'natural_activation=False, hardware=False',
    'Preserve Town Summary ROM or reconstruction':'Preserve Town Shortage ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Town Shortage test candidate

The [local ROM](../../{ROM.as_posix()}) shows the complete Shortage condition in Town Summary and both Market Trade views.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Compact Shortage status display

Town Summary and Market Trade both clipped Shortage to Shorta. The clean Japanese groups the seven shortages under 品不足 in these compact fields. The existing English word fits the available screen space once the two text fields reserve all eight glyph cells. The full status names and wording carry forward. The original getters were checked for all 256 input values. [Source references and editorial decision](../{REVIEW.as_posix()})

Town Summary uses a disjoint rectangle in its existing text atlas. The first trial widened the source field in place and exposed another field's pixels. Its ROM and captures are preserved. Trade places the wider bitmap in 288 additional bytes within the existing screen's stack allocation. The original allocation and bitmap-construction calls supplied exact runtime addresses and correctly bounded display rectangles. [Checked allocation and display evidence](../{VERIFY.as_posix()})

Paired Lisbon replays set one city-status byte to the stock Luxury Shortage value. Normal inputs reached Town Summary and both Local and Cargo. All three screens showed the full word and all sampled pixels outside the affected fields matched. A separate ordinary replay verified Normal in both Trade views, then returned to the Market and advanced into Julio's navigation tutorial. Natural shortage and hardware remain unvisited. [Before and after](../{VERIFY.as_posix()}/shortage_comparison.png) · [Ordinary Trade return](../{VERIFY.as_posix()}/ordinary_trade_return_verification.json)

The clean-input patch reconstructs the candidate exactly. Six cold-start frames, 24 protected getters, and 49 focused tests passed. Two optional historical fixture tests skipped. All 276 open shared entries carry forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env|globals()
exec(compile(program,__file__+'::register', 'exec'),env)


if __name__ == '__main__':
    env['main']()
