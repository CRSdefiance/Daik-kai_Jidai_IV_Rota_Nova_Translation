"""Review the eleven actual source speakers without turning metadata into biographies."""
from pathlib import Path
from scripts import review_hodram_B251_B280_names_v1 as previous
from scripts.review_hodram_B311_B324_contextual_v1 import ROOT, CURRENT, OUT as PROSE
from scripts.source_locked_derivation_v5118 import checked_text

NATIVE = ROOT / 'scoped_names_current_v1.json'
REVIEW = Path('translations/hodram_B311_B324_scoped_names_review_v1.json')
ROLES = ROOT / 'role_bindings_v1.json'
TERMS = ROOT / 'scoped_terms_v1.json'
REASONS = {
0: 'Retain approved Rafael Castor. Source actor0 actually speaks in B314 and B318, even though this is the SC1 archive. Castor Company is his explicit company identity in Hodram’s recognition, not a new surname, rank or relationship.',
1: 'Retain approved Hodram and Joakim with Bergstrom in their distinct progressive/full-name components. The decisive captain, FI injury notice and native captain-role207 identify the established captain without adding a new rank.',
2: 'Retain Lil Argot for リル・アーゴット. Her conditional recognition of Charles’s book supports her own excited voice, not a new relationship or asserted participation in every version of the exchange.',
18: 'Retain Charles Rochefort and full Charles Jean Rochefort for the source given/middle/surname components. His alchemical enthusiasm and the explicitly supported fleet-command joke do not put a new rank or noble particle in his name.',
22: 'Retain Samwell Khan and full Samwell da Khan in the two original name consumers. Preserve the comic doubtful python identification without inventing age or a professional title. These scoped getters do not approve every other middle-field consumer.',
151: 'Retain Sailor on progressive nameplates and Retainer in the full-name consumer. Cries, gear mishaps, survey reporting and the qualified unassigned-role fallback remain generic; neither source status nor regional metadata creates a named character or new rank.',
161: 'Retain Villager for 村民. The sextant barter and solemn unnamed-object offer establish no chief title, kinship or personal name. Asian metadata is separate from the progressive label and does not certify a biography.',
179: 'Retain Villager for 村民. The guide and grieving monk witness use a shared role slot; this does not prove they are one individual in all scenes. American metadata is not a surname, exact birthplace or invented chief title.',
204: 'Retain readable Verisa for ヴェリーサ. San Jorge is separate location metadata, not a surname. The incense-burner request, grateful reading and pirate warning do not establish romance, kinship or a magical occupation title in her label.',
205: 'Retain Silvia for シルビア. Veracruz is separate location metadata, not a surname. The friendly forgotten map lead supplies no new personal relationship or expedition role.',
206: 'Retain Isabel for イサベル. Bahamas is separate location metadata. Her concern for a respected monk establishes neither kinship nor a religious order or personal clerical title.'}

source = checked_text(previous.source, {
    'len(actors)==21': 'len(actors)==11',
    "len(result['rows'])==42": "len(result['rows'])==22",
    "or (actor==151 and r.get('source_selector')==208)":
        "or (actor==151 and r.get('source_selector') in [208,209,211,214,218])",
    'current_native_getters=42': 'current_native_getters=22',
    'scoped_actors=21,justified_retentions=21': 'scoped_actors=11,justified_retentions=11',
    'Reviewed 21 scoped names: 21 justified retentions; 42 fresh current getters.':
        'Reviewed eleven scoped names: eleven justified retentions; 22 fresh current getters.',
})
env = {**previous.env, **globals(), '__file__': __file__}
exec(compile(source, __file__ + '::same-clean-fields-current-getters-and-individual-name-decisions', 'exec'), env)
if __name__ == '__main__':
    env['main']()
