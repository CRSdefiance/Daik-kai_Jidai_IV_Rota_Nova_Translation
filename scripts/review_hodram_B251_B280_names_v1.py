"""Review scoped names and roles using fresh current getters and exact clean fields."""
import inspect
from pathlib import Path
from scripts import review_hodram_B231_B250_names_terms_v1 as previous
from scripts.review_hodram_B251_B280_contextual_v1 import ROOT,CURRENT,OUT as PROSE
from scripts.source_locked_derivation_v5118 import checked_text

NATIVE=ROOT/'scoped_names_current_v1.json';REVIEW=Path('translations/hodram_B251_B280_scoped_names_review_v1.json')
ROLES=ROOT/'role_bindings_v1.json';TERMS=ROOT/'scoped_terms_v1.json'
REASONS={
1:'Retain approved Hodram and Joakim with Bergstrom. Progressive and full-name consumers preserve distinct source components. FA is the surname, not an organization or unspoken rank.',
13:'Retain Cesare Tony. His elaborate figurehead praise, doubts and private thoughts belong to the same companion; no divine identity or religious occupation is added to his name.',
20:'Retain Fernando Dias. His riddle discovery, fear and curse question do not justify a new title, family label or narrator identity.',
63:'Retain Julian Vermeer for ジュリアン・フェルメール. The guild calls him Portuguese and a traitor aiding Spain; those allegations remain dialogue, not a new nameplate title or external biography.',
64:'Retain Yuris Huygens for ユリス・ヒュイゲン. Correct Yulis in the story to the public Yuris form. His noble status is explicit but supplies no specific Lord title, historical identity or new family relationship.',
65:'Retain the accepted Plett Perrault public fields. Correct Prett Perot/Prett in this dialogue; the father’s killing and daughter’s revenge do not add an execution, surname variant or invented rank.',
66:'Retain Jean Ramusio for ジャン・ラムジオ. His smuggling accusations and self-serving denials identify this speaker without making the claim of innocence a narrator fact.',
67:'Retain established Gabriel Cardocci for ガブリエル・カルドッチ. The provisional Carducci gloss does not justify silently renaming the character. His Italian origin is explicitly in dialogue; no new biography or kinship is inferred.',
68:'Retain accepted Jacob Portunto. His source Dutch identity, alleged African windfall and pirate pretensions remain dialogue; they do not create a pirate rank in his name.',
72:'Retain Hernan Berio for エルナン・ベリオ. The provisional Berrio gloss is not an approved rename. His self-important 様 is localized through the boast, removing the invented Lord from speech without adding a title to the nameplate.',
92:'Retain Barkeep for 酒場の親父. The tavern debt and dry retort establish the occupation; father-like address does not establish age or a family relationship.',
113:'Retain Port Worker for 出港所の兄貴. London/Stockholm referrals concern his work; familiar address does not mean the captain’s brother.',
114:'Retain Port Worker in the African regional slot. Region metadata distinguishes a source slot, not a new personal name, nationality claim or family relation.',
147:'Retain Guildmaster for ギルドの元締め. The London, Stockholm and San Jorge commissions identify a shared occupational slot, not one invented personal identity across all towns.',
148:'Retain Guildmaster in the Islamic-region slot. Basra, Calicut and Athens jobs do not turn opaque regional metadata into a religious title or a personal biography.',
149:'Retain Guildmaster in the Chinese-region slot. His compassion and moral anger in the Hangzhou job do not establish the daughter’s relationship to him.',
151:'Retain Sailor on the progressive nameplate and Retainer in the full-name consumer. This source actor reports Gabriel’s suspected stolen property and is also the qualified unassigned companion-role fallback; neither function creates a new rank or observed conditional participation.',
178:'Retain Follower for 信徒. The rude map buyer’s source label supports an adherent/follower, while this exchange alone supplies no specific religion, cult name, gender, age or leadership role. The earlier approved shared label remains valid here.',
189:'Retain Wanda for ワンダ. Her Amsterdam location is separate metadata, not a surname; the greeting supplies no new relationship.',
190:'Retain Julia for ジュリア. Lisbon remains location metadata, and her ruins answer adds no family link to similarly named characters.',
200:'Retain Titis for ティティス. Jakarta is location metadata; making an exception for a foreign visitor adds no new romance, kinship or occupation.'}

source=inspect.getsource(previous.main)
cut=source.index("    asset=Path('translations/all_item_names_arm9_v1.json');items=[]")
source=source[:cut]+"    print('Reviewed 21 scoped names: 21 justified retentions; 42 fresh current getters. Name planes remain.')\n"
source=checked_text(source,{
    'len(actors)==19':'len(actors)==21','len(result[\'rows\'])==38':'len(result[\'rows\'])==42',
    "assert set(prior_fields)==set(actors)-{151}":"assert set(prior_fields)==set(actors)",
    'if actor!=151:':'if actor in prior_fields:',
    "            assert not raw or raw.isascii()\n":"",
    "text=raw.decode('ascii') if pointer else None":"text=raw.decode('cp932') if pointer else None",
    'current_native_getters=38':'current_native_getters=42',
    'scoped_actors=19,justified_retentions=19':'scoped_actors=21,justified_retentions=21',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-name-contract-scoped-decisions-with-opaque-metadata','exec'),env)
if __name__=='__main__':env['main']()
