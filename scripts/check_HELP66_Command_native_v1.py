"""Fresh native checks for the changed fleet page and its unchanged continuation."""
from scripts import check_HELP_T44_T80_native_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'Shared_HELP_T44_T80_formatting_20261104': 'HELP66_Command_amendment_20261104',
    "PLAN=ROOT/'refined_v2/automatic_plans_v1.json'": "PLAN=ROOT/'automatic_plans_v1.json'",
    'Early_HELP23_release_verified_20261104': 'Town_HELP23_release_verified_20261104',
    "len(plan['pages'])==38 and plan['target_topic_count']==217": "len(plan['pages'])==2 and plan['target_topic_count']==217",
    'len(proofs)==38 and len(sheets)==10': 'len(proofs)==2 and len(sheets)==1',
    'native_pages=38,complete_articles=37': 'native_pages=2,complete_articles=1',
    '38 native Help pages/37 articles pass;ten readable sheets needdirect view.': 'Fleet66: two native pages pass; one readable sheet needs direct view.',
})
exec(compile(source, __file__ + '::same-complete-native-parser-font-bounds-and-glyph-checks-for66-216', 'exec'), globals())
