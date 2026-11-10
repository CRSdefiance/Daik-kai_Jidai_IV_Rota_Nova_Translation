"""Bind individual decisions to the reviewed identities and correct source-gloss attribution."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Lil269_B243_B282_clean_20261110')
REASONS={
2:'Retain approved Lil Argot and exact default-name macros. Her curious, flippant, compassionate and deliberately teasing replies do not invent kinship or romance.',
13:'Retain Cesare Tony, matching the clean components. His ornate figurehead admiration and private spiritual reflections do not make him a priest or introduce a different title.',
20:'Retain Fernando Dias. Clean actor20 owns the wall discovery, statue alarm, curse concern and bodily-heaviness replies in B251; these are not Lil speaking twice or an anonymous extra sailor.',
62:'Retain Jacks Bloom, faithful to Jakkusu Buruumu and both native consumers. The source explicitly calls him English; do not change him to a historical French Jacques or infer nationality from spelling.',
63:'Retain Julian Vermeer, matching both source components and established consumers. The source explicitly identifies him as Portuguese; the surname does not license rewriting his nationality or biography.',
64:'Retain Yuris Huygens, the source-bound forms. Correct older Ulis/Huygen body spellings; noble birth does not establish a newly named hereditary title.',
65:'Retain Plett Perrault, consistently with the native consumers. Correct Prett Perrot in the earlier prose; the source murderer is brought alive and his fate is left to the client.',
67:'Retain Gabriel Cardocci, matching the source identity and approved current consumers. Correct Cardocchi in body text; his explicit Italian origin needs no invented Roman-peninsula euphemism.',
68:'Retain Jacob Portunto, correcting Portund body text. Smuggler, pirate pretensions and cargo obsession concern the same source character, not a new rank or company.',
69:'Retain Peralonso Aguirre, a sensible source-bound Spanish name. His spy role and comic overfamiliarity establish no historical identity or relationship with Lil.',
70:'Retain Zaganos Bey as the established full name. Bey is a source name component, not a new rank conferred by this review; capture does not prove execution.',
92:'Retain Barkeep for the source tavern proprietor. Oyaji/ojisan are familiar addresses, not evidence of fatherhood; European metadata is not a surname.',
96:'Retain Patron for the source tavern customer. This actor interrupts the B256 barkeep/Lil exchange before Jacks appears; do not merge the patron with the barkeep or invent a friendship.',
113:'Retain Port Worker for the original port-office service role. Familiar brother-like Japanese wording creates no actual brotherhood or named naval rank.',
147:'Retain Guildmaster for the source guild head in the European quest exchanges. Regional metadata is not a personal surname, and the role does not make him the captives\' relative.',
148:'Retain Guildmaster for the source guild head in the Basra spy exchange. The unconsumed Islam/Arab metadata discrepancy remains in the broader name/metadata review; this scoped label approves neither a personal surname nor an ethnicity.',
149:'Retain Guildmaster for the source guild head in the Plett exchange. His authority to pass the captive to the client does not make him her father or establish a sentence.',
151:'Retain Sailor on the progressive nameplate and the existing Retainer catalogue alias for this exact startup fallback. Selector208 resolves here only before a conditional assignment; no future roster, feudal rank or full catalogue UI approval is inferred. Broader catalogue role wording stays in scope.',
188:'Retain Margrete, faithful to Marugureete and established consumers. Hamburg is regional metadata, not an appended surname or a new nationality claim.',
189:'Retain Wanda, matching the source name and both consumers. Her friendly ruins response establishes no new relationship with Lil.',
190:'Retain Julia for Juria. Her Lisbon metadata is not a surname, and Julia is not the separate adventurer Julian Vermeer.',
193:'Retain Myrine for Myurinee as the established individual name. The ancient-civilization conversation gives her no invented academic title or mythological biography.',
195:'Retain Nelly for Nerii. The still-Japanese unconsumed Alexandria metadata remains in the broader name review; this nameplate/catalogue-string review does not approve that hidden field globally.',
196:'Retain Hatra for Hatora and the current consumer spelling. Her Solomon-treasury rumor does not identify her with a city or confer historical expertise.',
200:'Retain Titis for Tititisu, matching both current consumers. Her local-ruins invitation does not establish identity with the separate FE entity voice or authorize an unrequested mythological rename.',
}


def main():
    out=ROOT/'contextual_comparisons_v2.json';config=ROOT/'prose_config_v1.json'
    assert not out.exists() and not config.exists()
    source=ROOT/'contextual_comparisons_v1.json';doc=deepcopy(load(source));changes=[]
    fixes={
        'DK4_MES_B251_R0006':'Fernando calls the admiral over to writing on the wall.',
        'DK4_MES_B251_R0109':'Fernando notices the wall opening.',
        'DK4_MES_B251_R0117':'Fernando alerts the admiral to a strange statue.',
        'DK4_MES_B251_R0124':'Fernando points it out and says it resembles a figurehead.',
        'DK4_MES_B251_R0131':'Fernando cries out in alarm, asking what is happening.',
        'DK4_MES_B251_R0139':'Fernando cries out and stammers for the admiral.',
        'DK4_MES_B251_R0161':'Fernando is taken aback by the offer of power.',
        'DK4_MES_B251_R0171':'Fernando wonders what that was and worries that using the object could bring a curse.',
        'DK4_MES_B251_R0204':'Fernando stammers and urges escape.',
        'DK4_MES_B251_R0231':'After escape Fernando pants and expresses relief at the close call.',
        'DK4_MES_B251_R0234':'Fernando notices feeling physically heavy; no cause or magnitude is stated in the speech.',
        'DK4_MES_B256_R0020':'A separate tavern patron asks whether Lil is looking for Jacks.',
        'DK4_MES_B256_R0027':'The patron implies the answer should be obvious before Jacks interrupts.',
    }
    for row in doc['records']:
        if row['id'] in fixes:
            assert row['source_selector']==(96 if row['block']==256 else 20)
            before=row['source_meaning'];row['sealed_independent_source_meaning']=before;row['source_meaning']=fixes[row['id']]
            changes.append(dict(id=row['id'],field='source_meaning',before=before,after=row['source_meaning'],reason='Exact complete source preamble and bound clean/current actor identity resolve the speaker; sealed draft and source bytes remain unchanged.'))
        if row['block']==256:
            row['sealed_independent_exchange_context']=row['whole_exchange_context']
            row['whole_exchange_context']='Lil asks a barkeep about Jacks Bloom. A separate Patron interrupts to ask if she seeks Jacks, who then appears and identifies himself. She relays Hamburg\'s search and Jacks asks for passage. Preserve all three NPC roles and the source name; no kinship or invented friendship.'
        if row['id']=='DK4_MES_B256_R0027':
            before=row['finding'];row['finding']=row['finding'].replace("barkeep's","patron's");row['localization_note']=row['finding']
            changes.append(dict(id=row['id'],field='finding',before=before,after=row['finding'],reason='Describe the exact actor96 patron rather than actor92 barkeep.'))
    assert len(changes)==14
    doc.update(contextual_attribution_corrections=changes,sealed_original_drafts_andcomparisons_preserved=True,
        parent_comparisons=str(source),parent_comparisons_sha256=digest(source))
    save(out,doc)
    names=ROOT/'scoped_names_macros_reference_v2.json';assert {r['actor_ID'] for r in load(names)['records']}==set(REASONS)
    save(config,dict(proposals=str(out),names=str(names),terms=str(ROOT/'scoped_terms_reference_v1.json'),
        roles=str(ROOT/'dynamic_roles_current_v1.json'),objects=str(ROOT/'current_objects_v1/current_objects.json'),
        source_objects=269,proposal_counts=[104,165],final_counts=[104,165],item_bindings=0,file_path='/data/SC2.DK4',
        name_reasons=REASONS,scope_id='LIL_SC2_B243_B282_269',name_context='Forty complete Lil SC2 exchanges B243-B282, scoped native nameplate/catalogue strings and original startup fallback only; unconsumed metadata, full catalogue layout and future conditional roles remain unvisited.',
        amendments={},FE_contexts={249:'FE pay and Sofala-share notices',250:'FE unnamed protective voice and separate Luck/Charm+1 notices',
            251:'FE puzzle inscription, crackling sound and unnamed authoritative entity; no ordinary actor nameplate',
            257:'FE pay and Hamburg-share notices',261:'FE pay and two distinct Seville-share notices',265:'FE pay and Basra-share notices',
            268:'FE pay and Batavia-share notices',271:'FE pay and Hangzhou-share notices',273:'FE advance-payment notice',
            274:'FE pay and Calicut-share notices',276:'FE advance-payment notice',277:'FE pay and Havana-share notices',
            279:'FE advance-payment notice',280:'FE pay and Genoa-share notices'},
        kind_counts={'progressive':226,'system-FE':36,'typed-choice-label':7},
        out='translations/lil_B243_B282_contextual_review_v1.json',names_out='translations/lil_B243_B282_scoped_names_v1.json',proof_out=str(ROOT/'prose_gates_v1.json')))
    print('Prepared269 contextual decisions,25 individual name reasons and14 precise attribution-note corrections;sealed originals preserved.')


if __name__=='__main__':main()
