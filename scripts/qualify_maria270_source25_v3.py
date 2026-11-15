"""Make the injected unowned prose satisfy the unchanged detector's English threshold."""
from scripts.qualify_maria270_source25_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{"b'%s      '":"b'%s ABC  '"})
exec(compile(source,__file__+'::same-four-original-detector-rejections-with-English-prose-fixture','exec'),globals())
