"""Permit source-bound per-record anonymous voice/narration labels without nameplates."""
from scripts import author_editorial_prose_packet_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "speaker=names[source['source_selector']]":
    "speaker=names.get(source['id'],names[source['source_selector']])",
})
env={**previous.write_packet.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::source-bound-semantic-speaker-label','exec'),env)
write_packet=env['write_packet']
