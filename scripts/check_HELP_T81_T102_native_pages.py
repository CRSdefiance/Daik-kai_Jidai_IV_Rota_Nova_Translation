"""Fresh full native Help parser/glyph/bounds checks on22 sea/battle/password pages."""
from scripts import check_HELP_T44_T80_native_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
 'Shared_HELP_T44_T80_formatting_20261104':'Shared_HELP_T81_T102_formatting_20261104',
 'Early_HELP23_release_verified_20261104':'Town_HELP23_release_verified_20261104',
 "len(plan['pages'])==38 and plan['target_topic_count']==217":"len(plan['pages'])==22 and plan['target_topic_count']==217",
 'len(proofs)==38 and len(sheets)==10':'len(proofs)==22 and len(sheets)==6',
 'native_pages=38,complete_articles=37':'native_pages=22,complete_articles=22',
 '38 native Help pages/37 articles pass;ten readable sheets needdirect view.':'22 native Help pages/22 articles pass;six readable sheets needdirect view.',
})
exec(compile(source,__file__+'::unchanged-current-parser-full-font-instruction-andmemory-guards-for22-pages','exec'),globals())
