"""Review eight scoped speakers through the original current name consumers."""
from pathlib import Path
from scripts import review_hodram_B251_B280_names_v1 as previous
from scripts.review_hodram_B301_B310_contextual_v1 import ROOT,CURRENT,OUT as PROSE
from scripts.source_locked_derivation_v5118 import checked_text

NATIVE=ROOT/'scoped_names_current_v1.json';REVIEW=Path('translations/hodram_B301_B310_scoped_names_review_v1.json')
ROLES=ROOT/'role_bindings_v1.json';TERMS=ROOT/'scoped_terms_v1.json'
REASONS={
1:'Retain approved Hodram and Joakim with Bergstrom in their distinct progressive/full-name components. The temple objection, monk conversation and injury notice identify the same captain; FI is his given-name substitution, not a title or new party member.',
16:'Retain Gerhard Adernkatz. The equipment reminder and qualified travel estimates belong to this established companion. His practical advice does not add a medical, noble or military title.',
137:'Retain Senior Monk for 高僧. The Buddhist temple context and source elevated monastic status support the natural role label without naming an abbot, religious head or additional office. Japanese is regional metadata, not part of his name.',
151:'Retain Sailor on progressive nameplates and Retainer in the full-name consumer. The frightened cries and qualified fallback for unassigned roles208/211/214/215/218 remain generic. No actual future role assignment, new personal identity or rank is inferred.',
192:'Retain Matilda for マチルダ. Genoa is separate location metadata, not a surname. Her helpful Colosseum clue and friendly greeting do not establish romance, kinship or participation in the expedition.',
197:'Retain Safia for サフィア. Basra is location metadata, not a surname or a religious identity. The dancing improvement and rumored treasure lead do not establish a specific prior lesson or romance.',
201:'Retain the established public Mihwa form for 美華, rather than the provisional Meihua source gloss. Hangzhou is separate metadata, not a surname or invented biography. The city-gate exception is discreet dialogue, not a new role or legal office.',
203:'Retain accepted Sakura for さくら. Osaka is location metadata, not a surname. Her temple visit and partway escort are friendly offers, not kinship, romance or participation in the full expedition.'}

source=checked_text(previous.source,{
    'len(actors)==21':'len(actors)==8',"len(result['rows'])==42":"len(result['rows'])==16",
    "or (actor==151 and r.get('source_selector')==208)":
        "or (actor==151 and r.get('source_selector') in [208,211,214,215,218])",
    'current_native_getters=42':'current_native_getters=16',
    'scoped_actors=21,justified_retentions=21':'scoped_actors=8,justified_retentions=8',
    'Reviewed 21 scoped names: 21 justified retentions; 42 fresh current getters.':
        'Reviewed eight scoped names: eight justified retentions; 16 fresh current getters.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-clean-fields-and-current-getters-new-eight-actor-scope','exec'),env)
if __name__=='__main__':env['main']()
