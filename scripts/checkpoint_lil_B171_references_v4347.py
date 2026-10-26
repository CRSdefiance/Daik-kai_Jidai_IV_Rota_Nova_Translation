"""Checkpoint B171 reference/gameplay approval; preserve pending counts and main."""
from copy import deepcopy
import gzip
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_reference_checkpoint_v4347')
INPUT = Path('translations/lil_B171_editorial_manuscript_v4.json')
DOC = Path('translations/lil_B171_editorial_manuscript_v5.json')
APPROVAL = Path('work/analysis/lil_B171_reference_approval_v4346/approval_receipt.json')
FAMILY = 'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37'
NEXT = 'Create the atomic B171 compiler with source-bound negative controls, register its profile after the complete V4303 stack, build only through build_integrated_release.py, verify the exact clean-input patch and fresh registered New Game/town startup, then integrate/complete the37 pending records. Contextual/native/relocation/reference/content proofs are sealed; do not repeat without a change. Continue B172-B180 and every wider storyline/shared town/shop/random/Help/player-facing prose family. Preserve promoted main V4303 and every ROM, translation, draft, executed producer/proof/failure. Graphics/all18 plaques and the later older-record technical re-audit remain separate and open.'
SUMMARY = "V4347 seals37 whole-exchange Lil B171 Sanghyeon visitation and morning follow-up reviews for registered integration:24 revisions and13 individually justified retentions. Clean Japanese and individual fresh glosses preceded predecessor English comparison. Preserve the visitor's respectful/formal call and FI address,introduction,shared teacher and senior training relationship,self-blame for Yifa's unruliness,unauthorized mountain departure to escape training and foreign travel. Preserve this scene's newly supplied unnamed-country travel prohibition,Yifa's apparent ignorance,grave violation and expulsion,formal severed training bond,then childhood upbringing like brother and sister,protective worry,humble guidance request,conditional training/teacher message and farewell. Add no biological kinship,romance,teacher identity/gender,country name,feudal rank,school name,further punishment or lost powers. Preserve Lil's dream uncertainty,Yifa's exuberant interrupted greeting,sensed presence and familiar warmth,her own arts explanation,Lil relaying only training instructions,and the work-first/training-second comic reminder. Spoken Sanghyeon does not add catalogue-only Kan. B170 is not retroactively expanded with B171 facts. Every retained call,pause,reaction,question,closing and siblinglike simile has an individual exact-reference reason.\n\nAll37 complete216x64 native planes,296 fresh logical/compiled and148 stored alignment cases pass complete leading/internal/trailing glyphs,unique cells,zero row origins,four-row bounds and single-page consumption. Stored proofs include88 fresh parity-tail cases/22 planes and60 exact reused cases/15 planes. All five native andseven actual sheets were viewed. Fifteen source-consumer,one missing-FI and14 formatter rejection controls pass;16 narrow row-count notes exempt no other check. No authored breaks,padding,wording waiver or shared guard/metric change.\n\nOnly B171 changes from2120 to2312 stored bytes;logical2120 becomes2310. All45 commands,37 complete speech preambles,selectors02/19/51,eight nonrelative leaves,4500/6000/4621/61FF,resource6325,C200 and both source ends2112/2116 mapped to2302/2306 remain exact. There are no relative sites,predicates,FE,typed choices,2000 pause or source A000. Inverse restoration recovers every predecessor logical byte;all335 other SC2 blocks and every other file/component,ARM9,COMMON,font,graphic,cache/BSS and123040 staged bytes remain exact. Both images pass336 original whole loads/cache hits and672 parent modes;three entry censuses,four poisoned-guard end decodes and37 relocated dispatches pass. Original C200 request[1,0,13,0,0,0,1],owned queue writes and unowned4MiB are preserved. Ten resource boundary cases andfour presentation structural cases are reused only by exact command/runtime binding. Six original progressive/full-name consumers bind Lil Argot,Yifa Sol,Sanghyeon Kan and restore owned scratch/rings and all4MiB. Static selector51 is actor81,not literal Q. Source event171/action172 is bound without claiming earned eligibility.\n\nTwo20001-frame Japanese/English cold boots retain all45 source commands plus nine original B22 init commands/four A000s. Both observe all37 speeches and53 fixture commands,without omission,flattening or forced conditions. Every complete English native ink/gray plane and paired Japanese portrait/name/upper region matches. FI1 actually displays. All seven actual sheets,six English full screens andfour Japanese counterparts were viewed. Original black upper presentation,bedroom fade,waking and morning exchange are observed. First end2112 returns11737/11735;whole RGB town11770 matches. Second end2116 has stored/native-decoder coverage only. Initialized Amsterdam is a content fixture,not a source-location claim. Natural event171 activation,earned flags,full route and hardware verification are not claimed.\n\nThe same following B120 command shape ends16536/16533 without new editorial credit.59 later sampled sailing regions differ,including boat/sea animation and supplies. Two focused repeats reproduce each same-ROM command timing and requested framebuffer exactly. Persistent funds/models/actor/town/item/goods/tasks/calendar fingerprints agree at3130,7510,11770 and16450;whole1A04 actor models and captain2 match at11770. PRNG agrees at3130 and differs in later samples. Twenty-two cross-language command timestamp differences include16 speeches andsix presentation/resource/C200/end commands;order,results and source effects remain intact. Original wait/yield/discarded-RAND/generator/wrapper spans are clean-source exact and rebound to documented V824 scheduler entropy. The pattern is consistent with that mechanism;no new every-RAND causal trace,equal-world claim,seed/instruction/outcome override or RAM fixture is made. Later19990 model/persistent fingerprints differ and remain explicitly recorded.\n\nCoverage stays5762 fresh rereads:5725 completed/integrated and37 pending;source/prose5765,including3909 SC2 and64 SC3;route reviewed/completed4163/4126. Historical completed decisions remain3635 revised/2090 retained. New source/prose and completion credit are both0. Promoted main V4303 remains546 manuscript batches/114 accepted layers with its exact clean-input patch. Registry,profile,builder,main pointer,immutable construction input and every earlier package stay unchanged. Three new research/content ROMs are pinned;every generated ROM and translation is preserved. All four cold boots are terminal. Registered compiler,integration,patch and startup checks remain pending.\n\nRemaining B172-B180 has161 physical speeches and zero typed-choice leads,not a full-project denominator. Every wider editorial family stays open. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active."


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode()


if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    before_bytes = lp.read_bytes()
    assert sha(before_bytes) == read('work/analysis/promotion_v4331/promotion_receipt.json')['ledger_sha256']
    ledger = json.loads(before_bytes)
    approval, doc = map(read, [APPROVAL, DOC])
    assert approval['manuscripts'] == {str(DOC): sha(DOC.read_bytes())}
    assert approval['new_emulator_runs'] == 4 and len(approval['actual_sampled_display_IDs']) == 37 and not approval['offline_only_display_IDs']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'], fresh['fresh_pass_records_integrated'], fresh['fresh_pass_records_pending_native_actual_release']) == (5762, 5725, 37)
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
        coverage_note='5762 rereads/5725 integrated/37 pending;B171 native/reference/representative approved. No additional review/completion credit;registered integration remains.')
    active = ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(INPUT)] == [r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(INPUT)] = []
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;37-Lil-B171-reference-approved-pending-registered-release', note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id'] == FAMILY:
            unit.update(**pending, status=doc['status'], actual_new_cold_boot_runs=4, actual_complete_native_panels=37, registered_release_pending=True)
        elif unit['id'] == 'all-route-scenes':
            unit['next'] = NEXT
    oldscope = ledger['unfinished_editorial_scope_v4329']
    assert sha(Path(oldscope['path']).read_bytes()) == oldscope['sha256']
    inventory = deepcopy(read(oldscope['path']))
    inventory.update(next_focus=NEXT)
    inventory['B171_reference_and_actual_coverage_v4347'] = pending
    ROOT.mkdir(parents=True)
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v4347'] = {**oldscope, 'path': str(inv), 'sha256': sha(inv.read_bytes())}
    ledger['lil_B171_reference_reconciliation_v4347'] = dict(summary=SUMMARY, evidence=evidence, pending_family=pending,
        source_prose_reviews_added=0, completion_credit_added=0, actual_new_cold_boot_runs=4, full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    fixture = read('work/analysis/lil_B171_display_fixture_v4340/complete_effect_preserving_B22_fixtures.json')
    pinned = 0
    for row in fixture['fixtures'] + [read('work/analysis/lil_B171_research_v4335/research_image_receipt.json')]:
        rom = Path(row['research_ROM'])
        assert sha(rom.read_bytes()) == row['research_ROM_sha256']
        if not any(p['path'] == str(rom.resolve()) for p in pins):
            pins.append(dict(path=str(rom.resolve()), reason='V4347 B171 source-bound full-content evidence input. Preserve every ROM;no pruning. SHA-256 ' + sha(rom.read_bytes())))
            pinned += 1
    assert pinned == 3
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]
    (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before_bytes, mtime=0))
    planned = {lp: encoded(ledger), pins_path: encoded(pins)}
    section = '## V4347:37 B171 reviews reference/gameplay approved;registered integration pending\n\n' + SUMMARY + '\n\nApproval: ' + APPROVAL.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '.\n\nNext: ' + NEXT + '\n\n'
    for index, path in enumerate(docs):
        first, rest = path.read_text(encoding='utf-8').split('\n', 1)
        planned[path] = (('# Current editorial handoff - V4347' if index == 0 else first) + '\n\n' + section + rest).encode()
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
    save(ROOT / 'checkpoint_receipt.json', dict(checkpoint='V4347', evidence=evidence, ledger_sha256=sha(lp.read_bytes()),
        fresh_reread=5762, integrated=5725, pending=37, source_prose=5765,
        new_source_prose_reviews=0, new_completed_records=0, preserved_release_files=stable_hashes,
        updated_files={str(Path(row['target']).relative_to(Path.cwd())): row['planned_sha256'] for row in mutations},
        new_emulator_runs=4, actual_complete_native_panels=37, reviewed_sheets=7,
        ROMs_pinned=3, ROMs_deleted=0, all_jobs_terminal=True, full_goal_complete=False))
    print('V4347 checkpoint complete:37 reference-approved pending records;37 actual panels/four boots;3 ROMs pinned. MainV4303,registry,builder and all credit counts preserved.')
