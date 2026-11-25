"""Assemble all reviewed exchanges and record contextual name/gloss corrections."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil382_residual_A_clean_20261110')
CONTEXTS = {
0: 'Yukihisa recognizes Muramasa with awe and describes its uncanny glow. Preserve the cursed-blade epithet without inventing an actual supernatural effect.',
1: 'Gerhard recognizes the recovered object by its unchanged dull gleam and marvels that nobody picked it up. He parted with it; no cause of loss or item identity is established here.',
2: 'Hayreddin threatens the party in separate battle alternatives, including a warning about an unnamed man more fearsome than himself. Yukihisa, Al and Gerhard answer in their distinct warrior voices; no superior rank or battle result is added.',
3: 'Aziza rallies her pirates against FO: Snake takes command, Angel steers to the enemy starboard quarter and Dandy reports gun readiness. Fernando reacts to a woman pirate; Lil accepts the challenge. Preserve each source actor and faction substitution.',
4: 'Separate Aziza encounter alternatives show discovery, a crew rally and a renewed threat to sink FO. These are conditional encounters, not one forced chronology.',
5: 'Lil confronts Yuris the ship thief. His offended appeal to noble birth meets her impatient disbelief that he is fussing over a nickname while facing capture.',
6: 'Lil condemns Plett Perrault for murder. He deflects by accusing her of having sins too; her anger escalates into a refusal to hold back. His defense establishes no equal crime by Lil.',
7: 'Lil condemns Jacob Portunto for petty trading tricks that disgrace merchants. Jacob reacts with contempt for a lecture from her; invent no new commercial offense or age.',
8: 'Lil challenges Gabriel over selfish trading and harm to others. His dismissal of agreements ends her attempt at persuasion and leads to a challenge, without an invented treaty or outcome.',
9: 'Lil feels capable of defeating Zaganos Bey now. His booming reply threatens that her boast will be her last words; neither confidence is a confirmed result.',
10: 'After defeat, Hayreddin lets Lil go with a warning to avoid the southern Mediterranean and build renown in Africa or Asia. Lil resents losing, Camille recognizes their strength and Gerhard values everyone being safe.',
11: 'Victory and Camille’s praise turn solemn when Manuel mourns the fallen and recites three stanzas comparing sea and mother. Lil is baffled and pouts at Camille’s teasing; Manuel closes with gentle acceptance. Keep the foreign sound/writing claim as hearsay and infer no dead mother or romance.',
12: 'The complete Aziza mutiny, rescue and recruitment arc links profit resentment to her father’s Bloodstained Shamshir. Al intervenes; Yukihisa, Cristina and Fernando assist; Lil refuses to tolerate murder and bargains from a two-million demand to one million. Aziza recalls Basra mercy, her father’s accidental death and the vanished sword, realizes she wanted his keepsake, voluntarily leaves piracy and joins Lil. Preserve grief, agency and playful gratitude; invent no romance, marriage, shipwreck or killer.',
13: 'Separate Aziza withdrawal and Lil victory alternatives preserve their spirited rivalry, the refusal to submit and Aziza Nurennahar’s full name. Do not merge alternative outcomes.',
14: 'Separate Lil defeat/retreat alternatives contrast her frustrated resolve, Fernando’s recommendation to withdraw and Aziza’s confident death threats. Preserve the source speakers without deciding every escape outcome.',
15: 'Captured Yuris is to be taken to Batavia. His pained disbelief contrasts with Lil’s brisk confidence; no particular sentence is given.',
16: 'Lil takes captured Plett toward Hangzhou and mocks his lost bravado. His claim of repentance remains his own speech, not proof of genuine reform.',
17: 'Captured Jacob worries about cargo while Lil reminds him that he must face punishment in Calicut. Do not invent a sentence, confiscation or loss of the cargo.',
18: 'Gabriel’s capture for transport to Havana is separate from conditional recognition after the tavern scam. He minimizes the agreement breach and complains of two interferences only in that prior-meeting branch.',
19: 'Captured Zaganos demands death. Lil refuses and insists that he return to Genoa to apologize; this does not establish an execution or additional punishment.',
21: 'Escante approaches under mock courtesy to Miss FA, then orders surprise fire at the flagship. Cristina and Yifa have separate identical reactions. His free-lesson joke and further volley provoke Lil’s acceptance of war; no noble rank or death is implied.',
115: 'Read all 41 source objects: nine credited tablet/context objects involving Lil and Janus remain context only. The 32 eligible later objects explicitly use Maria3 and Xien10 within SC2. Bandits blame Europeans for their ruined village; Maria distinguishes slave traders and pillaging soldiers from indiscriminate targets, rejects cycles of revenge and proposes resisting great-power partition through the Proofs of Conquest. The bandits voluntarily accept her invitation to sea and offer an unnamed stone tablet. Preserve the source controls, colonial harms and qualified confidence; invent no kinship or roster post.',
235: 'Seven voice variants announce Charles’s letter. He reports sailors’ account of a Spanish merchant fleet traveling from the New World toward West Africa, a roar far west of Lisbon, renewed courage and an incidental Spanish naval rescue. The sound remains scientifically unexplained; Lil fears a possible monster. Preserve the source geography and hearsay, with Charles Jean Rochefort’s signature.',
236: 'Seven voice variants announce Jam’s letter. His personal excitement about India frames a Gupta sacred-beast statue rumor, alleged foresight and a hope of beating Fernando at gambling, despite finding no seller or witness. Fernando’s five-hundred-year retort is hyperbole. Lil remains interested despite Jam’s gambling focus. Use the current Jam Jack Ludwyan signature without inventing a real-world identity or item effect.',
237: 'Cesare indignantly recounts idle sailors’ Demon-Piercing Arrow rumors: an angel’s legendary weapon, rumored archery skill, speculative cannon usefulness and competing Skye/Lewis leads. Lil privately tires of the rant. Preserve Cesare’s fussy voice and the uncertainty of every alleged location and effect.',
238: 'Janus catches his hand on a metal mast fitting. A port worker praises protective gloves, cannot find them and tentatively recalls Denmark before insisting on Jutland. Lil agrees to search; he offers the gloves because they do not fit and he had intended to sell them. Preserve his claims as claims, without kinship, a diagnosis or an unspoken catalogue title.',
239: 'Francisca’s sadness concerns a stolen glass rose ornament Dad bought for her birthday, valuable to her despite uncertain price. The bartender’s brusqueness does not identify him as Dad. Both New World answers lead to a friend-of-a-friend’s Havana swindler story; Lil doubts the connection, Camille urges help and haste, and Lil promises to try. Keep both menu indices and the thief’s initial uncertainty.',
240: 'Gabriel’s unpaid-tab joke leads to an attempted payment with fake amethyst. Lil identifies glass and the real owner; the barkeep confronts him, but he escapes. The barkeep returns the ornament and vows to hand him to the governor’s office if found again. Preserve joke, escalation and future intent; invent no family relationship, exact party count, arrest or death.',
241: 'Lil returns the Frozen Rose to Francisca, whose relief leads to a suggestion to visit the wooden church on the outskirts, described as unusual for Europe. Preserve the actual handover, warm thanks and prospective visit.',
242: 'Julio admires a figurehead; the priest says it chooses its carrier, most failed seekers return injured and it mysteriously returns after an owner’s death. Try/refuse options lead to separate reluctant-help, failure, success and refusal material. Preserve luck, modesty, religious blessings and the exact FI Spirit increase of one; invent no deliberate figurehead attack or extra acquisition notice.',
}
NAME_REASONS = {
2: 'Retain approved Lil Argot. Her playful confidence, sympathy and bargaining fit the existing identity; FI/FA/FO remain runtime substitutions rather than license to rewrite other source speakers.',
3: 'Retain approved Maria Li and full Maria Huamei Li. The later B115 source explicitly uses actor3 within SC2; her moral argument and invitation establish no new rank, kinship or male identity.',
4: 'Retain Janus Pasar, the established rendering of Jenasu Pasaa. Correct provisional Jenas references in contextual metadata; his injury and the tablet discussion do not establish a new personal relationship.',
6: 'Retain Julio Erneco. His aged, reluctant speech does not justify Boss replacing the explicit Admiral address or an invented kinship with Lil or the priest.',
7: 'Retain Cristina Erneco consistently with the bound current consumers for this scope. Correct provisional Christina references; wider earlier spelling consumers remain in the broader name review, without inventing a familial relationship from her surname.',
9: 'Retain approved Camille Overijssel and full Camille Marinus Overijssel. His practical reassurance, enjoyment of poetry and sympathy remain distinct from Lil; the poem establishes no romance.',
10: 'Retain Xien Yan. His sharp B115 bandit rebuke belongs to the exact source actor10, not a substituted Lil companion or a newly ranked officer.',
11: 'Retain Jam Ludwyan and full Jam Jack Ludwyan as the established source-bound forms. Use that exact letter signature; the provisional Ledoyen draft neither establishes a new spelling nor a historical French identity.',
12: 'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His contemplative and formal warrior speech needs no invented Lord title, family link or new rank.',
13: 'Retain Cesare Tony. His fussy rant concerns crew maintenance and rumors; it confers no religious office or historical identity.',
16: 'Retain Gerhard Adernkatz. Preserve his first-person refusal to lose and his reflective concern for safety; the recovered object does not authorize a new surname or title.',
17: 'Retain Al Shin and full Al Ferid Shin. His decisive help to Aziza establishes no romance, marriage or ownership of her.',
18: 'Retain Charles Rochefort and full Charles Jean Rochefort, matching the letter signature. His scientific interest establishes no doctorate or confirmed expertise about the roar.',
20: 'Retain Fernando Dias. Clean actor20 is Ferunando Diasu; Emilio is a different actor. Correct both current Peres and the independent draft Emilio in Jam’s gambling line, and audit all source-gloss labels using actor20.',
23: 'Retain Manuel Almeida. His memorial poem and spiritual language establish no newly ranked priesthood or claim about his actual mother’s fate.',
25: 'Retain Yifa Sol. Her Escante-bombardment reaction is a source actor25 alternative, not Cristina speaking twice or a new relationship.',
27: 'Retain Aziza Nurennahar consistently with her full self-introduction. Just call me Aziza permits familiar address; her pirate father and the rescue establish no relationship with Al beyond the source exchange.',
34: 'Retain Barbarossa Hayreddin and full Barbarossa Fazul Hayreddin. His named threat and comparison with an unnamed more fearsome man do not establish a new superior, title or identity.',
43: 'Retain Diogo Escante and full Diogo de Escante. His mock Miss FA courtesy requires no noble Lady title for Lil or an invented rank for himself.',
64: 'Retain Yuris Huygens, the established source-bound identity. Correct current Ulysse and provisional Juris in body/gloss references; noble birth is his explicit claim, not a newly named hereditary title.',
65: 'Retain Plett Perrault. Correct Prett Perot in the older body text; his criminal identity and claimed repentance authorize no particular sentence or genuine reform.',
67: 'Retain Gabriel Cardocci. His selfish trading, swindle and escape are separate source events; do not invent a historical identity, noble title or new relationship with the barkeep.',
68: 'Retain Jacob Portunto. His petty trading and cargo obsession identify the same character without an invented company or judicial title.',
70: 'Retain Zaganos Bey as the established complete name. The existing Bey component is not a new rank granted by this review; Lil’s refusal to kill him preserves the source outcome.',
92: 'Retain Barkeep as the natural generic tavern-role nameplate. Oyaji and dear do not prove fatherhood or intimacy; European metadata is not a personal surname.',
113: 'Retain Port Worker for the source port-worker archetype. Aniki is familiar address, not proof of being Janus’s brother; European metadata adds no personal surname or biography.',
139: 'Retain Priest for the explicit Christian clergy role. Father is an appropriate respectful address in this exchange, not a family relationship or a new ecclesiastical rank.',
151: 'Retain Sailor on the progressive nameplate and the existing generic service-role alias Retainer in the catalogue. This is the source lookout and startup fallback for selector208/voice4, not an observed future crew assignment or a granted feudal rank. Broader catalogue role terminology remains separate.',
153: 'Retain Sailor for Aziza’s collective pirate-crew cheers and the existing catalogue subordinate alias Retainer. The source regional metadata is not a surname; do not turn the collective cheer into a named officer or a new feudal rank.',
180: 'Retain Bandit for the explicit source bandit role. Africa is regional metadata, not a surname or proof of a specific ethnicity; the spokesman’s revenge and voluntary acceptance need no invented leader title.',
183: 'Retain Angel as the pirate’s explicit nickname. It does not make him the supernatural angel in the unrelated arrow legend or establish a holy identity.',
184: 'Retain Snake as the pirate’s explicit nickname. His command response and mutiny add no real animal identity, family relationship or newly granted rank.',
185: 'Retain Dandy as the pirate’s explicit nickname. His restrained readiness report and later bargaining need no noble title or invented relationship.',
186: 'Retain Francisca for the source Furanshisuka identity. Stockholm is place metadata, not a surname; her explicitly mentioned Dad is not identified as the barkeep.',
}


def main():
    out = ROOT/'contextual_comparisons_v1.json'
    config = ROOT/'prose_config_v1.json'
    assert not out.exists() and not config.exists()
    partpaths = [ROOT/f'comparisons_{name}_v1.json' for name in
        ['B0_B11','B12','B13_B21_B115','B235_B238','B239_B242']]
    parts = [load(p) for p in partpaths]
    packetpath = ROOT/'clean_source_packet.json'
    packet = load(packetpath)
    rows = [deepcopy(r) for p in parts for r in p['records']]
    selected = [r for g in packet['groups'] for r in g['records']]
    assert len(rows) == len(selected) == len({r['id'] for r in rows}) == 382
    assert set(CONTEXTS) == set(packet['selected_blocks'])
    assert all(p['runtime'] == parts[0]['runtime'] and p['all_five_gates_still_pending'] for p in parts)
    corrections = []
    for row, original in zip(rows, selected, strict=True):
        assert all(row[k] == original[k] for k in ['id','file_path','source_hex','source_reference','source_Japanese'])
        assert not any(row['review'].values())
        before = row['source_meaning']
        after = before
        for a, b in [('Emilio','Fernando'),('Jenas','Janus'),('Christina','Cristina'),('Juris','Yuris'),('Devil-Piercing','Demon-Piercing')]:
            after = after.replace(a,b)
        if after != before:
            corrections.append(dict(id=row['id'], field='source_meaning', before=before, after=after,
                reason='Contextual reconciliation with exact clean actor20 identity or bound current name/item consumer; sealed source-first drafts remain unchanged.'))
            row['sealed_independent_source_meaning'] = before
            row['source_meaning'] = after
        priorcontext = row['whole_exchange_context']
        row['sealed_independent_exchange_context'] = priorcontext
        row['whole_exchange_context'] = CONTEXTS[row['block']]
        if row['block'] == 0 and row['id'] == 'DK4_MES_B0_R0010':
            beforefinding = row['finding']
            assert beforefinding.startswith('Retain Gerhard-like formality')
            row['finding'] = "Retain Yukihisa's contemplative formality: the uncanny glow draws him in without adding a power or a curse effect."
            row['localization_note'] = row['retention_reason'] = row['finding']
            corrections.append(dict(id=row['id'],field='retention_reason',before=beforefinding,after=row['finding'],
                reason='Describe the actual speaker’s formal source voice without an unnecessary comparison to another character.'))
    assert len(corrections) == 23
    counts = Counter(r['decision'] for r in rows)
    assert counts == {'revision':257,'retention':125}
    namespath = ROOT/'scoped_names_macros_reference_v1.json'
    names = load(namespath)
    assert {r['actor_ID'] for r in names['records']} == set(NAME_REASONS)
    evidence = {str(p):digest(p) for p in [*partpaths,packetpath,namespath,ROOT/'scoped_terms_reference_v1.json',
        ROOT/'dynamic_roles_current_v1.json',ROOT/'current_objects_v1/current_objects.json',ROOT/'clean_draft_seal_v1.json',Path(__file__)]}
    save(out, dict(records=rows,records_count=382,complete_exchanges=30,blocks=packet['selected_blocks'],runtime=parts[0]['runtime'],
        revised=257,retained=125,all_individual_findings_andretention_reasons_saved=True,all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,
        contextual_metadata_corrections=corrections,complete_exchange_contexts_reviewed=CONTEXTS,
        sealed_independent_drafts_preserved_not_rewritten=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    save(config, dict(proposals=str(out),names=str(namespath),terms=str(ROOT/'scoped_terms_reference_v1.json'),
        roles=str(ROOT/'dynamic_roles_current_v1.json'),objects=str(ROOT/'current_objects_v1/current_objects.json'),
        source_objects=382,proposal_counts=[257,125],final_counts=[257,125],item_bindings=6,file_path='/data/SC2.DK4',
        name_reasons=NAME_REASONS,scope_id='LIL_SC2_RESIDUAL_A_382',
        name_context='All30 complete clean/current Lil residual-A source groups; exact scoped nameplate/catalogue consumers only. Native startup role fallback is not future conditional participation.',
        amendments={},FE_contexts={115:'FE whispering panel; no actor nameplate',241:'FE Frozen Rose handover; no actor nameplate',242:'FE FI Spirit increase of one; no actor nameplate'},
        kind_counts={'progressive':375,'system-FE':3,'typed-choice-label':4},
        out='translations/lil_residual_A_382_contextual_review_v1.json',
        names_out='translations/lil_residual_A_382_scoped_names_v1.json',proof_out=str(ROOT/'prose_gates_v1.json')))
    print('PASS all382 comparisons merged in source order;23 explicit metadata corrections;34 scoped names prepared.')


if __name__ == '__main__':
    main()
