"""Register the follow-up favors, bounties, and ruin clues."""

from inspect import getsource
from pathlib import Path

from scripts import register_guild_search_and_survey_20261118 as publication
from scripts import register_port_favors_and_searches_20261118 as parent
from scripts import replay_followup_favors_20261118 as replay
from scripts import stage_followup_favor_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = stage.base, stage.native, publication.workflow
PROFILE = 'all-routes-followup-favors-v1-20261118'
ROOT = Path('out/followup_favors_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Followup_Favors_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_followup_favors_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_followup_favors_20261118.md')
QA, STARTUP = stage.ROOT / 'supported_qa.xml', stage.ROOT / 'own_startup_verification.json'
DECK = stage.ROOT / 'sailor_stat_preservation.json'
SHOWN = replay.scope['folder'](replay.CASE)
REWARD = SHOWN / 'capture' / 'frame_005725_cold_boot.png'
RETENTION_REASONS = {
    (0, 280, 13): "The contact names Plett and presses Rafael for an answer.",
    (0, 281, 72): "The recommendation, distance and conversational invitation remain intact. The stored wording already matches the planned layout.",
    (0, 284, 5): "Rafael's short report tells the guild that Peralonso has been brought in.",
    (1, 270, 13): "The contact identifies Plett after explaining the request, then asks for a commitment.",
    (1, 271, 12): "The short rebuke turns Plett's claim of remorse back on him.",
    (1, 271, 66): "The Forbidden City is worth visiting and some distance away. All three clauses already fit the exchange.",
    (1, 272, 25): "The guildmaster repeats the capture request with urgency.",
    (2, 270, 6): "The quick appeal to Lil's sympathy belongs before the woman's story.",
    (2, 270, 13): "The contact gives Plett's name and asks Lil whether she will help.",
    (2, 271, 67): "The familiar invitation to visit keeps the recommendation and the practical warning about distance.",
    (3, 239, 23): "The regional lead remains a rumor and keeps the epithet at the center of Yuris's objection.",
}


def replay_dependencies(final):
    fixture = base.load(SHOWN / 'fixture.json')
    assert fixture['reference_ROM_sha256'] == base.digest(stage.ROM)
    assert fixture['original_scene_commands_exact'] and fixture['whole_source_ROM_inverse']
    archive = '/data/SC3.DK4'
    bank = native.IlnkContainer.parse(final.read_file(archive))
    return {path: native.digest(final.read_file(path)) for path in (native.ARM, '/GRP/KANJI.FNT')} | {
        f'{archive}:B{block}': native.digest(bank.blocks[block]) for block in (33, 244)}


def verify_indices(records):
    changed = {}
    for row in records:
        source = row['source_reference']['record_index']
        stored = row['current_reference']['record_index']
        assert stored == row['staged_reference']['record_index']
        if source != stored:
            changed.setdefault((row['route'], row['block']), {})[source] = stored
    assert changed == stage.INDEX_MAP
    return [dict(route=r, block=b, clean_to_current_indices=m) for (r, b), m in changed.items()]


def verify_deck(candidate):
    receipt = base.load(DECK)
    assert receipt['candidate_sha256'] == candidate
    assert base.digest(receipt['earlier_gameplay_proof']) == receipt['earlier_gameplay_proof_sha256']
    assert receipt['identical_repair_word_count'] == 29 and len(receipt['identical_ARM9_ranges']) == 7
    assert not receipt['new_deck_gameplay'] and not receipt['hardware']
    return receipt


def verify_reward_frame(live):
    report = base.load(live['report'])
    row, = (item for item in report['frames_captured'] if item['frame'] == 5725)
    assert Path(row['path']) == REWARD
    assert base.digest(REWARD) == row['PNG_sha256'] == '815fc4def647ce9f6864e1a6cc26d0faf2701df0d6add6a3a8e271ab75f878c1'
    return row | {'observed_text': 'Received 72,000 coins.'}


def main():
    env = vars(publication) | globals()
    verifier = checked_text(getsource(publication.verify), {
        "live['candidate_sha256'] == base.digest(stage.prior.ROM)": "live['candidate_sha256'] == candidate",
        "len(records) == 206 and len(edited) == staged['preview_count'] == 42":
            "len(records) == 132 and len(edited) == staged['preview_count'] == 39",
        "len(stage.prior.BLOCKS)": "len(stage.BLOCKS)",
        "if r['source_selector'] != 254": "if r['source_selector'] < 207",
        "if key[:2] == (3, 226) and row['id'] in seen:": "if key[:2] == (3, 244) and row['id'] in seen:",
        "and initialized emulator on byte-identical scene": "and initialized emulator",
        "offline_only_Plett_turns=sorted(set(replay.SCENE_TURNS) - set(replay.TURNS)),":
            "source_current_index_map=verify_indices(records), sailor_stat_preservation=verify_deck(candidate), "
            "observed_reward=verify_reward_frame(live),",
    })
    exec(compile(verifier, __file__ + '::verify', 'exec'), env)
    source = getsource(publication.main)
    start = source.index('        out.write(f')
    end = source.index("''')", start) + len("''')")
    documentation = """        out.write(f'''# Follow-up favors and bounties

Reviewed 132 turns in 28 complete story blocks across all four routes. The ledger records {prose} wording revisions and {released['justified_retentions']} justified retentions. The revisions keep Julian's reported occupation tentative, leave Plett's fate to the woman who sought help, and preserve the distinctions between an advance and the final payment. The six relocated turns retain both Japanese and current command indices. [Exact review ledger](../{REVIEW.as_posix()})

All {staged['preview_count']} revised pages passed native checks and visual review. An initialized emulator replay covered Gabriel's handover, the 72,000-coin reward, the northern village clue and the return to the port menu. The other scenes received offline checks. Natural activation and physical hardware remain unverified. The exact candidate passed six cold-boot holds, 24 protected names and {tests} targeted repository tests. [Handover replay](../{(VERIFY / 'live_1.png').as_posix()}) [Reward frame](../{(VERIFY / REWARD.name).as_posix()})

The patch reconstructs the candidate byte for byte from clean input. It preserves all 114 accepted layers and the ASCII right-bound correction. Main retains its accepted build. The credited total stays at 27,700 with 276 pending shared keys. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The candidate's Sailor Info plaques, font, 29 ARM9 repair words and seven display ranges match the previously replayed Crew Review ROM byte for byte. This check reused the earlier Fernando gameplay evidence. The photographed title overlap still needs hardware confirmation on a known build. [Preservation receipt](../{(VERIFY / DECK.name).as_posix()})

The next 152 clean and current turns are staged under work/remaining_bounties_source_20261118 in SC0 B286–292, SC1 B274–280, SC2 B272–278 and SC3 B246–252.
''')"""
    changes = {
        source[start:end]: documentation,
        "len(manifest['batches']) == 857 and len(manifest['checks']) == 192": "len(manifest['batches']) == 859 and len(manifest['checks']) == 194",
        "    candidate = staged['candidate_sha256']":
            "    candidate = staged['candidate_sha256']\n"
            "    prose = sum(stage.precedent.normalize(r['english']) != r['previous_English'] for r in edited)",
        "for source in (stage.STORED, STARTUP, QA, SHOWN / 'verified.json'):":
            "for source in (stage.STORED, STARTUP, QA, DECK, REWARD, SHOWN / 'verified.json', SHOWN / 'fixture.json'):",
        "release_stack_before_guild_survey.json": "release_stack_before_followup_favors.json",
        "release_stack_with_guild_survey.json": "release_stack_with_followup_favors.json",
        "verified_ruin_statue_and_ice_predecessor=predecessor, guild_search_and_survey_release=str(REVIEW)":
            "verified_port_favors_and_searches_predecessor=predecessor, followup_favors_release=str(REVIEW)",
        "registered_guild_search_and_survey_and_complete_parent_inverse": "registered_followup_favors_and_complete_parent_inverse",
        "manifest['guild_search_and_survey_pipeline']": "manifest['followup_favors_pipeline']",
        "registered_manifest_entries=858, passing_release_checks=193": "registered_manifest_entries=860, passing_release_checks=195",
        "prose_revisions=len(edited), name_label_revisions=0, text_display_revisions=0":
            "prose_revisions=prose, name_label_revisions=0, text_display_revisions=len(edited)-prose",
        "initialized_Maria_Plett=True": "initialized_Maria_Gabriel_handover=True",
        "The survey parties and four guild searches are reviewed across all routes.":
            "The follow-up favors, bounties and ruin clues are reviewed across all routes.",
        "ledger['guild_search_and_survey_20261118']": "ledger['followup_favors_20261118']",
        "existing_credit=206, prose_revisions=len(edited)": "existing_credit=132, prose_revisions=prose, wrap_only_revisions=len(edited)-prose",
        "Guild searches and surveys test candidate": "Follow-up favors test candidate",
        "includes the survey and guild-search dialogue review": "includes the follow-up favors and bounty review",
        "for path in (ROM, stage.ROM, stage.prior.ROM, stage.ROOT.with_name('guild_search_and_survey_20261118_v2') / stage.ROM.name):":
            "for path in (ROM, stage.ROM, stage.prior.ROM):",
        "Preserve guild survey candidate": "Preserve follow-up favors candidate",
        "with 858 entries, 114 accepted layers and 193 passing checks.": "with 860 entries, 114 accepted layers and 195 passing checks.",
    }
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
