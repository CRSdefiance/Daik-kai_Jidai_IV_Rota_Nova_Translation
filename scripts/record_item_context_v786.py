"""Record tested type-provider research and actual old Guild context."""

import shutil
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_item_type_provider_v786 import ROOT, PRIOR, CURRENT
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.verify_item_guild_context_v786 import CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/item_diplomacy_context_v786_research.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V786 Item names and Guild context research')
SUMMARY = (
    'V786 tests six nominal English letter names through both original getters: '
    '20 complete pointer/text/8 MiB/ABI cases preserve older types6-9 and57 village/Deck replacements. '
    'Actual research getter output feeds2,774 native layouts and76 independent font planes; '
    'all seven sheets are visually reviewed. A normal8,400-frame V783 Guild visit proves '
    'role5/actor149 and one complete old1071 hold,then cancels to town with38816 coins '
    'and persistent objects unchanged.180 clean/current town NPC lookups and four original '
    'buy/sell fragments bind all four regional Guildmasters. Repaired676/677 and all3668 '
    'COMMON mappings remain exact. This is research,not new prose gameplay approval: '
    'virtual name consumers/crops,diplomacy branch eligibility,production dispatch/integration, '
    'registered ROM/patch and new scene samples remain. V783 stays current; '
    '417 complete,496 source/prose,79 drafts;full editorial and separate graphics goals unfinished.'
)


def main():
    provider = read(ROOT/'nominal_provider_research.json')
    guild = read(ROOT/'Guild_context_verification.json')
    layout_root = ROOT/'provider_layouts'
    layout = read(layout_root/'verification.json')
    matrix = read(layout_root/'native_layout_matrix.json')
    arm = (ROOT/'NOMINAL_PROVIDER_RESEARCH_ONLY.bin').read_bytes()
    previous = (PRIOR/'ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == layout['research_ARM9_sha256'] == provider['target_research_ARM9_sha256']
    assert layout['provider_proof_sha256'] == sha((ROOT/'nominal_provider_research.json').read_bytes())
    assert len(provider['native_getter_cases']) == 20
    assert len(guild['all180_original_source_current_town_Guild_lookup_cases']) == 180
    assert len(guild['four_original_buy_sell_lookup_and_speech_fragments']) == 4
    assert layout['complete_native_layouts'] == matrix['count'] == 2774 and not matrix['findings']
    assert len(layout['complete_font_planes']) == 76 and len(layout['preview_sheets']) == 7
    for row in layout['complete_font_planes']+layout['preview_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    visual = {'all76_full_font_planes_visually_reviewed_in_seven_sheets': True,
        'sheets': layout['preview_sheets'], 'complete_leading_trailing_characters_and_words': True,
        'left_margins_line_breaks_substitutions_and_bounds_reviewed': True,
        'dense1089_first_word_This_also_inspected_in_original228x64_plane': True,
        'supplied_same_faction_partner_enemy_pairs_and_maximum_numbers_are_not_eligibility_claims': True,
        'no_production_dispatch_actual_revised_prose_or_generic_UI_crop_approval': True}
    save(layout_root/'visual_review.json', visual)
    # Leave the producer's original visual_review_pending field historical;
    # this separately pinned visual receipt records the subsequent review.
    for proof, script in ((provider, 'scripts/prepare_item_type_provider_v786.py'),
                          (guild, 'scripts/verify_item_guild_context_v786.py'),
                          (layout, 'scripts/probe_item_provider_layout_v786.py')):
        assert proof['producer_sha256'] == sha(Path(script).read_bytes())
    old_spans = read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')['private_spans']
    old_spans += [read(PRIOR/'source_tail_ownership.json')['span']]
    for lo, hi in old_spans:
        assert arm[lo-0x02000000:hi-0x02000000] == previous[lo-0x02000000:hi-0x02000000]
    rom = NdsImage.open(CURRENT)
    common, original_arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    before, after = [common_message_entries(common, value, clean=False) for value in (original_arm, arm)]
    assert len(before) == len(after) == 3668
    for a, b in zip(before, after):
        assert (a.block, a.block_offset, a.copy_end, a.text) == (b.block, b.block_offset, b.copy_end, b.text)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))
    reference = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    earlier = []
    for row in reference['entries']:
        formatted, lines = native_layout(cpu, after[row['id']].text, row['id'], ())
        assert lines == row['lines'] and formatted.hex() == row['native_formatted_hex']
        earlier.append({'id': row['id'], 'lines': lines, 'native_formatted_hex': formatted.hex()})
    save(ROOT/'earlier_prose_preservation.json', {'all3668_COMMON_mappings_and_texts_exact': True,
        'all14_old_private_runtime_spans_and_BOOM_constant_exact_to_V785': True,
        'existing_native_selector_and_status_evidence_inherits_by_exact_code_and_data_identity': True,
        'repaired676_677': earlier, 'old_V747_actual_scene_reference_unchanged': True,
        'no_new_user_shop_scene_activation_claim': True})

    cfg = read('translations/shared_dialogue_editorial_release_v2.json')
    for name, expected in cfg['dependencies'].items():
        assert sha(Path(name).read_bytes()) == expected, name
    protected = dict(read(PRIOR/'checkpoint.json')['protected_files_unchanged'])
    for name, expected in protected.items():
        assert sha(Path(name).read_bytes()) == expected, name
    assert sha(CURRENT.read_bytes()) == guild['candidate_sha256'] == provider['source_ROM_sha256']

    DOC.write_text('''# V786: nominal letter names and actual Guild speaker context

## Current status

V783 remains the current registered experimental ROM and exact patch. No new ROM,
COMMON prose, release profile, canonical promotion or completed-entry credit is
produced here. Coverage stays **417 completed, 496 source/prose reviewed, 79 drafts**.
The 76-entry item/diplomacy batch remains unintegrated. The wider shared text,
every route, remaining prose and the separate graphics audit remain unfinished.

The previous goal turn made concrete progress on runtime ownership and routing.
This turn advances the real type provider, complete prototype fonts and an actual
Guild consumer. It does not turn a preview or an old-build scene into a new release approval.

## Native nominal-name prototype

An isolated ARM9 research input redirects the six original type-table fields
atomically and stores the complete six proposed English names in the source-bound
132-byte placement from V785. The names consume 110 bytes including NULs:
goodwill letter, pact proposal, pact termination notice, truce proposal,
declaration of war and demand for submission.

Research ARM9 SHA-256:
`44f4e07420034aad87d837bf9b5be4066ac5bdeec5f2dea2b8141d8e5be4f6c8`.
Its parent is the V785 research ARM9
`288bcbfa29e2cbc6df81326bade9f074c156148cf2c2749ccabc0c570bbba4bf`.
Five source allocations and six pointer fields are the only differences.
Restoring those eleven changes reproduces the complete parent byte for byte.

Twenty native cases execute both original getters for all ten types. They verify
complete pointers, NUL-terminated text, callee-saved ABI and unchanged entire
8 MiB memory during each getter. Types 6–9 remain Lure Fleet, Forge Papers,
Bad Rumors and Bribe. All 57 earlier village/Deck replacements, the C++ RTTI name,
old strategist code, adjacent bytes and memory geometry remain exact.
No function or generic renderer is changed by the nominal-name prototype.

This input is for native CPU research. Complete generic/virtual name consumers,
write exclusions, display crops and production approval are still open. The
current playable V783 getters still return Japanese for types 0–5.

## Current prototype layouts and visual review

The six argument strings are read from the research getter itself. They feed
2,774 original printf/existing paragraph-formatter cases and 76 independent full
font planes. All seven sheets are visually reviewed, including complete first and
last letters, substitutions, margins and bounds. The dense first word `This` in
1089 was also inspected in its original 228×64 plane. No findings remain.

The source V784 manuscript and layout producer are unchanged. A separate adapter
records its exact substitutions and effective program. Some supplied cross-product
faction pairs and maximum-size amounts are deliberately stress inputs; they are
not claims that those selections or funds can be earned. These tests invoke the
existing formatter directly. They do not approve all original caller branches,
the proposed production dispatcher or actual new prose/letter-name gameplay.

## Actual unmodified V783 Guild visit

A normal 8,400-frame cold boot uses an isolated byte-exact copy of the unchanged
Maria Seoul cartridge save. It uses controller/stylus inputs, no savestate,
cheats, inventory/location/quest/relationship fixtures or dialogue injection.
The original harness and emulator DLL hashes are checked. Both capture processes
are terminal; no background emulator process is being left running.

The first navigation probe entered the Square and triggered a Maria scene; it
is retained as discovery evidence and receives no Guild credit. In the final run,
a Palace popup was cancelled before selecting the real Guild compass icon at
bottom-screen (20,145). The recorded final schedule is authoritative; the initial
plan alone does not describe the whole interactive run.

At 5,600, the actual Guildmaster is visible and the captured building-role field
is 5. At 7,200, the existing COMMON1071 `Which item?` is bound to its exact complete
resident block, owner template, printf buffer and independent full glyph mask.
Its leading presentation space is preserved. At 7,600, the normal Items list
appears. Cancelling returns to town at 8,400. Native financial getters remain
38,816 coins, with unchanged share, investment and growth values. Company,
fleet, ships and complete persistent actor/town/item/goods objects remain exact.
The initial full screen and all 4 MiB RAM equal the earlier V783 3,200-frame control.

This verifies the **old** V783 consumer and its context. It does not show the
revised `Which one would you like?` wording or any new nominal letter name.

## Clean-source Guild NPC and caller mapping

The original 21 tagged culture rows and lookup instructions are unchanged.
Across all 90 town objects, 180 clean-Japanese/current native lookup cases resolve
the four regional Guildmaster actors 147–150. Clean names are ギルドの元締め;
the established English is Guildmaster. This checks the lookup for every town
object, not the availability of a Guild in every town or actual travel there.

The real Seoul context resolves actor 149. Four original clean/current buy/sell
prefix/speech fragments obtain the town and role through the native functions
and reach COMMON1071 or1085 with that actor. No guessed NPC sentinel, replacement
provider or role override is used. Sell is a native fragment test; the actual
capture exercises Buy Items only. Full Guild diplomacy eligibility, its entry
setter/control branches and nominal-name virtual display consumers remain open.

## Earlier repairs and remaining work

All 3,668 current COMMON mappings, complete texts and copy extents stay exact.
All 14 earlier private runtime spans and the moved economic-boom constant match
V785, so their existing routing/status tests inherit by exact code/data identity.
The user's repaired COMMON676/677 also reproduce their exact native wrapping.
V747 remains their actual shop-scene framebuffer reference.

Next: close the generic/virtual scheme-name display paths, Guild diplomacy branch
and argument eligibility, then prove production dispatch and copies. Integrate
the full 76 paragraphs through natural-dialogue-v2 and the registered full stack,
produce an exact clean-input patch and test representative actual buy/sell/bargain
and diplomatic scenes plus ordinary startup. Continue1146 onward,resolve750–752,
all routes and other prose. Revisit older record checks when the whole goal completes.

The original 18 plaques remain open in the separate graphics audit; the Online
body exclusion, preserved brown marks and Rafael/Joakim/Maria/Camille decisions
remain unchanged. No guide screenshot is promoted from these research captures.
No commit or GitHub push is made.

## Evidence

Native and preview evidence: `work/analysis/item_diplomacy_context_v786`.
Actual captures: `E:/Rota Nova translations/Generated/work/emulation_v193/item_guild_v786`.
Archive: `E:/Rota Nova translations/Editorial review/V786 Item names and Guild context research`.
Reproduce with prepare_item_type_provider_v786.py,
probe_item_provider_layout_v786.py, verify_item_guild_context_v786.py and
record_item_context_v786.py under scripts. Actual capture reproduction uses the
terminal report's complete input schedule and the pinned original save.
''', encoding='utf-8')

    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 417 and ledger['records_with_source_and_prose_pass'] == 496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs']) == 79
    if not (ROOT/'editorial_ledger_before_v786.json').exists():
        save(ROOT/'editorial_ledger_before_v786.json', ledger)
    ledger['latest_checkpoint'] = SUMMARY
    ledger['latest_item_type_and_Guild_context_research'] = {
        'documentation': str(DOC), 'provider': str(ROOT/'nominal_provider_research.json'),
        'layouts': str(layout_root/'verification.json'), 'visual_review': str(layout_root/'visual_review.json'),
        'actual_old_Guild_context': str(ROOT/'Guild_context_verification.json'),
        'new_editorial_completion_credit': 0, 'all76_production_formatting_approval_pending': True}
    ledger['formatting_watchlist']['latest_research_reference_proof'] = str(ROOT/'earlier_prose_preservation.json')
    ledger['coverage_units'][0]['next'] = (
        'Close generic/virtual scheme-name consumers/crops and write exclusions;Guild diplomacy eligibility/arguments; '
        'production dispatch and COMMON copies;register combined76-entry ROM/exact patch and actual buy/sell/bargain/diplomacy '
        'plus startup. Native Guild NPC mapping and old1071 actual context are now source-bound. '
        'Then1146 onward,750-752,all routes/remaining prose;graphics audit and older-record follow-up stay open.')
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    assert latest['sha256'] == sha(CURRENT.read_bytes()) and latest['profile'] == 'all-routes-unified-v783'
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    for name in ('docs/known_issues.md', 'docs/todo.md', 'docs/translation_progress.md', 'docs/editorial_review_goal.md'):
        path = Path(name)
        text = path.read_text(encoding='utf-8')
        heading = '## V786: nominal letter names and actual Guild context'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+
                ' See [V786 research](item_diplomacy_context_v786_research.md).\n', encoding='utf-8')

    proofs = {str(p): sha(p.read_bytes()) for p in ROOT.rglob('*.json')
              if p.name not in ('checkpoint.json', 'archive_receipt.json')}
    save(ROOT/'checkpoint.json', {'id': 'V786-item-types-and-actual-Guild-context-research',
        'documentation': str(DOC), 'current_candidate': latest,
        'research_ARM9_sha256': sha(arm), 'proofs': proofs, 'protected_files_unchanged': protected,
        'previous_goal_turn_classification': 'progress:V785 runtime/source-storage evidence changed the next available action',
        'this_turn_classification': 'progress:native type provider,new layouts and actual Guild context evidence',
        'completed_records': 417, 'source_prose_reviews': 496, 'drafts': 79,
        'new_editorial_completion_credit': 0, 'new_playable_ROM_or_registered_patch': False,
        'full_goal_complete': False, 'graphics_audit_separate_and_unfinished': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'summary': SUMMARY})
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    producers = [Path('scripts/prepare_item_type_provider_v786.py'), Path('scripts/probe_item_provider_layout_v786.py'),
        Path('scripts/verify_item_guild_context_v786.py'), Path(__file__), DOC, LEDGER]
    sources = [p for p in ROOT.rglob('*') if p.is_file() and p.name not in ('archive_receipt.json', 'checkpoint_run.log')]
    sources += [p for p in CAP.rglob('*') if p.is_file() and 'saves' not in p.parts]
    probe = CAP.parent/'item_context_v786'
    sources += [p for p in probe.rglob('*') if p.is_file() and 'saves' not in p.parts]
    copies = []
    for src in sources+producers:
        if src.is_relative_to(CAP.parent):
            destination = ARCHIVE/'captures'/src.relative_to(CAP.parent)
        elif src.is_absolute():
            destination = ARCHIVE/src.relative_to(Path.cwd())
        else:
            destination = ARCHIVE/src
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)
        digest = sha(src.read_bytes())
        assert sha(destination.read_bytes()) == digest
        copies.append({'source': str(src), 'copy': str(destination), 'sha256': digest})
    receipt = {'archive': str(ARCHIVE), 'copies': copies, 'all_copies_SHA256_exact': True,
        'research_only_no_guide_or_new_ROM': True}
    save(ROOT/'archive_receipt.json', receipt)
    save(ARCHIVE/'archive_receipt.json', receipt)
    print(f'V786 recorded,progress updated and{len(copies)} artifacts archived. V783 current;417 completed/79 drafts;goal active.', flush=True)


if __name__ == '__main__':
    main()
