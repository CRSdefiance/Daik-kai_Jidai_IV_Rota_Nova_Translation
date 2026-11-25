"""Compare source bytes directly, accepting either hex letter case without normalization."""
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.registered_reviewed_text_data_v2 import source as previous

source = checked_text(previous, {
    "clean[source['offset']:source['offset'] + source['capacity']].hex() == r['source_hex']":
        "clean[source['offset']:source['offset'] + source['capacity']] == bytes.fromhex(r['source_hex'])",
})
exec(compile(source, __file__ + '::exact-clean-source-bytes-independent-of-hex-letter-case', 'exec'), globals())
