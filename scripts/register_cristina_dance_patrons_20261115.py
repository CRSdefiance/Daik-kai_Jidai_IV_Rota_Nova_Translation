"""Register the four-route patron dialogue and byte-exact clean-input patch."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_cristina_dance_patrons_20261115 as live
from scripts import stage_cristina_dance_patrons_20261115 as stage
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-cristina-dance-patrons-v1-20261115'
ROOT = Path('out/cristina_dance_patrons_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Cristina_Dance_Patrons_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_cristina_dance_patrons_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_cristina_dance_patrons_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_cristina_dance_patrons_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds')


def verify(prior, guard, viewed):
    staged, boot, game, draft = map(base.load, (stage.STORED, STARTUP, live.OUTPUT, stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert all(r['candidate_sha256'] == candidate for r in (staged, boot, game, draft))
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256'] == game['previous_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(p) == sha for proof in (boot, game) for p, sha in proof['evidence'].items())
    assert game['initialized_story'] and not game['natural_event_activation'] and not game['hardware']
    assert len(game['held_panels']) == 3 and len(game['exact_control_frames']) == 9
    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert len(sheet['messages']) == 12 and base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests == 32 and all(int(suite.get(k, 0)) == 0 for k in ('failures', 'errors', 'skipped'))

    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(stage.files, (old, new))
    changed = staged['target_story_archive_sha256']
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == changed.keys()
    for path, compiled in stage.transform(old, draft['records']):
        assert compiled == after[path] and stage.digest(compiled) == changed[path]
    assert stage.digest(after[stage.ARM]) == staged['target_ARM9_sha256'] == prior['target_ARM9_sha256']
    verify_runtime(after[stage.ARM], prior)
    checked = bind_registered_story_percent_guard(guard)(stage.files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    for path in changed:
        new.replace_file(path, before[path])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()

    assert len(draft['records']) == 72 and sum(row['decision'] == 'revision' for row in draft['records']) == 9
    for row in draft['records']:
        row['registered_reference'] = row['staged_reference'] | {'candidate_sha256': candidate}
    draft.update(gameplay=game, native_sheet=sheet, checked_story_format_guard=checked)
    validate_natural_dialogue_batch(draft)
    if not review.PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, review.PATCH)
    if not review.REBUILT.exists():
        apply_xdelta(stage.CLEAN, review.PATCH, review.REBUILT)
    assert review.REBUILT.read_bytes() == stage.ROM.read_bytes()
    return staged, draft, tests


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# The patrons at Cristina’s dance

The four routes now use **Patron 1**, **Patron 2**, and **Patrons** for the same two onlookers. Nine embedded labels and cheers were revised. The 63 retentions include each captain’s distinct reaction, Cristina’s explanation, and Claudio’s apology in Rafael’s route. All 72 lines have exact Japanese and current references. [Review ledger](../{REVIEW.as_posix()})

All 12 patron panels passed native glyph, bounds and one-panel checks and were visually reviewed. The paired initialized Rafael replays copied the original excerpt and its scene controls into the established opening fixture. All three revised holds matched their full text masks, and nine other frames matched, including dismissal, Rafael and Claudio’s regular nameplates, and the applause. The other routes were checked offline. Natural event activation and hardware remain open. [Before and after](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers, the unchanged actor table and the ASCII right-bound correction. Six startup frames, 24 protected name getters, {tests} targeted tests and byte-exact reconstruction passed. All 72 lines already carried editorial credit.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 835 and len(manifest['checks']) == 170",
        '825 entries, 114 accepted layers and 160 passing checks': '836 entries, 114 accepted layers and 171 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=836, passing_release_checks=171',
        "verify(prior, profile['source25_multiarchive_guard'])": "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.cristina_dance_patrons.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.cristina_dance_patrons.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_cristina_dance_patrons.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_square_trend_dialogue_predecessor=predecessor, cristina_dance_patrons_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['cristina_dance_patrons_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "for row in draft['records']:\n"
            "        if row['decision'] == 'revision':\n"
            "            records = manifest['changed_records'][row['file_path']]\n"
            "            if row['id'] not in records:\n"
            "                records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks=dict(zip(staged['target_story_archive_sha256'], stage.BLOCKS))",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], "
            "**{f'target_SC{i}_sha256': staged['target_story_archive_sha256'][f'/data/SC{i}.DK4'] for i in range(4)},",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], "
            "**{f'SC{i}_sha256': release[f'target_SC{i}_sha256'] for i in range(4)}, registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            "changed_components=[], changed_internal_files=list(staged['target_story_archive_sha256'])",
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=9, text_display_revisions=0, justified_retentions=63, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['cristina_dance_patrons_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=9, justified_retentions=63',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The patrons at Cristina’s dance now use consistent labels across all four routes.',
        '# Ritual Officiant Labels test candidate': '# Cristina Dance Patrons test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'localizes the patron labels in all four routes’ Cristina dance scenes',
        "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA)":
            "(stage.STORED, STARTUP, live.OUTPUT, live.SHEET, Path(draft['native_sheet']['path']), QA)",
        'Preserve verified ritual title candidate': 'Preserve verified Cristina Dance Patrons candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register-dance-patrons', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
