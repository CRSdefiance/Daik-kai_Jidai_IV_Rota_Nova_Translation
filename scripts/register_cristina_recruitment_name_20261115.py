"""Register the exact story-only spelling fix and reconstructed cumulative ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_ritual_officiant_labels_20261115 as predecessor
from scripts import replay_cristina_recruitment_name_20261115 as live
from scripts import stage_cristina_recruitment_name_20261115 as stage
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-cristina-recruitment-name-v1-20261115'
ROOT = Path('out/cristina_recruitment_name_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Cristina_Recruitment_Name_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_cristina_recruitment_name_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
QA = stage.ROOT / 'repository_qa_supported.xml'
DOC = Path('docs/editorial_cristina_recruitment_name_20261115.md')
CHECK = 'registered_cristina_recruitment_spelling_and_complete_parent_inverse'
HISTORICAL = Path('translations/lil_B122_B127_contextual_final_review_v1.json')
FOLLOWUP = Path('releases/all_routes_editorial_20261114_lil_midroute_wraps_candidate/verification/registered_review.json')
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds')


def verify(prior, guard, viewed):
    staged, startup, game = map(base.load, (stage.STORED, live.STARTUP, live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == staged['candidate_sha256'] == startup['candidate_sha256'] == game['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (startup, game) for path, sha in proof['evidence'].items())
    assert game['matched_complete_corrected_dialogue'] and game['all_framebuffer_differences_inside_original_dialogue_body']
    assert base.digest(live.SHEET) == game['sheet_sha256'] == viewed
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests and all(int(suite.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped'))

    clean, old, new = [base.NdsImage.open(path) for path in (stage.CLEAN, parent.ROM, stage.ROM)]
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.FILE}
    planned, proof = stage.plan(clean, old, base.load(parent.MANIFEST))
    assert all(staged[key] == value for key, value in proof.items())
    blocks = IlnkContainer.parse(before[stage.FILE]).blocks
    revised = IlnkContainer.parse(after[stage.FILE]).blocks
    assert [n for n, (a, b) in enumerate(zip(blocks, revised, strict=True)) if a != b] == [stage.BLOCK]
    assert revised[stage.BLOCK] == planned
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.FILE, before[stage.FILE])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    ctx = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    actor = names.current_getters(ctx)['rows'][2*7:2*7+2]
    assert all(row['text'] == 'Cristina Erneco' and row['actor_ID'] == 7 for row in actor)
    source = {row['id']: row for row in base.load(HISTORICAL)['records'] if row['id'].startswith('DK4_MES_B123_')}
    later = next(row for row in base.load(FOLLOWUP)['records'] if row['id'] == 'DK4_MES_B123_R0020')
    historical = {str(path): base.digest(path) for path in (HISTORICAL, FOLLOWUP)}
    rows = []
    for n, item in enumerate(proof['all_eight_dialogue_records']):
        old_review = source[item['id']]
        assert old_review['source_hex'] == item['source']['raw_hex'] and all(old_review['review'].values())
        expected = old_review['compiled_hex']
        approved = str(HISTORICAL)
        if item['id'] == later['id']:
            assert all(later['review'].values())
            expected = later['registered_reference']['raw_hex']
            approved = str(FOLLOWUP)
        assert bytes.fromhex(expected).rstrip(b' ') == bytes.fromhex(item['current']['raw_hex']).rstrip(b' ')
        rows.append(item | dict(file_path=stage.FILE, block=stage.BLOCK,
            source_meaning=old_review['source_meaning'].replace('Christina', 'Cristina'), localization_note=item['reason'],
            context='Julio remembers his granddaughter, tells Lil she is skilled with a sword and says where she lives. Lil agrees to go.',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
            archived_approval=approved, contextual_source_offset=item['source']['offset'],
            registered_reference=item['target'] | dict(candidate_sha256=candidate),
            fresh_format_check=n == stage.ORDINAL, name_source_actor=7 if n == stage.ORDINAL else None))
    draft = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(rows[0]['review']), records=rows, candidate_sha256=candidate, historical_evidence=historical,
        spelling_census=staged['target_spelling_census'], native_actor_name_evidence=actor, additional_dialogue_credit=0,
        gameplay=game, checked_story_format_guard=checked)
    validate_natural_dialogue_batch(draft)
    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged | dict(target_ARM9_sha256=prior['target_ARM9_sha256']), draft, tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', required=True)
    viewed = parser.parse_args().viewed_sha
    original = getsource(predecessor.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    doc = '''    base.replace_checked(DOC, f\'''# Cristina’s recruitment dialogue

In Lil’s story, Julio remembers his granddaughter, Cristina, and suggests bringing her along. The clean text names クリスティナ, and both current name getters return Cristina Erneco. His line now reads “Yes! Let’s bring Cristina along.” The following exchange still tells Lil that Cristina is his granddaughter, is skilled with a sword and lives in London. The seven individual reasons for retaining the other lines are in the [registered review](../{REVIEW.as_posix()}).

The correction updates the one stored Christina spelling found across the 1,307 story blocks. The exact 3,668 mapped shared records and the Help and ARM9 string scans also returned no Christina hits. The edit keeps all command extents, speaker selectors, nearby replies and the original one-line fit. The revised line passed a complete native font comparison and paired initialized Lil gameplay. Those runs show the original eight-line exchange with ordinary controller inputs. Natural activation and hardware remain untested. A separate cumulative startup and {tests} targeted tests passed. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) reconstruct the release byte for byte and preserve all 114 accepted layers. The dialogue ledger stays at 27,700 credited records, with 276 mapped shared keys still open.
\'''.encode('utf-8'))'''
    replacements = {
        original[first:last]: doc,
        '825 entries, 114 accepted layers and 160 passing checks': '826 entries, 114 accepted layers and 161 passing checks',
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159": "len(manifest['batches']) == 825 and len(manifest['checks']) == 160",
        'registered_manifest_entries=825, passing_release_checks=160': 'registered_manifest_entries=826, passing_release_checks=161',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.cristina_recruitment.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.cristina_recruitment.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_cristina_recruitment.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_ritual_officiant_predecessor=predecessor, cristina_recruitment_name_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['cristina_recruitment_name_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.FILE].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']": "story_block=stage.BLOCK, revised_ordinal=stage.ORDINAL",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.FILE]',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=0, justified_retentions=7, reviewed_UI_labels=0, story_name_revisions=1',
        'initialized_Rafael_dialogue=True': 'initialized_Lil_dialogue=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['cristina_recruitment_name_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'story_name_revisions=1, justified_retentions=7',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Julio uses the approved Cristina spelling in Lil’s recruitment exchange.',
        '# Ritual Officiant Labels test candidate': '# Cristina Recruitment Name test candidate',
        'distinguishes two ritual officials from the Christian Priest role': 'uses Cristina in Julio’s recruitment dialogue',
        '(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft[\'native_sheet\'][\'path\']), QA)':
            '(stage.STORED, STARTUP, live.LIVE, live.SHEET, QA)',
        'Preserve verified ritual title candidate': 'Preserve verified Cristina recruitment candidate',
    }
    env = vars(predecessor) | globals() | dict(VIEWED=viewed, STARTUP=live.STARTUP)
    exec(compile(checked_text(original, replacements), __file__ + '::registered-story-successor', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
