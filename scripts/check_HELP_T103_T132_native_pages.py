"""Fresh complete native parser/font/glyph/bounds checks for all30 Deck tutorial pages."""
from scripts import check_HELP_T44_T80_native_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'Shared_HELP_T44_T80_formatting_20261104':'Shared_HELP_T103_T132_formatting_20261104',
    "PLAN=ROOT/'refined_v2/automatic_plans_v1.json'":"PLAN=ROOT/'refined_v3/automatic_plans_v1.json'",
    'Early_HELP23_release_verified_20261104':'Shipyard_HELP37_release_verified_20261104',
    "len(plan['pages'])==38 and plan['target_topic_count']==217":"len(plan['pages'])==30 and plan['target_topic_count']==217",
    'len(proofs)==38 and len(sheets)==10':'len(proofs)==30 and len(sheets)==8',
    'native_pages=38,complete_articles=37':'native_pages=30,complete_articles=30',
    '38 native Help pages/37 articles pass;ten readable sheets needdirect view.':'30 native Deck Help pages pass;eight readable sheets need direct view.',
})
exec(compile(source,__file__+'::same-full-native-parser-pixel-font-link-and-memory-guards-for30-final-Deck-pages','exec'),globals())
