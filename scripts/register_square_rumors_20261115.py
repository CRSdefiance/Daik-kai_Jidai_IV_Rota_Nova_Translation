"""Register the reviewed Square rumors with their exact clean-input patch."""

from inspect import getsource
from pathlib import Path

from scripts import checkpoint_square_rumors_20261115 as live
from scripts import register_town_market_wraps_20261115 as template
from scripts import stage_square_rumors_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent, publisher = stage.base, stage.parent, template.publisher
PROFILE = 'all-routes-square-rumors-v1-20261115'
ROOT = Path('out/square_rumors_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Square_Rumors_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_square_rumors_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_square_rumors_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED_NATIVE = '8427f4232c6f5037a85cf63d88f33729c7d93aba780bb59dec521f9f12e74393'
VIEWED_GAMEPLAY = 'd0d3796e209c8104086f1596b15d06e6af5e4d560e439e115bddb5610d690a1b'
CHECKPOINT = 'All 21 Square regional rumors are reviewed, with ten revisions registered.'
EDITED = sorted(stage.PROSE)


def verify(prior, guard):
    source = checked_text(getsource(template.verify), {
        'map(stage.files, (old, new))': 'map(template.stage.files, (old, new))',
        'guard)(stage.files(base.NdsImage.open(stage.CLEAN)), after)':
            'guard)(template.stage.files(base.NdsImage.open(stage.CLEAN)), after)',
        "storage['preserved_entries'] == 3664": "storage['preserved_entries'] == 3658",
        "len(review['records']) == 12 and len(review['specialty_title_arguments']) == 25":
            "len(review['records']) == 21 and len(review['source_exact_ranges']) == 4",
        "len(sheet['messages']) == 8": "len(sheet['messages']) == 20",
        "gameplay['observed_changed_keys'] == [739, 743, 748] and gameplay['offline_only_changed_keys'] == [749]":
            "gameplay['observed_changed_keys'] == [709, 729] and gameplay['offline_only_changed_keys'] == sorted(set(EDITED) - {709, 729})",
        "len(gameplay['complete_holds']) == 9 and len(gameplay['transitions']) == 3":
            "len(gameplay['complete_holds']) == 2 and len(gameplay['transitions']) == 8",
        "base.digest(live.SHEET) == gameplay['sheet_sha256']":
            "base.digest(live.SHEET) == gameplay['sheet_sha256'] == VIEWED_GAMEPLAY",
    })
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::verification', 'exec'), scope)
    return scope['verify'](prior, guard)


def update_rumor_ledger(ledger, release, sha, checkpoint):
    source = checked_text(getsource(template.update_ledger), {'town_market_wraps_20261115': 'square_rumors_20261115'})
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::ledger', 'exec'), scope)
    scope['update_ledger'](ledger, release, sha, checkpoint)


def main():
    source = getsource(template.main).replace('def main():', 'def publish():', 1)
    source = checked_text(source, {
        '== 816 and len(manifest["checks"]) == 151': '== 819 and len(manifest["checks"]) == 154',
        'registered_manifest_entries=817,passing_release_checks=152': 'registered_manifest_entries=820,passing_release_checks=155',
        '817 entries, 114 accepted layers, 152 checks.': '820 entries, 114 accepted layers, 155 checks.',
        'verified_expedition_report_wraps_predecessor': 'verified_square_country_briefings_predecessor',
        'town_market_wraps.pending.json': 'square_rumors.pending.json',
        'release_stack_before_town_market_wraps.json': 'release_stack_before_square_rumors.json',
        'town_market_wraps_release': 'square_rumors_release',
        'registered_town_market_wraps_and_complete_parent_inverse': 'registered_square_rumors_and_complete_parent_inverse',
        'town_market_wraps_registered_successor_pipeline': 'square_rumors_registered_successor_pipeline',
        'Source-reviewed town and Market prose and wraps.': 'Source-reviewed regional rumors in the Square.',
        'prose_revisions=2,justified_retentions=8,text_display_revisions=4': 'prose_revisions=10,justified_retentions=11,text_display_revisions=10',
        'observed_changed_keys=[739, 743, 748], observed_complete_holds=9, offline_specialty_argument_pairs=25':
            'observed_changed_keys=[709, 729], observed_complete_holds=2, offline_only_changed_keys=[712, 713, 716, 719, 720, 724, 725, 726]',
        '# Town and Market Wraps test candidate': '# Square Rumors test candidate',
        'includes the revised town and Market dialogue': 'includes the revised Square rumors',
        'Preserve town and Market wrap release and verified replays.': 'Preserve the Square rumors release and verified replays.',
        'env = vars(publisher) | globals() | dict(DIGEST=digest)':
            'env = vars(publisher) | globals() | dict(DIGEST=digest, update_ledger=update_rumor_ledger)',
    })
    start = source.index("    document = '''")
    end = source.index("    source = source[:start] + document", start)
    document = '''    base.replace_checked(DOC, f"""# Square regional rumors

The [registered review](../{REVIEW.as_posix()}) compares all 21 regional rumors against the clean Japanese and the cumulative English. Ten lines are revised and eleven are retained with individual reasons. Clifford’s rumor keeps his former piracy, his admiralty and the reported knighthood. Sweden’s fleet pays its own way through trade and privateering. The Escante rumor keeps Mexico and Peru together. Hayreddin’s current wording preserves the father relationship without assigning a specific kind of kinship.

Two Istanbul replays used disposable copies of the same save and the previously documented five-byte region and random seed setup. Clifford and Escante both displayed complete body and Shopkeeper nameplate glyphs on the original consumer. The candidate’s entire message block appeared once in each live cache, and both rumors returned to the shop list after one advance. The other eight revisions were checked offline with the original renderer. All 20 [before and after pages](../{(VERIFY / 'portrait_sheet_01.png').as_posix()}) and the [gameplay sheet](../{(VERIFY / 'gameplay_lower_screens.png').as_posix()}) received visual review. Ordinary regional travel and hardware were outside the replay scope.

The exact [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. Six startup frames, 24 protected name getters and 40 targeted tests passed. All 21 records had prior editorial credit. The ledger records 27,700 credited reviews and 276 mapped shared records still to review or classify.
""".encode())'''
    source = source[:start] + '    document = ' + repr(document) + '\n' + source[end:]
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::successor', 'exec'), scope)
    scope['publish']()


if __name__ == '__main__':
    main()
