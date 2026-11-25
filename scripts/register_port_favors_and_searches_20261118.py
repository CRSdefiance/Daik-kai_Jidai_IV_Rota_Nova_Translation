"""Register the source-bound port favors and guild searches."""

from inspect import getsource
from pathlib import Path

from scripts import register_guild_search_and_survey_20261118 as parent
from scripts import replay_port_favors_and_searches_20261118 as replay
from scripts import replay_rafael_courier_pagination_20261118 as pagination
from scripts import stage_port_favor_wraps_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
workflow = parent.workflow
PROFILE = 'all-routes-port-favors-and-searches-v1-20261118'
ROOT = Path('out/port_favors_and_searches_registered_20261118_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Port_Favors_and_Searches_20261118_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261118_port_favors_and_searches_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_port_favors_and_searches_20261118.md')
QA, STARTUP = stage.ROOT / 'supported_qa.xml', stage.ROOT / 'own_startup_verification.json'
SHOWN = replay.scope['folder'](replay.CASE)
PAGES = pagination.scope['folder'](pagination.CASE)
RETENTION_REASONS = {
    (3, 233, 13): 'The request identifies a Spanish spy and reports his operating area with uncertainty.',
    (3, 234, 21): 'Maria ignores his invitation and asks the barkeep for Peralonso by his approved name.',
}


def replay_dependencies(final):
    receipt = base.load(SHOWN / 'fixture.json')
    assert receipt['reference_ROM_sha256'] == base.digest(stage.ROM)
    assert receipt['original_scene_commands_exact'] and receipt['whole_source_ROM_inverse']
    archive = '/data/SC3.DK4'
    bank = native.IlnkContainer.parse(final.read_file(archive))
    return {path: native.digest(final.read_file(path)) for path in (native.ARM, '/GRP/KANJI.FNT')} | {
        f'{archive}:B{block}': native.digest(bank.blocks[block]) for block in (33, 234)}


def verify_index_map(records):
    observed = {}
    for row in records:
        source = row['source_reference']['record_index']
        current = row['current_reference']['record_index']
        assert row['staged_reference']['record_index'] == current
        if source != current:
            observed.setdefault((row['route'], row['block']), {})[source] = current
    assert observed == stage.prior.INDEX_MAP
    return [dict(route=r, block=b, source_to_current=m) for (r, b), m in observed.items()]


def verify_pagination(candidate):
    proof = base.load(PAGES / 'verified.json')
    fixture = base.load(PAGES / 'fixture.json')
    assert candidate == proof['candidate_sha256'] == fixture['reference_ROM_sha256']
    assert fixture['original_scene_commands_exact'] and fixture['whole_source_ROM_inverse']
    assert proof['initialized_emulator'] and not proof['natural_activation'] and not proof['hardware']
    assert [(row['turn'], row['page']) for row in proof['complete_holds']] == [(6, 1), (9, 1), (9, 2)]
    assert all(base.digest(path) == sha for path, sha in proof['evidence'].items())
    return proof


def preview_name(item):
    path = Path(item['path'])
    return 'rafael_pagination_' + path.name if path.parent == PAGES else path.name


def main():
    env = vars(parent) | globals()
    verify_source = checked_text(getsource(parent.verify), {
        "live['candidate_sha256'] == base.digest(stage.prior.ROM)": "live['candidate_sha256'] == candidate",
        "len(records) == 206 and len(edited) == staged['preview_count'] == 42":
            "len(records) == 135 and len(edited) == 32 and staged['preview_count'] == 33",
        "if r['source_selector'] != 254": "if r['source_selector'] < 207",
        "and initialized emulator on byte-identical scene": "and initialized emulator",
        "    sheets = list(staged['sheets']) + live['sheets']":
            "    pages = verify_pagination(candidate)\n"
            "    sheets = list(staged['sheets']) + live['sheets'] + pages['sheets']",
        "        if key[:2] == (3, 226) and row['id'] in seen:":
            "        if (key[:2] == (3, 234) and row['id'] in seen) or key in ((0, 277, 6), (0, 277, 9)):",
        "offline_only_Plett_turns=sorted(set(replay.SCENE_TURNS) - set(replay.TURNS)),":
            "source_current_index_map=verify_index_map(records), initialized_rafael_pagination=pages,",
    })
    exec(compile(verify_source, __file__ + '::verify', 'exec'), env)
    source = getsource(parent.main)
    first = source.index('        out.write(f')
    last = source.index("''')", first) + len("''')")
    note = """        out.write(f'''# Port favors and guild searches

Reviewed 135 turns in 24 complete story blocks across all four routes. The ledger records {prose} wording revisions, {len(edited)-prose} wrap-only revisions and {released['justified_retentions']} justified retentions. Rafael's guild wants Julian brought in. Lil's guild wants his whereabouts. The revised exchanges also keep Gabriel's unpaid tab as a running joke and preserve Lil and Maria's different responses to Peralonso. Seven records in Hodram B266 and Maria B233 retain separate clean and current command indices. [Exact review ledger](../{REVIEW.as_posix()})

All 33 revised pages passed native layout checks and visual review. An initialized DeSmuME test confirmed that Rafael's description of Julian keeps the allegation about Spain on the first page and the report about courier work on the second. Another run covered Maria's original tavern meeting and resumed the host scene. Other scenes were checked offline. Natural activation and hardware remain unverified. Six cold-boot holds, 24 protected names and {tests} targeted tests passed. [Tavern replay](../{(VERIFY / 'live_1.png').as_posix()}) [Rafael pagination](../{(VERIFY / 'rafael_pagination_live_1.png').as_posix()})

The clean-input patch reconstructs the candidate byte for byte and preserves all 114 accepted layers. Main retains its accepted build. The credited total stays at 27,700 with 276 pending shared keys. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)

The next 132 clean and current story turns are staged under work/followup_favors_source_20261118. They cover SC0 B279–285, SC1 B267–273, SC2 B265–271 and SC3 B239–245.
''')"""
    changes = {
        source[first:last]: note,
        "len(manifest['batches']) == 857 and len(manifest['checks']) == 192": "len(manifest['batches']) == 858 and len(manifest['checks']) == 193",
        "    candidate = staged['candidate_sha256']":
            "    candidate = staged['candidate_sha256']\n"
            "    prose = sum(stage.precedent.normalize(r['english']) != r['previous_English'] for r in edited)",
        "        name = Path(item['path']).name": "        name = preview_name(item)",
        "    base.save(REVIEW, draft)":
            "    for proof_path, package_name in ((SHOWN / 'fixture.json', 'maria_fixture.json'),\n"
            "            (PAGES / 'fixture.json', 'rafael_pagination_fixture.json'),\n"
            "            (PAGES / 'verified.json', 'rafael_pagination_verified.json')):\n"
            "        copyfile(proof_path, VERIFY / package_name)\n"
            "        assert base.digest(proof_path) == base.digest(VERIFY / package_name)\n"
            "    base.save(REVIEW, draft)",
        "release_stack_before_guild_survey.json": "release_stack_before_port_favors.json",
        "release_stack_with_guild_survey.json": "release_stack_with_port_favors.json",
        "verified_ruin_statue_and_ice_predecessor=predecessor, guild_search_and_survey_release=str(REVIEW)":
            "verified_guild_search_and_survey_predecessor=predecessor, port_favors_and_searches_release=str(REVIEW)",
        "registered_guild_search_and_survey_and_complete_parent_inverse": "registered_port_favors_and_searches_and_complete_parent_inverse",
        "manifest['guild_search_and_survey_pipeline']": "manifest['port_favors_and_searches_pipeline']",
        "registered_manifest_entries=858, passing_release_checks=193": "registered_manifest_entries=859, passing_release_checks=194",
        "prose_revisions=len(edited), name_label_revisions=0, text_display_revisions=0":
            "prose_revisions=prose, name_label_revisions=0, text_display_revisions=len(edited)-prose",
        "initialized_Maria_Plett=True": "initialized_Maria_Peralonso=True, initialized_Rafael_pagination=True",
        "The survey parties and four guild searches are reviewed across all routes.":
            "The port favors and related guild searches are reviewed across all routes.",
        "ledger['guild_search_and_survey_20261118']": "ledger['port_favors_and_searches_20261118']",
        "existing_credit=206, prose_revisions=len(edited)": "existing_credit=135, prose_revisions=prose, wrap_only_revisions=len(edited)-prose",
        "Guild searches and surveys test candidate": "Port favors and searches test candidate",
        "includes the survey and guild-search dialogue review": "includes the port favors and guild-search dialogue review",
        "for path in (ROM, stage.ROM, stage.prior.ROM, stage.ROOT.with_name('guild_search_and_survey_20261118_v2') / stage.ROM.name):":
            "for path in (ROM, stage.ROM, stage.prior.ROM):",
        "Preserve guild survey candidate": "Preserve port favors candidate",
        "with 858 entries, 114 accepted layers and 193 passing checks.": "with 859 entries, 114 accepted layers and 194 passing checks.",
    }
    exec(compile(checked_text(source, changes), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
