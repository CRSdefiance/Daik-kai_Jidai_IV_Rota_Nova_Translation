"""Register the localized embedded Boy and Foreign Girl panels."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import register_cristina_dance_patrons_20261115 as previous
from scripts import register_ritual_officiant_labels_20261115 as workflow
from scripts import replay_embedded_story_roles_20261115 as live
from scripts import stage_embedded_story_roles_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-embedded-story-roles-v1-20261115'
ROOT = Path('out/embedded_story_roles_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Embedded_Story_Roles_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_embedded_story_roles_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_embedded_story_roles_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'supported_qa.xml'
CHECK = 'registered_embedded_story_roles_and_complete_parent_inverse'
review = SimpleNamespace(PATCH=stage.ROOT / 'clean_input.xdelta', REBUILT=stage.ROOT / 'clean_rebuilt.nds',
                         NATIVE=stage.ROOT / 'portrait_sheet_02.png')


def verify(prior, guard, viewed):
    original = getsource(previous.verify)
    sheet_code = """    first, second = staged['sheets']
    assert base.digest(second['path']) == base.digest(review.NATIVE) == second['sha256']
    assert (base.digest(live.SHEET), base.digest(first['path']), base.digest(second['path'])) == viewed
    assert (game['sheet_sha256'], first['sha256'], second['sha256']) == viewed
    assert [len(sheet['messages']) for sheet in (first, second)] == [20, 18]
    assert base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']
    sheet = first"""
    replacements = {
        "len(game['held_panels']) == 3 and len(game['exact_control_frames']) == 9":
            "len(game['held_panels']) == 8 and len(game['exact_control_frames']) == 15",
        """    sheet, = staged['sheets']
    assert (base.digest(live.SHEET), base.digest(sheet['path'])) == viewed == (game['sheet_sha256'], sheet['sha256'])
    assert len(sheet['messages']) == 12 and base.digest(stage.MANUSCRIPT) == staged['manuscript_sha256']""": sheet_code,
        "len(draft['records']) == 72 and sum(row['decision'] == 'revision' for row in draft['records']) == 9":
            """len(draft['records']) == 29 and sum(row['decision'] == 'revision' for row in draft['records']) == 15
    assert sum(len(row['native_pages']) for row in draft['records']) == 38
    assert sum(bool(row['FI_offsets']) for row in draft['records']) == 3
    assert {row['substitution'] for row in game['held_panels']} == {'Hodram', None}
    draft['native_sheets'] = staged['sheets']""",
    }
    env = vars(previous) | globals()
    exec(compile(checked_text(original, replacements), __file__ + '::verify', 'exec'), env)
    return env['verify'](prior, guard, viewed)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=3, required=True)
    viewed = tuple(parser.parse_args().viewed_sha)
    original = getsource(workflow.main)
    first = original.index('    base.replace_checked(DOC, f')
    last = original.index("'''.encode('utf-8'))", first) + len("'''.encode('utf-8'))")
    note = """    base.replace_checked(DOC, f'''# Boy and Foreign Girl story panels

The [registered ledger](../{REVIEW.as_posix()}) covers 12 embedded Boy panels across the four Cristina rescue scenes and 17 Foreign Girl panels in Hodram’s route. The labels in 15 Hodram panels now use the same colon as the 14 retained panels. Cristina’s reassurance and the boy’s panic still alternate in the same order. The girl stays unnamed while she responds with gestures and tries Hodram’s name. She says Sera before her nameplate appears.

All 38 native previews were checked and viewed. This includes the three live name tokens at the same stored offsets, with their default, short and full 16-byte name samples. The two-line heading stays aligned with the body in the name exchange. Every revised panel fits its original byte allocation and one page. The surrounding commands and the actor catalog match the predecessor.

Paired Hodram cold boots ran the original extracted panel and speech commands in an initialized opening. Eight revised panels, including all three available Hodram substitutions, matched their complete masks. Fifteen frames matched exactly, including the transition to Sera’s ordinary nameplate and dismissal. This demonstrates the native display on the excerpt. Natural activation of those events and hardware testing remain open. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [cumulative candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the 114 accepted layers and ASCII right-bound correction. Six startup frames, 24 protected name getters, {tests} targeted tests and the byte-exact round trip passed. The 29 panels already carried editorial credit.
'''.encode('utf-8'))"""
    replacements = {
        original[first:last]: note,
        "len(manifest['batches']) == 824 and len(manifest['checks']) == 159":
            "len(manifest['batches']) == 836 and len(manifest['checks']) == 171",
        '825 entries, 114 accepted layers and 160 passing checks': '837 entries, 114 accepted layers and 172 passing checks',
        'registered_manifest_entries=825, passing_release_checks=160':
            'registered_manifest_entries=837, passing_release_checks=172',
        "verify(prior, profile['source25_multiarchive_guard'])":
            "verify(prior, profile['source25_multiarchive_guard'], VIEWED)",
        'release_stack.ritual_officiant.pending.json': 'release_stack.embedded_story_roles.pending.json',
        'editorial_review_current.ritual_officiant.pending.json': 'editorial_review_current.embedded_story_roles.pending.json',
        'release_stack_before_ritual_officiant.json': 'release_stack_before_embedded_story_roles.json',
        'verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW)':
            'verified_cristina_dance_patrons_predecessor=predecessor, embedded_story_roles_release=str(REVIEW)',
        "manifest['ritual_officiant_pipeline']": "manifest['embedded_story_roles_pipeline']",
        "manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')":
            "records = manifest['changed_records'][stage.FILE]\n"
            "    for row in draft['records']:\n"
            "        if row['decision'] == 'revision' and row['id'] not in records:\n"
            "            records.append(row['id'])",
        "owned_ARM9_fields=staged['fields'],\n        owned_alignment_span=staged['new_label_span']":
            "owned_story_blocks={stage.FILE: list(stage.BLOCKS)}",
        "target_ARM9_sha256=staged['target_ARM9_sha256'],":
            "target_ARM9_sha256=staged['target_ARM9_sha256'], "
            "target_SC1_sha256=staged['target_story_archive_sha256'][stage.FILE],",
        "ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE)":
            "ARM9_sha256=release['target_ARM9_sha256'], SC1_sha256=release['target_SC1_sha256'], "
            "registered_release_verification=str(RELEASE)",
        'changed_components=[stage.ARM], changed_internal_files=[]':
            'changed_components=[], changed_internal_files=[stage.FILE]',
        'initialized_Rafael_dialogue=True': 'initialized_Hodram_dialogue=True',
        'name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0':
            'name_label_revisions=15, text_display_revisions=0, justified_retentions=14, reviewed_UI_labels=0',
        "ledger['ritual_officiant_nameplates_20261115']": "ledger['embedded_story_roles_20261115']",
        'name_label_revisions=2, justified_retentions=13': 'name_label_revisions=15, justified_retentions=14',
        'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.':
            'The Boy and Foreign Girl panels now use consistent labels during Cristina’s rescue and Sera’s introduction.',
        '# Ritual Officiant Labels test candidate': '# Embedded Story Roles test candidate',
        'distinguishes two ritual officials from the Christian Priest role':
            'standardizes Boy and Foreign Girl labels while preserving the name reveal',
        'Preserve verified ritual title candidate': 'Preserve verified Embedded Story Roles candidate',
    }
    env = vars(workflow) | globals() | {'VIEWED': viewed}
    exec(compile(checked_text(original, replacements), __file__ + '::register', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
