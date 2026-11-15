"""Register the verified Square giveaway and shop replies on the cumulative release."""

from inspect import getsource
from pathlib import Path

from scripts import checkpoint_square_samples_wraps_20261115 as live
from scripts import register_town_market_wraps_20261115 as parent
from scripts import stage_square_samples_wraps_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, publisher = stage.base, parent.publisher
PROFILE = 'all-routes-square-samples-wraps-v1-20261115'
ROOT = Path('out/square_samples_wraps_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Square_Samples_Wraps_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_square_samples_wraps_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_square_samples_wraps_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED_NATIVE = '0cff219ea9e8ed1c0f860ae219eda5cd4a7755417af980fea7ee6e8b26ae48cf'
CHECKPOINT = 'Twenty-two Square giveaway and shop replies are reviewed, with nine changes registered.'
EDITED = sorted(set(stage.PROSE) | set(stage.PHRASES))


def verify(prior, guard):
    source = checked_text(getsource(parent.verify), {
        "storage['preserved_entries'] == 3664": "storage['preserved_entries'] == 3659",
        "len(review['records']) == 12 and len(review['specialty_title_arguments']) == 25":
            "len(review['records']) == 22 and len(review['original_shop_condition_selectors']) == 13",
        "len(sheet['messages']) == 8": "len(sheet['messages']) == 18",
        "gameplay['observed_changed_keys'] == [739, 743, 748] and gameplay['offline_only_changed_keys'] == [749]":
            "gameplay['observed_changed_keys'] == [665, 673, 683] and gameplay['offline_only_changed_keys'] == [659, 661, 667, 672, 684, 687]",
        "len(gameplay['complete_holds']) == 9 and len(gameplay['transitions']) == 3":
            "len(gameplay['complete_holds']) == 6 and len(gameplay['transitions']) == 5",
    })
    scope = vars(parent) | globals()
    exec(compile(source, __file__ + '::verification', 'exec'), scope)
    return scope['verify'](prior, guard)


def main():
    source = getsource(parent.main).replace('def main():', 'def publish():', 1)
    source = checked_text(source, {
        '== 816 and len(manifest["checks"]) == 151': '== 817 and len(manifest["checks"]) == 152',
        'registered_manifest_entries=817,passing_release_checks=152': 'registered_manifest_entries=818,passing_release_checks=153',
        '817 entries, 114 accepted layers, 152 checks.': '818 entries, 114 accepted layers, 153 checks.',
        'verified_expedition_report_wraps_predecessor': 'verified_town_market_wraps_predecessor',
        'town_market_wraps.pending.json': 'square_samples_wraps.pending.json',
        'release_stack_before_town_market_wraps.json': 'release_stack_before_square_samples_wraps.json',
        'town_market_wraps_release': 'square_samples_wraps_release',
        'registered_town_market_wraps_and_complete_parent_inverse': 'registered_square_samples_wraps_and_complete_parent_inverse',
        'town_market_wraps_registered_successor_pipeline': 'square_samples_wraps_registered_successor_pipeline',
        'Source-reviewed town and Market prose and wraps.': 'Source-reviewed Square giveaway and shop replies.',
        'prose_revisions=2,justified_retentions=8,text_display_revisions=4': 'prose_revisions=7,justified_retentions=13,text_display_revisions=9',
        'observed_changed_keys=[739, 743, 748], observed_complete_holds=9, offline_specialty_argument_pairs=25':
            'observed_changed_keys=[665, 673, 683], observed_complete_holds=6, offline_only_changed_keys=[659, 661, 667, 672, 684, 687]',
        '# Town and Market Wraps test candidate': '# Square Samples Wraps test candidate',
        'includes the revised town and Market dialogue': 'includes the revised Square giveaway and shop replies',
        'Preserve town and Market wrap release and verified replays.': 'Preserve Square giveaway and shop reply release and verified replays.',
        'env = vars(publisher) | globals() | dict(DIGEST=digest)':
            'env = vars(publisher) | globals() | dict(DIGEST=digest, update_ledger=update_square_ledger)',
    })
    start = source.index("    document = '''")
    end = source.index("    source = source[:start] + document", start)
    document = '''    base.replace_checked(DOC, f"""# Square giveaway and shop dialogue

The [registered review](../{REVIEW.as_posix()}) checks 22 records against the clean Japanese and current English. It covers the free-sample confirmations and pitches, the customer’s response, and the shopkeeper’s replies under six town conditions. Seven records received prose revisions, two keep the same wording with improved wrapping, and thirteen retain their prior wording and presentation. The game’s original post-load wrapper was checked for the alternative voices. Every changed page passed complete glyph, width and allocation checks. All 18 [before and after pages](../{(VERIFY / 'portrait_sheet_01.png').as_posix()}) received visual review.

Two Istanbul emulator replays confirmed the revised sample prompt, Manuel’s revised pitch, the customer’s retained response, a retained shop greeting and the rewrapped epidemic reply. Six complete dialogue holds and five transitions passed. The normal giveaway consumed both selected cargo units. A three-byte Chapel and role fixture and a separate two-byte town condition fixture supplied the prerequisites in disposable saves. Six changed alternatives were checked offline. [Gameplay sheet](../{(VERIFY / 'gameplay_lower_screens.png').as_posix()})

The cumulative cold boot matched six startup frames and 24 protected name getters. Forty targeted tests passed. The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and the ASCII right-bound correction. Hardware confirmation remains open. All 22 records had prior credit. The ledger stands at 27,700 reviews, with 276 mapped shared records remaining.
""".encode())'''
    source = source[:start] + '    document = ' + repr(document) + '\n' + source[end:]
    scope = vars(parent) | globals()
    exec(compile(source, __file__ + '::successor', 'exec'), scope)
    scope['publish']()


def update_square_ledger(ledger, release, sha, checkpoint):
    source = checked_text(getsource(parent.update_ledger), {'town_market_wraps_20261115': 'square_samples_wraps_20261115'})
    scope = vars(parent) | globals()
    exec(compile(source, __file__ + '::ledger', 'exec'), scope)
    scope['update_ledger'](ledger, release, sha, checkpoint)


if __name__ == '__main__':
    main()
