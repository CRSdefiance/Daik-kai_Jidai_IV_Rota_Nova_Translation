"""Publish the reviewed Square briefings through the cumulative release workflow."""

from inspect import getsource
from pathlib import Path

from scripts import checkpoint_square_country_briefings_20261115 as live
from scripts import register_town_market_wraps_20261115 as template
from scripts import stage_square_country_briefings_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, parent, publisher = stage.base, stage.parent, template.publisher
PROFILE = 'all-routes-square-country-briefings-v1-20261115'
ROOT = Path('out/square_country_briefings_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Square_Country_Briefings_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_square_country_briefings_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_square_country_briefings_20261115.md')
STARTUP, QA = stage.ROOT / 'own_startup_verification.json', stage.ROOT / 'repository_qa_verified.xml'
NATIVE_SHEET = stage.ROOT / 'portrait_sheet_01.png'
VIEWED_NATIVE = 'c86ee70035803fc3a655a3e34f0aafb20793c3273bc010118af5cb9219aa904c'
VIEWED_GAMEPLAY = '109adf74f05fc57395a72fcef5acc29750b1f4d156757fdfba4446842f8c549b'
CHECKPOINT = 'Twenty-four Square shopkeeper replies and regional briefings are reviewed, with nine revisions registered.'
EDITED = sorted(stage.PROSE)


def verify(prior, guard):
    source = checked_text(getsource(template.verify), {
        "storage['preserved_entries'] == 3664": "storage['preserved_entries'] == 3659",
        "len(review['records']) == 12 and len(review['specialty_title_arguments']) == 25":
            "len(review['records']) == 24 and len(review['original_shop_condition_selectors']) == 13",
        "len(sheet['messages']) == 8": "len(sheet['messages']) == 18",
        "gameplay['observed_changed_keys'] == [739, 743, 748] and gameplay['offline_only_changed_keys'] == [749]":
            "gameplay['observed_changed_keys'] == [657, 689] and gameplay['offline_only_changed_keys'] == sorted(set(EDITED) - {657, 689})",
        "len(gameplay['complete_holds']) == 9 and len(gameplay['transitions']) == 3":
            "sum(map(len, gameplay['complete_holds'].values())) == 7 and len(gameplay['transitions']) == 2",
        "base.digest(live.SHEET) == gameplay['sheet_sha256']":
            "base.digest(live.SHEET) == gameplay['sheet_sha256'] == VIEWED_GAMEPLAY",
    })
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::verification', 'exec'), scope)
    return scope['verify'](prior, guard)


def update_country_ledger(ledger, release, sha, checkpoint):
    source = checked_text(getsource(template.update_ledger), {'town_market_wraps_20261115': 'square_country_briefings_20261115'})
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::ledger', 'exec'), scope)
    scope['update_ledger'](ledger, release, sha, checkpoint)


def main():
    source = getsource(template.main).replace('def main():', 'def publish():', 1)
    source = checked_text(source, {
        '== 816 and len(manifest["checks"]) == 151': '== 818 and len(manifest["checks"]) == 153',
        'registered_manifest_entries=817,passing_release_checks=152': 'registered_manifest_entries=819,passing_release_checks=154',
        '817 entries, 114 accepted layers, 152 checks.': '819 entries, 114 accepted layers, 154 checks.',
        'verified_expedition_report_wraps_predecessor': 'verified_square_samples_wraps_predecessor',
        'town_market_wraps.pending.json': 'square_country_briefings.pending.json',
        'release_stack_before_town_market_wraps.json': 'release_stack_before_square_country_briefings.json',
        'town_market_wraps_release': 'square_country_briefings_release',
        'registered_town_market_wraps_and_complete_parent_inverse': 'registered_square_country_briefings_and_complete_parent_inverse',
        'town_market_wraps_registered_successor_pipeline': 'square_country_briefings_registered_successor_pipeline',
        'Source-reviewed town and Market prose and wraps.': 'Source-reviewed Square shopkeeper replies and country briefings.',
        'prose_revisions=2,justified_retentions=8,text_display_revisions=4': 'prose_revisions=9,justified_retentions=15,text_display_revisions=9',
        'observed_changed_keys=[739, 743, 748], observed_complete_holds=9, offline_specialty_argument_pairs=25':
            'observed_changed_keys=[657, 689], observed_complete_holds=7, offline_only_changed_keys=[690, 693, 694, 696, 702, 704, 705]',
        '# Town and Market Wraps test candidate': '# Square Country Briefings test candidate',
        'includes the revised town and Market dialogue': 'includes the revised Square shopkeeper replies and country briefings',
        'Preserve town and Market wrap release and verified replays.': 'Preserve the Square country briefings release and ordinary Amsterdam replay.',
        'env = vars(publisher) | globals() | dict(DIGEST=digest)':
            'env = vars(publisher) | globals() | dict(DIGEST=digest, update_ledger=update_country_ledger)',
    })
    start = source.index("    document = '''")
    end = source.index("    source = source[:start] + document", start)
    document = '''    base.replace_checked(DOC, f"""# Square shopkeeper replies and country briefings

The [registered review](../{REVIEW.as_posix()}) checks 24 records against the clean Japanese and cumulative English, with nine revisions and fifteen individual retentions. The retail exchange keeps the question tag and the complete reply about bulk trade on separate lines. The Dutch briefing reads in two lines. Spain’s speaker reports the nickname as hearsay, the Genoa and Venice briefing restores trading rights, and Yi Seong-gye’s whole name stays together. The briefings are independent local selections that use the original square shopkeeper consumer.

The ordinary Amsterdam New Game replay verified seven complete dialogue holds, six **Shopkeeper** nameplates, and two menu returns. The revised trade-house referral appeared in the Jewelry Shop. The revised independence briefing appeared in the Liquor and Jewelry shops. The other seven revised briefings were checked through the original renderer offline. All 18 [before and after pages](../{(VERIFY / 'portrait_sheet_01.png').as_posix()}) and the [gameplay sheet](../{(VERIFY / 'gameplay_lower_screens.png').as_posix()}) received visual review. Hardware remains untested.

The cumulative cold boot matched six startup frames and 24 protected name getters. Forty targeted tests passed. The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. All 24 records had prior credit. The ledger records 27,700 credited reviews and 276 mapped shared records still to review or classify.
""".encode())'''
    source = source[:start] + '    document = ' + repr(document) + '\n' + source[end:]
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::successor', 'exec'), scope)
    scope['publish']()


if __name__ == '__main__':
    main()
