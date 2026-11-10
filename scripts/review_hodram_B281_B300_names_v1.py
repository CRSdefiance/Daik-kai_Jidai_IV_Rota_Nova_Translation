"""Review scoped speakers and four explicitly spoken names with the original current getters."""
from scripts import review_hodram_B251_B280_names_v1 as previous
from scripts.review_hodram_B281_B300_contextual_v1 import ROOT,CURRENT,OUT as PROSE
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

NATIVE=ROOT/'scoped_names_current_v1.json';REVIEW=Path('translations/hodram_B281_B300_scoped_names_review_v1.json')
ROLES=ROOT/'role_bindings_v1.json';TERMS=ROOT/'scoped_terms_v1.json'
SPOKEN={28:[(286,16)],42:[(286,12),(286,16),(286,27)],43:[(286,16)],73:[(282,19),(285,6)]}
REASONS={
1:'Retain approved Hodram, Joakim and Bergstrom, preserving progressive/full-name components. Royal deference, dry reflections and expedition commands do not create a new rank. FA remains surname, FI given name.',
14:'Retain Emilio Ferog. His named sleeping sound confirms actual sleep in the bear exchange, not death or a new relationship; the nameplate remains the same companion.',
16:'Retain Gerhard Adernkatz. The tactical advice, rescue effort and polite FI address belong to the established companion; 殿 does not require Lord or a new rank.',
18:'Retain Charles Rochefort and the source Jean middle component in the full-name consumer. His research, curiosity and material requests do not identify a historical person or add a profession to his nameplate.',
22:'Retain Samwell Khan and the source da component where the full-name consumer uses it. His uncertain man-eating-bear warning does not change identity, age or rank.',
28:'Retain James Clifford in the original consumers; the spoken surname Clifford matches クリフォード. The source places him in England without inventing a noble title or expanding this line into a biography.',
42:'Retain Vasquez Maldonado and the full-name de component. Tribute and the relative comparison with William remain dialogue about this established opponent, not a new moral judgment in the nameplate.',
43:'Retain accepted Diogo Escante and full Diogo de Escante. The surname in the Mexico reference matches the source; do not revert Diogo to another name or invent a title.',
71:'Retain William Clive for ウィリアム・クライブ. His shrill capture cries are character behavior, not an animal identity; retain the established surname and given name.',
73:'Retain native Iscal Yasar for イスカル・ヤサール. The source gloss’s provisional Iskal is not an approved rename. Both spoken full name and given-name reminder use Iscal; no new rank, ethnic surname or historical identity is invented.',
119:'Retain Port Worker for 出港所の兄貴. Familiar occupational address does not make him the captain’s brother, and the separate regional Native metadata is not part of his name.',
120:'Retain Guard for 衛兵. Relaying the king’s summons supports the role but not a specific officer rank, personal identity or family relation.',
125:'Retain King for 国王. The scene explicitly concerns Sweden’s monarch and supports Your Majesty in dialogue; it does not name the king or justify adding a historical royal identity.',
147:'Retain Guildmaster for ギルドの元締め. The shared job/return slot remains occupational across towns, not one invented person everywhere or a noble title.',
148:'Retain Guildmaster in the Islamic-region slot. The impatient Hernan reminder does not turn regional metadata into a religious title or a personal biography.',
151:'Retain Sailor on progressive nameplates and Retainer in the full-name consumer. Generic expedition reports and unassigned roles208/211/215/216 use this qualified fallback without asserting future conditional participation or a new rank.',
179:'Retain Villager for 村民. His ancestors/warrior legend and offer to accompany the search do not supply a tribal name, priesthood, age or new nationality label.',
194:'Retain Faticia for ファティシア. Istanbul is location metadata, not a surname. Her lightly flirtatious tip does not establish romance, kinship or a new profession.'}

source=checked_text(previous.source,{
    '    assert set(actors)==expected and len(actors)==21':
        '    expected|=set(SPOKEN)\n    assert set(actors)==expected and len(actors)==18',
    "len(result['rows'])==42":"len(result['rows'])==36",
    'assert set(prior_fields)==set(actors)':'assert set(prior_fields)==set(actors)-set(SPOKEN)',
    "                old=next(f for f in existing[151]['clean_fields'] if f['column']==column)\n                assert all(field[k]==old[k] for k in ('source_ARM9_field_offset','pointer_hex','hex','text'))":
        "                assert actor in SPOKEN and pointer==int.from_bytes(clean[at:at+4],'little')",
    "contexts=[r['id'] for r in prose['records'] if r.get('source_selector')==actor or (actor==151 and r.get('source_selector')==208)]":
        """contexts=[r['id'] for r in prose['records'] if r.get('source_selector')==actor or (actor==151 and r.get('source_selector') in [208,211,215,216])
            or (r['block'],r.get('source_reference',{}).get('record_index')) in SPOKEN.get(actor,[])]
        assert contexts""",
    'current_native_getters=42':'current_native_getters=36',
    'scoped_actors=21,justified_retentions=21':'scoped_actors=18,justified_retentions=18',
    'Reviewed 21 scoped names: 21 justified retentions; 42 fresh current getters.':
        'Reviewed 18 scoped names: 18 justified retentions; 36 fresh current getters.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-name-contract-speakers-and-explicit-spoken-identities','exec'),env)
if __name__=='__main__':env['main']()
