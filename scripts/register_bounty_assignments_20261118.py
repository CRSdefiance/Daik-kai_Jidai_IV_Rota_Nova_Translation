"""Register the bounty dialogue and its focused pagination replay."""

from inspect import getsource
from pathlib import Path

from scripts import register_guild_search_and_survey_20261118 as publication
from scripts import register_followup_favors_20261118 as parent
from scripts import replay_bounty_assignments_20261118 as replay
from scripts import stage_bounty_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = stage.base, stage.native, publication.workflow
PROFILE = 'all-routes-bounty-assignments-v1-20261118'
ROOT = Path('out/bounty_assignments_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Bounty_Assignments_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_bounty_assignments_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_bounty_assignments_20261118.md')
QA, STARTUP = stage.ROOT / 'supported_qa.xml', stage.ROOT / 'own_startup_verification.json'
SHOWN = replay.scope['folder'](replay.CASE)
FOREST = Path('work/forest_expeditions_source_20261118/index.json')
RETENTION_REASONS = {
    (1, 279, 15): "The Mediterranean lead is a report. The guildmaster's confidence and the advance complete the request.",
    (1, 280, 58): "The question shifts naturally from the reward to the town's recognizable landmark.",
    (1, 280, 65): "The guildmaster recommends a visit and explains the landmark's significance in colloquial speech.",
    (2, 275, 25): "The guildmaster presses Lil for news of Jacob in the same familiar tone as the request.",
    (3, 249, 14): "The maritime location remains qualified by what the guildmaster has heard. Keep the advance separate.",
    (3, 250, 58): "The guildmaster remembers to ask about the landmark after handing over the reward.",
}


def replay_dependencies(final):
    fixture = base.load(SHOWN / 'fixture.json')
    assert fixture['reference_ROM_sha256'] == base.digest(stage.ROM)
    assert fixture['original_scene_commands_exact'] and fixture['whole_source_ROM_inverse']
    archive = '/data/SC3.DK4'
    bank = native.IlnkContainer.parse(final.read_file(archive))
    return {path: native.digest(final.read_file(path)) for path in (native.ARM, '/GRP/KANJI.FNT')} | {
        f'{archive}:B{block}': native.digest(bank.blocks[block]) for block in (33, 247)}


def verify_indices(records):
    observed = {}
    for row in records:
        source = row['source_reference']['record_index']
        current = row['current_reference']['record_index']
        assert current == row['staged_reference']['record_index']
        if source != current:
            observed.setdefault((row['route'], row['block']), {})[source] = current
    assert observed == stage.INDEX_MAP
    return [dict(route=r, block=b, clean_to_current_indices=m) for (r, b), m in observed.items()]


def verify_forest():
    saved = base.load(FOREST)
    assert saved['record_count'] == 370 and saved['full_contextual_pass_pending']
    assert saved['candidate_sha256'] == base.digest(stage.ROM)
    assert len(saved['route_packets']) == 4
    old, final = [base.NdsImage.open(p) for p in (parent.ROM, stage.ROM)]
    for group in saved['route_packets']:
        assert base.digest(group['exact_packet']) == group['packet_sha256']
        before, after = [native.IlnkContainer.parse(rom.read_file(group['file_path'])).blocks[group['block']]
                         for rom in (old, final)]
        assert before == after and native.digest(after) == group['current_sha256']
    return dict(paired_index=str(FOREST), paired_index_sha256=base.digest(FOREST), rows=370)


def main():
    env = vars(publication) | globals()
    verification = checked_text(getsource(publication.verify), {
        "live['candidate_sha256'] == base.digest(stage.prior.ROM)": "live['candidate_sha256'] == candidate",
        "tuple(r['turn'] for r in live['complete_holds']) == replay.TURNS":
            "[(r['turn'], r['page']) for r in live['complete_holds']] == "
            "[(4, 1), (8, 1), (11, 1), (15, 1), (60, 1), (60, 2), (63, 1), (66, 1)]",
        "len(records) == 206 and len(edited) == staged['preview_count'] == 42":
            "len(records) == 138 and len(edited) == 39 and staged['preview_count'] == 41",
        "if r['source_selector'] != 254": "if r['source_selector'] < 207",
        "if key[:2] == (3, 226) and row['id'] in seen:": "if key[:2] == (3, 247) and row['id'] in seen:",
        "and initialized emulator on byte-identical scene": "and initialized emulator",
        "offline_only_Plett_turns=sorted(set(replay.SCENE_TURNS) - set(replay.TURNS)),":
            "source_current_index_map=verify_indices(records), next_forest_exchanges=verify_forest(),",
    })
    exec(compile(verification, __file__ + '::verify', 'exec'), env)
    source = getsource(publication.main)
    start = source.index('        out.write(f')
    end = source.index("''')", start) + len("''')")
    note = """        out.write(f'''# Bounty assignments and handovers

Reviewed 138 turns in 27 complete guild exchanges across all four routes. The ledger records {prose} wording revisions and {released['justified_retentions']} justified retentions. The revised dialogue preserves Clive's strange cry and the guildmaster's warning, Zaganos's resignation, Jean's excuses, and the captains' distinct reactions to Hernan. The map remains an illustrated clue whose whereabouts are unknown. Eight speeches retain both clean and current command indices. [Exact review ledger](../{REVIEW.as_posix()})

All 41 revised pages passed native checks and visual review. An initialized emulator replay covered Maria's original Clive handover, the 100,000-coin reward, the Veracruz share increase, both pages of the map clue and the port's resupply prompt. The other scenes received offline checks. Natural activation and physical hardware remain unverified. The candidate passed six cold-boot holds, 24 protected name outputs and {tests} targeted tests. [Handover replay](../{(VERIFY / 'live_1.png').as_posix()}) [Map continuation](../{(VERIFY / 'live_2.png').as_posix()})

The clean-input patch reconstructs the exact ROM and preserves all 114 accepted layers and the ASCII right-bound correction. Main retains its accepted build. The credited total stays at 27,700 with 276 pending shared keys. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The next review covers the complete forest expeditions in SC0 B293, SC1 B290, SC2 B283 and SC3 B252. All 370 dialogue bodies, choices and FE notices are bound to exact clean and current bytes in work/forest_expeditions_source_20261118/index.json. The forest blocks are byte-identical to the preceding candidate. The packet uses the current version of Hodram's bear warning.
''')"""
    changes = {
        source[start:end]: note,
        "len(manifest['batches']) == 857 and len(manifest['checks']) == 192": "len(manifest['batches']) == 860 and len(manifest['checks']) == 195",
        "    candidate = staged['candidate_sha256']":
            "    candidate = staged['candidate_sha256']\n"
            "    prose = sum(stage.precedent.normalize(r['english']) != r['previous_English'] for r in edited)",
        "for source in (stage.STORED, STARTUP, QA, SHOWN / 'verified.json'):":
            "for source in (stage.STORED, STARTUP, QA, SHOWN / 'verified.json', SHOWN / 'fixture.json'):",
        "release_stack_before_guild_survey.json": "release_stack_before_bounty_assignments.json",
        "release_stack_with_guild_survey.json": "release_stack_with_bounty_assignments.json",
        "verified_ruin_statue_and_ice_predecessor=predecessor, guild_search_and_survey_release=str(REVIEW)":
            "verified_followup_favors_predecessor=predecessor, bounty_assignments_release=str(REVIEW)",
        "registered_guild_search_and_survey_and_complete_parent_inverse": "registered_bounty_assignments_and_complete_parent_inverse",
        "manifest['guild_search_and_survey_pipeline']": "manifest['bounty_assignments_pipeline']",
        "registered_manifest_entries=858, passing_release_checks=193": "registered_manifest_entries=861, passing_release_checks=196",
        "prose_revisions=len(edited), name_label_revisions=0, text_display_revisions=0":
            "prose_revisions=prose, name_label_revisions=0, text_display_revisions=len(edited)-prose",
        "initialized_Maria_Plett=True": "initialized_Maria_Clive_map=True",
        "The survey parties and four guild searches are reviewed across all routes.":
            "The bounty assignments and related handovers are reviewed across all routes.",
        "ledger['guild_search_and_survey_20261118']": "ledger['bounty_assignments_20261118']",
        "existing_credit=206, prose_revisions=len(edited)": "existing_credit=138, prose_revisions=prose, wrap_only_revisions=len(edited)-prose",
        "Guild searches and surveys test candidate": "Bounty assignments test candidate",
        "includes the survey and guild-search dialogue review": "includes the bounty assignments and handovers",
        "for path in (ROM, stage.ROM, stage.prior.ROM, stage.ROOT.with_name('guild_search_and_survey_20261118_v2') / stage.ROM.name):":
            "for path in (ROM, stage.ROM, stage.prior.ROM):",
        "Preserve guild survey candidate": "Preserve bounty assignments candidate",
        "with 858 entries, 114 accepted layers and 193 passing checks.": "with 861 entries, 114 accepted layers and 196 passing checks.",
    }
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
