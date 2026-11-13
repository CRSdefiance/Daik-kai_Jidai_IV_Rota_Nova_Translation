"""Record verified runtime research without claiming editorial integration."""

import shutil
from pathlib import Path

from dk4tool.patch import item_diplomacy_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_item_runtime_storage_v785 import CURRENT, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/item_diplomacy_runtime_v785_research.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V785 Item and diplomacy runtime research')

SUMMARY = (
    'V785 verifies the proposed item/diplomacy selector in existing memory: '
    '35,072 exact routing/register cases, 140 complete 8 MiB status contracts, '
    'unchanged external private-bank references, ARMv5-compatible instructions, '
    '40 unchanged type-getter cases and preserved repaired shop formatting. '
    'An initial storage lead was rejected because V626 already uses it for live code. '
    'The replacement uses a source-bounded Extras text tail with original data-consumer controls. '
    'Six complete nominal phrases have a 110-byte placement proposal in 132 source-bound bytes; '
    'two village-reference leads are classified by executing their original instruction pairs. '
    'Full getter consumers, runtime writes, Guild context, production layouts, COMMON integration, '
    'registered ROM/patch and actual scenes remain pending. V783 stays current; '
    '417 complete, 496 source/prose and 79 drafts are unchanged. The separate graphics audit remains open.'
)


def main():
    plan = read(ROOT/'runtime_plan.json')
    audit = read(ROOT/'preservation_audit.json')
    scope = read(ROOT/'scope_proof.json')
    status = read(ROOT/'status_contracts.json')
    storage = read(ROOT/'type_phrase_storage_research.json')
    assert scope['cases'] == 35072 and status['count'] == 140
    assert audit['all40_type_getter_cases_pass'] and audit['user676_677_repaired_formatting_preserved']
    assert plan['source_ROM_sha256'] == sha(CURRENT.read_bytes())
    assert plan['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert sha((ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()) == audit['research_ARM9_sha256']
    assert sum(r['bytes'] for r in storage['proposed110_phrase_bytes']) == 110
    assert len(storage['two_exact_source_instruction_pair_classifications']) == 2
    for name in ('scripts/verify_item_runtime_v785.py', 'scripts/audit_item_runtime_storage_v785.py',
                 'scripts/research_item_type_storage_v785.py'):
        proof = plan if 'verify_' in name else audit if 'audit_' in name else storage
        assert proof['producer_sha256'] == sha(Path(name).read_bytes())
    cfg = read('translations/shared_dialogue_editorial_release_v2.json')
    for name, expected in cfg['dependencies'].items():
        assert sha(Path(name).read_bytes()) == expected, name
    assert sha(Path(cfg['manuscript']).read_bytes()) == cfg['manuscript_sha256']
    protected = read('work/analysis/shared_metadata_v783/verification.json')['protected_files_unchanged']
    protected = dict(protected)
    protected.update({str(CURRENT): '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d',
        str(CURRENT.with_suffix('.xdelta')): '9a23ef0e69dea7a460e48c35e9278936344778d20b93cb1161441f2c56014b7f',
        'translations/item_diplomacy_editorial_manuscript_v1.json':
            read('work/analysis/item_diplomacy_editorial_v784/layout_prototypes/verification.json')['manuscript_sha256']})
    for name, expected in protected.items():
        assert sha(Path(name).read_bytes()) == expected, name

    DOC.write_text('''# V785: item-shop and diplomatic-letter runtime research

## Current release and editorial coverage

V783 remains the current registered, batch-verified experimental ROM and patch.
This checkpoint creates no playable ROM, changes no production COMMON text,
and grants no additional completed-entry or production-formatting approval.
The ledger remains **417 completed entries, 496 source/prose reviews and 79 drafts**.
The next batch is still COMMON 1070–1145: 63 proposed revisions and 13 retained
wordings. The separate graphics audit, including the original 18 plaques,
remains unfinished. The Online screenshot-body exclusion, preserved brown marks,
approved character names and older-record follow-up remain in force.

## Runtime progress

The extended selector fits its existing 128-byte table and 172-byte gate bank.
It uses an 11-bit start and 5-bit interval length, preserving exact memberships.
Role-table keys retain 32-byte alignment; the older queued tables retain
16-byte alignment. Pointer keys are biased away from numeric coordinate/status
IDs. This fixes a collision found during prototyping before any ROM was built.

Six guarded changes produce research ARM9 SHA-256
`288bcbfa29e2cbc6df81326bade9f074c156148cf2c2749ccabc0c570bbba4bf`.
The source ARM9 is V783's
`daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02`.
No section, BSS, cache, startup, arena or 123,040-byte staged-payload geometry grows.
Every byte outside the six declared patches is restored and compared exactly.

| Evidence | Verified scope |
| --- | --- |
| 35,072 native selector cases | Exact old/new memberships, tested intervening/unaligned keys, wrong parents/high halves, registers, SP and LR |
| 140 status contracts | Complete 8 MiB guards, old UI names, all tested status sentences and ABI |
| Private reference census | Earlier external incoming contracts preserved, including the documented V772 bridge rebind |
| Instruction audit | Exact new code extents contain Thumb-1 and ARMv5 BL/BLX instructions |
| 40 original getter cases | Both type getters, all ten types, exact pointers/text, complete 8 MiB preservation and callee-saved ABI |
| COMMON 676/677 | Repaired native wrapping and complete text preserved in research bytes |

These are targeted native CPU tests. No new gameplay capture, complete playthrough,
hardware validation or new shop-scene activation is claimed. The V747 shop
framebuffer remains the actual scene reference for the user's formatting example.

## Storage conflict caught and corrected

The initial 0214C550–0214C564 lead is **rejected**. Although the Japanese label
table no longer points there, V626 already installs live strategist alignment
code in those bytes. An absence of absolute pointers was not ownership proof.
The source-byte guard stopped the prototype before a ROM could be produced.
V626's complete alignment/fallback bytes remain unchanged.

The moved `major economic boom` constant instead uses 20 bytes at
0216DEFC in the original Extras tie-in introduction's documented allocation.
Its complete translated prefix and terminating NUL remain exact. Absolute,
ARM/ADR, Thumb and crossing-string leads are inspected. Two apparent ARM
branches are words in the unchanged 0216215C–0216515C coordinate array:
its original base literal and consumer are pinned, and the original halfword
streaming instructions reproduce both coordinate pairs. These two cases are
qualified individually; there is no general data-range or unaligned-reference waiver.

## Six letter-type names

The V783 and research getters still return Japanese for types 0–5.
Types 6–9 remain exactly `Lure Fleet`, `Forge Papers`, `Bad Rumors` and `Bribe`.
The six proposed English document names are:

- goodwill letter
- pact proposal
- pact termination notice
- truce proposal
- declaration of war
- demand for submission

`Pact termination notice` is the revised nominal rendering of 協定破約.
It expresses the same complete notice and termination meaning as the earlier
`notice of pact termination` draft and reads naturally after `our` and `this`.
The original V784 plan and manuscript remain intact; the V2 proposal is separate.
The earlier prototype layouts using the old nominal phrase are not relabeled
as approval of the new getter output.

The six complete NUL-terminated names need 110 bytes. A nonoverlapping placement
fits within 132 source-bound bytes: three original scheme-label groups and two
retired village clues. Both complete active village replacements still match.
The two apparent village pointers span original MOV/BL instruction words;
both exact original instruction pairs are executed to their real callees with
argument, LR and whole-memory guards. All other current direct leads are the
six original type-table fields, which require an atomic registered redirect.
The intervening `7CScheme` RTTI name, adjacent code and all earlier text are preserved.

This is a **placement proposal**, not permission to overwrite the source labels.
Complete computed/virtual getter consumers, immutable-use/write closure and
display bounds/crops must be established first. Some consumers may require
context-specific nominal wording; the current 93D28/93D5C getter behavior is unchanged.

## Remaining batch work

1. Close original Guild constructor/NPC context, branch eligibility and arguments.
2. Map every relevant letter-name consumer, including virtual getters and crops;
   finish write exclusions and implement the six names through source guards.
3. Produce current native layouts and full font previews for every revised
   argument/output path, including the revised type-2 phrase.
4. Integrate all 76 paragraphs through natural-dialogue-v2 and the registered
   full release stack. Verify complete copies and exact clean-input patch.
5. Test representative actual buy/sell/bargain and diplomatic scenes, ordinary
   startup, scene transitions, bounds, pagination and complete letters.

Then continue COMMON 1146 onward, resolve 750–752 and review all routes and
remaining prose. No completion claim or canonical promotion is made.

## Evidence and reproduction

Research: `work/analysis/item_diplomacy_runtime_v785`.
Run `scripts/verify_item_runtime_v785.py`,
`scripts/audit_item_runtime_storage_v785.py`,
`scripts/research_item_type_storage_v785.py`, then
`scripts/record_item_runtime_v785.py` with the repository Python dependencies.
Research and producers are copied with SHA-256 receipts to
`E:/Rota Nova translations/Editorial review/V785 Item and diplomacy runtime research`.
No new guide screenshots, commit or GitHub push is produced.
''', encoding='utf-8')

    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 417
    assert ledger['records_with_source_and_prose_pass'] == 496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs']) == 79
    snapshot = ROOT/'editorial_ledger_before_v785.json'
    if not snapshot.exists():
        save(snapshot, ledger)
    ledger['latest_checkpoint'] = SUMMARY
    ledger['latest_runtime_research'] = {
        'checkpoint': str(DOC), 'proof': str(ROOT/'checkpoint.json'),
        'selector_cases': 35072, 'status_contracts': 140,
        'source_bound_type_phrase_placement': str(ROOT/'type_phrase_storage_research.json'),
        'type_phrase_plan_v2': str(ROOT/'letter_type_localization_DRAFT_v2.json'),
        'no_production_formatting_or_completion_credit': True}
    ledger['formatting_watchlist']['latest_research_reference_proof'] = str(ROOT/'user676_677_preserved.json')
    ledger['coverage_units'][0]['next'] = (
        'Finish Guild context/branch arguments and all nominal letter-name getter consumers/crops/write closure; '
        'implement the V785 six-name proposal, verify production layouts/copies, register combined ROM/exact patch '
        'and test actual item/diplomatic scenes for1070-1145. Continue1146 onward,resolve750-752,all routes/remaining prose; '
        'preserve graphics audit and older-record follow-up.')
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    assert latest['sha256'] == sha(CURRENT.read_bytes()) and latest['profile'] == 'all-routes-unified-v783'
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    for name in ('docs/known_issues.md', 'docs/todo.md'):
        path = Path(name)
        heading = '## V785: item and diplomacy runtime research'
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+
                ' See [V785 research](item_diplomacy_runtime_v785_research.md).\n', encoding='utf-8')

    proofs = {str(p): sha(p.read_bytes()) for p in ROOT.glob('*.json')
              if p.name not in ('checkpoint.json', 'archive_receipt.json')}
    save(ROOT/'checkpoint.json', {'id': 'V785-item-diplomacy-runtime-research',
        'documentation': str(DOC), 'current_candidate': latest,
        'research_ARM9_sha256': plan['research_ARM9_sha256'], 'proofs': proofs,
        'protected_files_unchanged': protected, 'summary': SUMMARY,
        'completed_records': 417, 'source_prose_reviews': 496, 'drafts': 79,
        'new_editorial_completion_credit': 0, 'new_playable_ROM_or_registered_patch': False,
        'all76_production_formatting_and_scene_approval_pending': True,
        'graphics_audit_separate_and_unfinished': True, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    copies = []
    producers = [Path(runtime.__file__), Path('scripts/verify_item_runtime_v785.py'),
        Path('scripts/audit_item_runtime_storage_v785.py'), Path('scripts/research_item_type_storage_v785.py'),
        Path(__file__), DOC, LEDGER]
    # The caller may redirect this process's stdout there. Do not archive a
    # log while this producer is still writing it.
    for src in [p for p in ROOT.rglob('*') if p.is_file() and p.name not in
                ('archive_receipt.json', 'checkpoint_run.log')]+producers:
        destination = ARCHIVE/src.relative_to(Path.cwd()) if src.is_absolute() else ARCHIVE/src
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)
        digest = sha(src.read_bytes())
        assert sha(destination.read_bytes()) == digest
        copies.append({'source': str(src), 'copy': str(destination), 'sha256': digest})
    receipt = {'archive': str(ARCHIVE), 'copies': copies, 'all_copies_SHA256_exact': True,
        'research_only_not_guide_or_playable_ROM': True}
    save(ROOT/'archive_receipt.json', receipt)
    save(ARCHIVE/'archive_receipt.json', receipt)
    print(f'V785 research recorded and archived: {len(copies)} exact copies. V783 remains current;417 complete/79 drafts;goal active.', flush=True)


if __name__ == '__main__':
    main()
