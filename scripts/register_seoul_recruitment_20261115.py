"""Register the verified Seoul recruitment revision and its clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_regional_town_dialogue_20261115 as regional
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import stage_seoul_recruitment_20261115 as stage
from scripts import verify_seoul_recruitment_20261115 as live
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-seoul-recruitment-v1-20261115'
ROOT = Path('out/seoul_recruitment_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Seoul_Recruitment_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_seoul_recruitment_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_seoul_recruitment_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_seoul_recruitment_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft, towns = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT, regional.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert all(p['candidate_sha256'] == candidate for p in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256'] == towns['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for proof in (boot, game, towns) for p, sha in proof['evidence'].items())
    assert game['ordinary_saved_game_entry'] and len(game['observed_panels']) == 35
    assert game['recruitment_notice'][0]['text'] == 'Yifa Sol joined!' and len(game['returned_control_frames']) == 5
    assert sum(map(len, towns['original_town_dialogue'].values())) == 19 and towns['layout_followups'] == [654, 732]
    sheet_paths = [live.SHEET, *(Path(row['path']) for row in staged['sheets'])]
    assert tuple(map(base.digest, sheet_paths)) == viewed == (game['sheet_sha256'], *(row['sha256'] for row in staged['sheets']))
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.FILE}
    assert stage.digest(after[stage.FILE]) == staged['target_SC3_sha256']
    assert stage.digest(after[stage.ARM]) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    changes = [row for row in draft['records'] if row['decision'] != 'retention']
    assert [row['id'] for row in changes] == staged['changed_records'] and len(changes) == 15
    (path, compiled), = stage.prior.transform(old, changes)
    assert path == stage.FILE and compiled == after[stage.FILE]
    memo = base.load(parent.MANIFEST)['relocations'][stage.ARM]['reviewed_name_integration']['catalog']
    archives = [stage.IlnkContainer.parse(image[f'/data/SC{route}.DK4']).blocks
                for image in (before, after) for route in range(4)]
    assert catalogue(after[stage.ARM], memo, archives[:4]) == catalogue(after[stage.ARM], memo, archives[4:])
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.FILE, before[stage.FILE])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    assert len(draft['records']) == 35 and sum(r['decision'] == 'revision' for r in changes) == 11
    for row in draft['records']:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
        row['review']['formatting'] = True
    draft.update(gameplay=game, checked_story_format_guard=checked,
                 regional_observations=str(regional.OUTPUT), regional_observations_sha256=base.digest(regional.OUTPUT))
    validate_natural_dialogue_batch(draft)
    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged, draft, tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=5, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Yifa’s recruitment in Seoul

All 35 lines were reviewed as an exchange, from Yukihisa catching Yifa following the party to Maria taking her aboard as an equal. Eleven lines were revised for voice or clarity, four keep their wording with better wraps, and twenty were retained with individual reasons. The company substitution stays in Yifa’s request. Maria and Yukihisa recognize her skill while leaving her claim about the binding spell open. [Exact source and current references](../{REVIEW.as_posix()})

Paired ordinary cold boots used the same Seoul save and inputs. The original Square entrance activated the entire event. All 35 complete dialogue masks and nameplates passed, including the company substitution. Five controls matched, including the pause during the demonstration, **Yifa Sol joined!**, and the return to the Square. The original Square calls and later shop exchanges agree. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The separate Tunis, Valencia and Syracuse runs verified 19 complete holds across nine shared records. The Tunis stock recommendation splits “be sure,” and the trend forecast splits “a while.” Both are recorded for a subsequent wrap pass. [Regional dialogue ledger](../{regional.OUTPUT.as_posix()})

The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers and original script controls. Six startup frames, 24 protected name getters, {tests} targeted tests, and byte-exact clean-input reconstruction passed. The 35 story records already had editorial credit. The ledger stands at 27,700 credited reviews and 276 mapped shared keys still open. Hardware was outside the replay scope.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 833 and len(manifest['checks']) == 168",
        '825 entries, 114 accepted layers and 160 passing checks': '834 entries, 114 accepted layers and 169 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=834, passing_release_checks=169',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.seoul_recruitment.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.seoul_recruitment.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_seoul_recruitment.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_market_conversation_predecessor=predecessor, seoul_recruitment_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['seoul_recruitment_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "manifest['changed_records'][stage.FILE].extend(ident for ident in staged['changed_records'] "
            "if ident not in manifest['changed_records'][stage.FILE])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_block=[stage.FILE, stage.BLOCK], changed_records=staged['changed_records']",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], target_SC3_sha256=staged['target_SC3_sha256'],",
        'changed_components=[stage.ARM], changed_internal_files=[]': 'changed_components=[], changed_internal_files=[stage.FILE]',
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], SC3_sha256=release['target_SC3_sha256'], registered_release_verification=str(RELEASE)",
        'new_contextual_records=0, prose_revisions=0': 'new_contextual_records=0, prose_revisions=11',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=0, text_display_revisions=4, justified_retentions=20, reviewed_UI_labels=0',
        'initialized_Rafael_dialogue=True': 'ordinary_seoul_recruitment=True',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['seoul_recruitment_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'prose_revisions=11, wrap_revisions=4, justified_retentions=20',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'Yifa’s full Seoul recruitment is reviewed and tested in ordinary gameplay. Regional town replays verify 19 additional holds.',
        '# Ritual Officiant Labels test candidate': '# Seoul Recruitment test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'improves dialogue and wraps in Yifa’s recruitment through Seoul Square',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA, regional.OUTPUT, *(Path(r['path']) for r in staged['sheets']))",
        'Preserve verified ritual title candidate': 'Preserve verified Seoul recruitment candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::registered-seoul-recruitment', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
