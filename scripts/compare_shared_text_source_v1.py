"""Bind source-first shared drafts and individual findings to the registered Lil261 bytes."""

import json
import struct
from collections import Counter
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_shared_text_source_v1 import reference


ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
RELEASE = Path('work/lil261_B323_B335_release_v1/registered_release_verification.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
DIRECTORY = '80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e'
FINDINGS = [
    [
        85,
        "retention-candidate",
        "The short range estimate is natural within a labeled sailing-range display. Its consumer must confirm that the surrounding label supplies the future-sailing context."
    ],
    [
        86,
        "retention-candidate",
        "The English preserves all four values and the departure verb. The date and status line structure follows distinct source display fields. Check exact caller arguments and indentation."
    ],
    [
        87,
        "revision-candidate",
        "Missing states absence. The Japanese reports insufficient quantity. Use Not enough with the same substitution."
    ],
    [
        88,
        "retention-candidate",
        "A concise, emphatic fleet-destruction notice preserves the result and reads naturally."
    ],
    [
        89,
        "retention-candidate",
        "The current sentence preserves retreat and its emphasis, with a natural short notice."
    ],
    [
        90,
        "retention-candidate",
        "The town is the defeated target and the ellipsis preserves the subdued tone. Confirm city versus town terminology at the consumer."
    ],
    [
        91,
        "retention-candidate",
        "The current short surrender notice preserves the result and ellipsis. Trailing spaces and the forced final line require display review."
    ],
    [
        92,
        "retention-candidate",
        "The existing financial-report offer is natural and preserves the subordinate fleets and permission to read the reports. Japanese leaves number implicit, so the caller must decide whether plural reports is appropriate."
    ],
    [
        93,
        "revision-candidate",
        "Opened fire adds an onset to the continuing bombardment. The proposed is firing on preserves the source action and both arguments."
    ],
    [
        94,
        "revision-candidate",
        "The current two fragments do not state who attacks whom. The proposed full sentence names the place first and the attacking pirate second, preserving native argument order."
    ],
    [
        95,
        "revision-candidate",
        "The source opening I is full-width in the current English. Replace it with an ASCII I and retain the trade, commodity and market-share facts. Keep sold large amounts if the consumer concerns aggregate sales."
    ],
    [
        96,
        "revision-candidate",
        "The current possessive can identify either a place or a faction. The clean notice is about a falling market share. Bind its argument and ownership before choosing in the place or the faction's share."
    ],
    [
        98,
        "retention-candidate",
        "The existing natural empty-list notice preserves absence of acquired items. Adding yet is optional and does not justify a revision by itself."
    ],
    [
        99,
        "retention-candidate",
        "The existing natural empty-discovery notice preserves the source. Adding yet is optional."
    ],
    [
        100,
        "retention-candidate",
        "Choose three skills you excel at is natural, exact in number and appropriate to selecting strengths."
    ],
    [
        101,
        "revision-candidate",
        "The bare list and Okay fragment are stilted. A full confirmation question makes the selected three skills clear without changing the substitutions."
    ],
    [
        102,
        "revision-candidate",
        "BGM is an internal abbreviation for background music. Music and sound effects reads naturally. Remove the early authored line break through the correct consumer formatter."
    ],
    [
        103,
        "retention-candidate",
        "The existing short setup prompt is fluent and accurately asks for the birthday."
    ],
    [
        104,
        "source-mismatch",
        "The clean source is Rafael's Portuguese-boy introduction. The current square-gathering line has unrelated content. Classify the active captain-chooser text source and this legacy COMMON entry before revising storage."
    ],
    [
        105,
        "source-mismatch",
        "The clean source introduces Hodram and Sweden's privateer fleet. The current square-gathering line is unrelated. The active captain description may be supplied elsewhere."
    ],
    [
        106,
        "source-mismatch",
        "The clean source introduces Lil and her childhood friend Camille. The current square-gathering line is unrelated. Bind the active description source before treating the COMMON entry as visible."
    ],
    [
        107,
        "source-mismatch",
        "The clean source introduces Maria, Ming isolation policy and anti-pirate protection. The current save-failure notice is unrelated. Confirm the DS description consumer."
    ],
    [
        108,
        "revision-candidate",
        "Game saves need is understandable but telegraphic. The proposed save warning keeps four blocks, the current inability to save and the choice to continue. Check whether this platform-specific text is reached on DS."
    ],
    [
        109,
        "retention-candidate",
        "The existing message preserves one free block, system data and the start-anyway choice in natural English. Platform reachability remains pending."
    ],
    [
        110,
        "retention-candidate",
        "The existing natural warning preserves the five-block requirement and start-anyway choice. Platform reachability remains pending."
    ],
    [
        111,
        "retention-candidate",
        "The existing sentence is exact and natural for absent game data. It does not confuse missing and corrupted data."
    ],
    [
        112,
        "retention-candidate",
        "System data not found is natural and accurate. Its trailing line and padding need consumer-specific formatting review."
    ],
    [
        113,
        "source-mismatch",
        "The clean source requires four free blocks for game data. The current line instead asks to start anyway. Restore the correct branch meaning only after confirming its active consumer."
    ],
    [
        114,
        "source-mismatch",
        "The clean source requires one free block for system data. The current line replaces that with an unrelated start-anyway question."
    ],
    [
        115,
        "retention-candidate",
        "The two short sentences accurately convey insufficient blocks and the five-block save requirement. Keep the current wording if its platform branch is used."
    ],
    [
        116,
        "retention-candidate",
        "The current instruction accurately names the memory card and controller and forbids insertion or removal during checking. Preserve those source facts while classifying platform use."
    ],
    [
        117,
        "revision-candidate",
        "Game data corrupt is a compressed fragment with an early break. The game data is corrupted is a natural complete notice. Check its consumer before formatting."
    ],
    [
        118,
        "retention-candidate",
        "System data is corrupted is concise, grammatical and accurate."
    ],
    [
        119,
        "revision-candidate",
        "Save ending? To memory card? splits one decision into two unnatural fragments. The proposed question preserves ending data and the destination."
    ],
    [
        120,
        "retention-candidate",
        "Everything correct? is a natural concise confirmation in a setup UI. Keep the short question if its scope is clear."
    ],
    [
        121,
        "source-mismatch",
        "The start confirmation is truncated into The game cannot save. Its stored selection ends before the rest of an unrelated save warning."
    ],
    [
        122,
        "source-mismatch",
        "The original system-load failure and initialization notice begins in the middle of the current save warning with here. Start anyway? Exact native message boundaries reveal a split sentence and lost source meaning."
    ],
    [
        123,
        "retention-candidate",
        "System data failed to load is understandable and accurate. Could not load reads more naturally, but that preference alone does not justify changing a working short status notice."
    ],
    [
        124,
        "retention-candidate",
        "The current line naturally states that formatting is available at save time and asks whether to start. Initialization and formatting correspond in this memory-card context, subject to platform classification."
    ],
    [
        125,
        "retention-candidate",
        "The existing complete sentence naturally preserves the substantial commercial investment and resulting economic recovery."
    ],
    [
        126,
        "retention-candidate",
        "The existing notice naturally distinguishes an economic boom from the preceding recovery notice and retains the same cause."
    ],
    [
        127,
        "retention-candidate",
        "Choose a base city is a clear concise command. City terminology is established here and should stay consistent."
    ],
    [
        128,
        "retention-candidate",
        "The current refusal is fluent and preserves the missing contract and the selected city."
    ],
    [
        129,
        "retention-candidate",
        "The two short sentences make the patrol target and contract requirement clear. The independent draft adds no essential meaning."
    ],
    [
        130,
        "revision-candidate",
        "Under contract can sound as though the fleet is under contract. Clarify that the selected city must have a contract, while preserving the fleet's port-call order."
    ],
    [
        131,
        "retention-candidate",
        "The short current attack-target command is exact and natural. Keep city terminology."
    ],
    [
        132,
        "retention-candidate",
        "The current sentence is fluent and accurately distinguishes an existing contract from the missing-contract refusal."
    ],
    [
        133,
        "retention-candidate",
        "The current sentence explicitly makes the contracted faction one that is not at war with the player. It preserves the negative condition."
    ],
    [
        134,
        "retention-candidate",
        "The current sentence accurately states the absence of a contract with an enemy faction and is natural in the city-selection context."
    ],
    [
        135,
        "revision-candidate",
        "Entry is unsafe softens the source refusal that entry is not possible and may omit the exit sense of 出入り. Bind whether the caller handles entering only or both directions before final wording."
    ],
    [
        136,
        "revision-candidate",
        "Hear market news is narrower than the source trends and other information and drops the shop-sign instruction. Restore that tutorial meaning and remove the premature two-line fragments."
    ],
    [
        750,
        "revision-candidate",
        "The current Start over? drops the speaker's confirmation emphasis and casual question. Its precise referent still needs a caller."
    ],
    [
        751,
        "revision-candidate",
        "A pain is a stiff isolated reaction. What a bother is an idiomatic put-upon response. Confirm the branch and speaker before approving."
    ],
    [
        752,
        "revision-candidate",
        "Don't waste my time is harsher and omits the request to stop joking. Preserve the busy speaker's brusque request with the source joke reference."
    ]
]


def main():
    output = ROOT / 'contextual_comparison_pending_consumers.json'
    assert not output.exists()
    source_path = ROOT / 'clean_source_packet.json'
    source, release, ledger = map(load, (source_path, RELEASE, LEDGER))
    assert digest(source['drafts']) == source['drafts_sha256']
    assert digest(release['candidate']) == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    image = NdsImage.open(release['candidate'])
    arm, common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    rows = owned_entries(common, arm, DIRECTORY)
    drafts = {r['message_ID']: r for r in source['records']}
    assert len(FINDINGS) == len(drafts) == 54
    keys = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    comparisons = []
    for number, status, finding in FINDINGS:
        original = drafts[number]
        assert ('/COMMON/MESFILE.DK4', original['id']) not in keys
        current = rows[number]
        raw = current.text
        comparisons.append(dict(**original, current_reference=reference(current), current_hex=raw.hex(),
            current_English=raw.decode('cp932'), comparison_status=status, comparison_finding=finding,
            independent_draft_is_provisional_not_final_approved_English=True,
            review=dict(source=True, context=False, localization=False, naturalness=False, formatting=False),
            current_native_consumer_andreachability_pending=True))
    raw = source['raw_command']
    at = raw['offset']
    value = bytes.fromhex(raw['terminated_hex'])
    field = 0x1150B4
    assert arm[at:at+len(value)] == value
    assert struct.unpack_from('<I', arm, field)[0] == 0x02000000 + at
    assert [i for i in range(0, len(arm)-3, 4) if arm[i:i+4] == struct.pack('<I', 0x02000000+at)] == [field]
    raw = dict(raw, current_offset=at, current_terminated_hex=value.hex(), current_text=value[:-1].decode('cp932'),
        exact_static_pointer_fields=[field], current_table_window_offset=0x1150B0,
        current_table_window_hex=arm[0x1150B0:0x1150C4].hex(), proposed_English='Abandon Ship',
        direct_consumer_bounds_andrelocation_pending=True, new_credit=0)
    censuses = [
        Path('work/story_source_coverage_20261109_SC0_v1/coverage.json'),
        Path('work/Hodram_source_coverage_20261109_v2/coverage.json'),
        Path('work/story_source_coverage_20261110_SC2_v8/coverage.json'),
        Path('work/story_source_coverage_20261110_SC3_v17/coverage.json'),
    ]
    census_records = []
    for path in censuses:
        data = load(path)
        assert not any(data[k] for k in ['missing', 'inventory_failures', 'legacy_source_bindings_not_exact'])
        assert all(r['covered'] for r in data['records'])
        census_records.append(dict(path=str(path), sha256=digest(path), native_objects=len(data['records']),
            missing=0, existing_source_inventory_reused=True))
    assert sum(r['native_objects'] for r in census_records) == 24092
    save(output, dict(source=str(source_path), source_sha256=digest(source_path),
        release=str(RELEASE), release_sha256=digest(RELEASE), candidate=release['candidate'],
        candidate_sha256=release['candidate_sha256'], ARM9_sha256=sha256(arm).hexdigest(),
        COMMON_sha256=sha256(common).hexdigest(), exact_COMMON_directory_sha256=DIRECTORY,
        immutable_loader_andcomplete_owned_directory_parser_pass=True,
        records=comparisons, counts=dict(Counter(r['comparison_status'] for r in comparisons)),
        raw_command=raw, all_four_native_story_censuses=census_records,
        current_source_mismatches_are_stored_content_findings_not_observed_gameplay=True,
        source_first_drafts_and_current_comparisons=54, completed_native_story_positions=24092,
        broader_COMMON_ARM9_names_items_player_facing_andretrospective_wrap_scope_remains_open=True,
        new_source_prose_credit=0, new_completion_credit=0, ROM_changed=False, full_goal_complete=False,
        evidence={str(p):digest(p) for p in [source_path, Path(source['drafts']), RELEASE, LEDGER, Path(__file__)]}))
    print('Bound 54 individual comparisons and the raw ship command to Lil261. Consumer and display gates remain.')


if __name__ == '__main__':
    main()
