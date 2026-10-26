"""Checkpoint B170 reference/gameplay approval; preserve pending counts and main."""
from copy import deepcopy
import gzip
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_reference_checkpoint_v4299')
INPUT = Path('translations/lil_B170_editorial_manuscript_v5.json')
DOC = Path('translations/lil_B170_editorial_manuscript_v6.json')
APPROVAL = Path('work/analysis/lil_B170_reference_approval_v4298/approval_receipt.json')
FAMILY = 'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33'
NEXT = ('Create the atomic B170 compiler with source-bound negative controls, register its profile after the complete V4251 stack, build only through build_integrated_release.py, verify the exact clean-input patch and fresh registered New Game/town startup, then integrate/complete the33 pending records. Existing contextual/native/relocation/reference/content proofs are sealed; do not repeat without a change. Continue B171-B180 and every wider storyline/shared town/shop/random/Help/player-facing prose family. Preserve promoted main V4251 and every ROM, translation, draft, executed producer/proof/failure. Graphics/all18 plaques and the later older-record technical re-audit remain separate and open.')
SUMMARY = '''V4299 seals33 whole-exchange Lil B170 contextual/native/reference/gameplay reviews for registered integration:21 revisions and12 individually justified retentions. Clean Japanese and individual fresh glosses preceded predecessor English comparison. Preserve the collision, rushed apology, irritation, sudden admission of fault, Lil's softening and vanity under flattery, advice request, explicit Admiral claim and FO fleet explanation, money as a question, Yifa fleeing constant scolding during Taoist training, continued practice and desire to become stronger, qualified sympathy, explicit ship-passage request, determination never to lose, prior harsh training and final work-hard encouragement. Use Yifa in source-spoken introductions; the native full nameplate is Yifa Sol. Add no sister relationship, teacher gender/name/school/country/degree, abuse, expulsion, spell, rank, price, romance or numeric skill. All12 working retentions have exact references and individual contextual reasons.

All33 complete216x64 native planes,264 logical/compiled and132 stored alignment cases pass complete first/internal/final glyphs,unique cells,zero row origins,four-row bounds and single-page behavior. Final logical proof has16 fresh/248 exact reused cases;stored targets have76 fresh/56 exact reused cases and19 fresh/14 exact reused planes. Five native sheets were already viewed;all six fresh actual sheets are now viewed.13 source-consumer,two missing-macro and14 formatter negatives pass. Eleven narrow row-count notes exempt no other check. No authored breaks,padding,wording waiver or shared guard/metric change.

Relocation changes only B170 from1860 to1752 stored bytes;target logical end1750. All45 commands,33 complete speeches,twelve nonrelative leaves,one two-byte2000 pause at36/resume38 mapped to32/34,resources6342/632D,presentation commands,later A000 hex1019/2001,C200 and both original ends1852/1856 mapped to1742/1746 remain intact. No relative site,predicate,FE or typed choice is invented. Inverse restoration recovers every predecessor logical byte;all335 other SC2 blocks and every other file/component,ARM9,COMMON,fonts,graphics,cache/BSS and123040 staged bytes remain exact. Both images pass336 original whole loads/cache hits and672 parent modes;three entry censuses,four poisoned-guard end decodes and33 relocated dispatches pass. Original C200 queue writes/all unowned4MiB are preserved;resource boundary and presentation structural reuse is exact and explicitly scoped. Four native full/progressive name consumers bind Lil Argot/Yifa Sol and owned scratch restoration. A000 packed-word semantics and earned recruitment are not inferred.

Two20001-frame Japanese/English cold boots retain all45 source commands plus nine original B22 init commands/four A000s. Both actual paths observe all33 speeches and53 fixture commands;no command is omitted,flattened or forced. Every English panel matches complete native ink/gray masks and paired Japanese portrait/name/upper regions,with zero differences. FI1/FO1 actually display. All six actual sheets,four English full screens andthree Japanese counterparts were viewed. Original full figure,collision/background transition,cleared pause panel,figure removal,resources and normal town return are observed. Pause3200..3332 resumes normally. Final encouragement precedes the source A00011076..11256,C20011256..11257 and first end1852 at11257 in both versions. Whole RGB pause3250 and town-return11290 match. The second declared end1856 has stored/native-decoder coverage only;it is not actually reached. Initialized Amsterdam is a content fixture,not a source-location statement. Natural event170 eligibility,earned flags,full-route completion and hardware verification are not claimed.

Longer captures also observe the same subsequent B120 command sequence ending16053;this adds no fresh editorial/completion credit. Sixty-seven later SeaView frames differ,including source water-depletion and English food-depletion outcomes. These are retained without masking,retiming or an equal-world claim. Two focused20001-frame repeats reproduce each same-ROM screen and command timing exactly. At3250,8410,11290 and16090,paired original funds,ship/models,persistent actor/town/item/goods objects,tasks and calendar fingerprints agree;whole1A04 actor models/captain2 match at11290. PRNG agrees at3250 and differs from8410. Twenty-two source/English speech return timestamps differ while command order/results,pause,effect,C200 and first-end timing agree. Original input-wait,yield,discarded-RAND,generator and wrapper spans are source-exact and rebound to documented V824 scheduler entropy. The observed seed/state pattern is consistent with that mechanism;no fresh B170 every-RAND-call causal trace is claimed. No seed,instruction,outcome or RAM fixture was supplied. Preserve the strict V4294 later-region failure and V4296 combined timing assertion,failed b derivation key and c native-byte serialization attempt;successful successors correct scope/serialization without changing ROMs or prose.

Coverage stays5725 fresh rereads:5692 integrated/completed and33 pending;source/prose5728,including3872 SC2 and64 SC3;route reviewed/completed4126/4093. Historical completed decisions remain3614 revised/2078 retained. New source/prose and completion credit are both0. Promoted main V4251 remains545 manuscript batches/114 accepted layers with its exact clean-input patch. Its registry,profile,builder,main pointer,immutable construction input and all older packages remain unchanged. The two new content-fixture ROMs are pinned;every generated ROM and translation is preserved. Four new cold boots are terminal. Registered B170 compiler,integration,patch and startup checks remain pending.

Remaining B171-B180 has198 physical speeches and zero typed-choice leads,not a full-project denominator. Every wider editorial family remains open. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active.'''


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode()


if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    before_bytes = lp.read_bytes()
    assert sha(before_bytes) == read('work/analysis/promotion_v4289/promotion_receipt.json')['ledger_sha256']
    ledger = json.loads(before_bytes)
    approval, doc = map(read, [APPROVAL, DOC])
    assert approval['manuscripts'] == {str(DOC): sha(DOC.read_bytes())}
    assert approval['new_emulator_runs'] == 4 and len(approval['actual_sampled_display_IDs']) == 33 and not approval['offline_only_display_IDs']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5725, 5692, 33)
    assert len(fresh['pending_contextual_families']) == 1
    pending = fresh['pending_contextual_families'][0]
    assert pending['id'] == FAMILY and pending['manuscript'] == str(INPUT)
    paths = [APPROVAL, DOC, Path(__file__)]
    for key in ['reference_map', 'representative_proof', 'final_padding_proof', 'relocated_control_proof', 'termination_decode_proof', 'focused_repeat_proof']:
        p = Path(doc[key])
        assert sha(p.read_bytes()) == doc[key + '_sha256']
        paths.append(p)
    for p, digest in approval['evidence'].items():
        assert sha(Path(p).read_bytes()) == digest
        paths.append(Path(p))
    evidence = {str(p): sha(p.read_bytes()) for p in paths}
    pending.update(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), manuscripts=approval['manuscripts'], pending=NEXT,
        actual_sampled_display_IDs=approval['actual_sampled_display_IDs'], offline_only_display_IDs=[], new_emulator_runs=4,
        reference_approval=str(APPROVAL), reference_approval_sha256=sha(APPROVAL.read_bytes()))
    fresh.update(latest_contextual_manuscript=str(DOC), latest_pending_contextual_family=FAMILY,
        coverage_note='5725 rereads/5692 integrated/33 pending;B170 native/reference/representative approved. No additional review/completion credit;registered integration remains.')
    active = ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(INPUT)] == [r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(INPUT)] = []
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;33-Lil-B170-reference-approved-pending-registered-release', note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id'] == FAMILY:
            unit.update(**pending, status=doc['status'], actual_new_cold_boot_runs=4, actual_complete_native_panels=33, registered_release_pending=True)
        elif unit['id'] == 'all-route-scenes':
            unit['next'] = NEXT
    oldscope = ledger['unfinished_editorial_scope_v4279']
    assert sha(Path(oldscope['path']).read_bytes()) == oldscope['sha256']
    inventory = deepcopy(read(oldscope['path']))
    inventory.update(next_focus=NEXT)
    inventory['B170_reference_and_actual_coverage_v4299'] = pending
    ROOT.mkdir(parents=True)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4299'] = {**oldscope, 'path': str(inv), 'sha256': sha(inv.read_bytes())}
    ledger['lil_B170_reference_reconciliation_v4299'] = dict(summary=SUMMARY, evidence=evidence, pending_family=pending,
        source_prose_reviews_added=0, completion_credit_added=0, actual_new_cold_boot_runs=4, full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    fixture = read('work/analysis/lil_B170_display_fixture_v4291/complete_effect_preserving_B22_fixtures.json')
    pinned = 0
    for row in fixture['fixtures']:
        rom = Path(row['research_ROM'])
        assert sha(rom.read_bytes()) == row['research_ROM_sha256']
        if not any(p['path'] == str(rom.resolve()) for p in pins):
            pins.append(dict(path=str(rom.resolve()), reason='V4299 B170 source-bound full-content evidence input. Preserve every ROM;no pruning. SHA-256 ' + sha(rom.read_bytes())))
            pinned += 1
    assert pinned == 2
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes, mtime=0))
    planned = {lp: encoded(ledger), pins_path: encoded(pins)}
    section = '## V4299:33 B170 reviews reference/gameplay approved;registered integration pending\n\n' + SUMMARY + '\n\nApproval: ' + APPROVAL.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\nNext: ' + NEXT + '\n\n'
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        planned[path] = (('# Current editorial handoff - V4299' if index == 0 else first) + '\n\n' + section + rest).encode()
    staged = ROOT / 'staged'
    staged.mkdir()
    mutations = []
    for index, (path, data) in enumerate(planned.items()):
        out = staged / (str(index) + '.planned')
        out.write_bytes(data)
        mutations.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(out.resolve()), planned_sha256=sha(data)))
    save(ROOT / 'mutation_plan.json', mutations)
    stable = ['translations/release_stack.json', 'translations/promoted_build.json', 'scripts/build_integrated_release.py']
    stable_hashes = {p: sha(Path(p).read_bytes()) for p in stable}
    for row in mutations:
        assert sha(Path(row['target']).read_bytes()) == row['before_sha256']
        assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
    for row in mutations:
        path, data = Path(row['target']), Path(row['planned']).read_bytes()
        with path.open('r+b') as stream:
            stream.write(data)
            if stream.seek(0, os.SEEK_END) != len(data):
                stream.truncate(len(data))
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(path.read_bytes()) == row['planned_sha256']
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in stable_hashes.items())
    save(ROOT / 'checkpoint_receipt.json', dict(checkpoint='V4299', evidence=evidence, ledger_sha256=sha(lp.read_bytes()),
        fresh_reread=5725, integrated=5692, pending=33, source_prose=5728,
        new_source_prose_reviews=0, new_completed_records=0, preserved_release_files=stable_hashes,
        updated_files={str(Path(row['target']).relative_to(Path.cwd())): row['planned_sha256'] for row in mutations},
        new_emulator_runs=4, actual_complete_native_panels=33, reviewed_sheets=6,
        ROMs_pinned=2, ROMs_deleted=0, all_jobs_terminal=True, full_goal_complete=False))
    print('V4299 checkpoint complete:33 reference-approved pending records;33 actual panels/four boots;2 ROMs pinned. MainV4251,registry,builder and all credit counts preserved.')
