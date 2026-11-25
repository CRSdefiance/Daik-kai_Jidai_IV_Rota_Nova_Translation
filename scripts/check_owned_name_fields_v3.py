"""Check retained new names against the same proposed ARM9; reuse prior changed-name planes."""
from scripts import check_owned_name_fields_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "actors=sorted({o['actor'] for r in proposal['fields'] for o in r['owners']})":
    "actors=binding['actors'];assert actors==[13,24,38,58,92]",
    'original_progressive_andfull_name_getters_pass=True,':
    'rendered_actors=actors,original_progressive_andfull_name_getters_pass=True,',
})
exec(compile(source, __file__ + '::five-retained-new-source-bound-name-consumers', 'exec'), globals())
