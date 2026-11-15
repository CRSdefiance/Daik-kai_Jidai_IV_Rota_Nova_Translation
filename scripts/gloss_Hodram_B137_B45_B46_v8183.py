"""Save complete clean-first Hodram source glosses andbind all27 prior B44 clean callbacks;no credit."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183')
PACKETS={
    137:Path('work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json'),
    45:Path('work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json'),
    46:Path('work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json'),
}
NAMES=Path('work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json')
GLOSSES={
137:{
6:'Charles notices the visitor with a questioning grunt.',
10:'Camille hesitantly apologizes for what happened a short while earlier. The exact earlier incident must be bound to the completed B44 confrontation.',
14:'Charles recognizes Camille as someone associated with that young woman and aggressively demands the reason for coming. This is not a claim of a family relationship or a named occupation.',
17:'Camille insists on apologizing to everyone, sincerely asks forgiveness, and regrets the terrible things that were said. Preserve the apology for the earlier exchange rather than inventing a physical attack.',
21:'Charles remains silent. Preserve the source pause and speaker control rather than inserting a new spoken judgment.',
25:'Camille explains that Lil was not trying specifically to make them angry.',
28:'Once Lil decides someone is a business rival, Camille says, she cannot seem to speak to them in any other way. This explains her manner without denying the insult or inventing a new feud.',
32:'Camille insists that Lil is kind underneath, while qualifying that she jumps to conclusions and makes strong assumptions. Camille asks them to forgive Lil. Preserve the apologetic hesitations and qualified defense rather than converting it to unconditional approval.',
35:'Gerhard remains silent. Do not add agreement or a new reaction absent from the text.',
39:'Hodram recalls or checks whether the visitor is named Camille. The familiar honorific does not grant a rank, kinship, or new relationship.',
43:'Camille is startled to be addressed and confirms the name hesitantly.',
47:'Hodram formally acknowledges the courteous apology and says that Lil can put her talents to use because someone capable like Camille is beside her. Preserve the acknowledgment and assessment; do not invent romance, employment rank, or a recruitment offer.',
50:'Camille becomes flustered and modestly rejects or downplays the praise.',
54:'Hodram reassures Camille that they choose their enemies and will not harm Camille and Lil. He asks Camille to pass this on to the partner after returning. Partner here is supported as an association, not specified as romantic or familial; no formal alliance is concluded.',
58:'Camille thanks them with relief and politely takes leave.',
74:'Hodram pauses silently after Camille leaves. Do not manufacture a new opinion in that pause.',
78:'Gerhard describes the visitor as a promising young person with an interesting future. Do not turn the compliment into a threat or infer a hidden identity or biography.',
82:'Hodram thoughtfully observes that their own fleet is beginning to run short of people. This is a staffing observation, not proof of an exact gameplay crew count or an immediate order to recruit Camille.',
86:'Gerhard agrees that expanding the fleet calls for more capable people.',
89:'Gerhard explains that the Mediterranean has many countries built on maritime trade and that searching large cities such as Lisbon and Seville might lead to capable people. Preserve the places, regional cultural context and possibility, not guaranteed recruitment.',
92:'Hodram agrees and suggests extending their network of routes through Mediterranean towns along the way. This is prospective travel/trading-route planning, not a claim that every route is already established.',
},
45:{7:'The port worker says that the woman leading or associated with the Argot Company is waiting for Hodram in Amsterdam. The familiar姐さん is not an older sister relationship; the full B44/B137/B46 context binds the intended Lil reference. Do not change the destination or imply a completed meeting.'},
46:{
6:'Lil sharply calls for Hodram to wait.',
10:'Lil checks the report that he is the richest person in this region, then challenges him to a contest. Preserve the hearsay/question and financial comparison; do not change this to the strongest person, world dominance, or an agreed bet.',
14:'Hodram questions what she means by a contest.',
19:'Lil identifies what she indicates as a key for deciphering a map showing a treasure location and declares that whoever finds it first will be the dominant figure in the North Sea. The passage announces a contest; it does not explicitly say she hands over a new map, owns a Proof, or that he has already accepted or won. Bind the original4800/item/control consumer before naming the indicated object.',
23:'Lil insists on a serious contest without holding back and declares that she especially refuses to lose to him. Keep her competitive bravado without inventing hatred, romance, a military rank or a guaranteed future outcome.',
51:'Hodram privately or pensively questions what a map key is and what she means. Preserve the unexplained confusion; native presentation/control flow must establish its exact delivery before final English.',
},
}
if __name__=='__main__':
    assert not ROOT.exists();packets={b:read(p) for b,p in PACKETS.items()};names=read(NAMES)
    assert len(names['records'])==6 and {r['source_actor_ID'] for r in names['records']}=={1,2,9,16,18,113}
    assert len({p['source_ROM_sha256'] for p in packets.values()})==1
    ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath)
    assert ledger['records_editorially_completed']==7143 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    image=NdsImage.open('work/clean.nds');bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    callbacks=[]
    for family in ledger['completed_editorial_families']:
        for record in family['records']:
            if record.get('file_path',family.get('file_path'))!='/data/SC1.DK4' or record.get('block')!=44:continue
            source=record['source_reference'];at=source['offset'];raw=bytes.fromhex(record['source_hex'])
            assert bank[44][at:at+len(raw)]==raw and bank[44][at+len(raw)]==0
            callbacks.append(dict(id=record['id'],file_path='/data/SC1.DK4',block=44,source_reference=source,
                source_hex=raw.hex(),source_Japanese=record['source_Japanese'],already_completed_family=family['id'],
                source_only_reuse_no_current_English_consulted_no_duplicate_credit=True))
    assert len(callbacks)==27
    rows=[]
    for block in [137,45,46]:
        packet=packets[block];g=packet['groups'][0]
        assert g['block']==block and not packet['inventory_failures'] and not g['completed_coverage_overlap']
        assert set(GLOSSES[block])=={r['source_record_index'] for r in g['records']}
        for i,r in enumerate(g['records']):
            rows.append(dict(**r,first_clean_source_gloss=GLOSSES[block][r['source_record_index']],
                previous_physical_source_ID=None if i==0 else g['records'][i-1]['id'],next_physical_source_ID=None if i+1==len(g['records']) else g['records'][i+1]['id'],
                physical_neighbors_not_yet_proved_actual_path=True,current_English_body_not_yet_consulted=True))
    assert len(rows)==28 and sum(r['block']==137 for r in rows)==21 and sum(r['block']==45 for r in rows)==1 and sum(r['block']==46 for r in rows)==6
    assert not any(m in r['source_Japanese'] for r in rows for m in ['FI','FA','FO'])
    events={b:packets[b]['groups'][0]['source_event_records'][0] for b in PACKETS}
    assert events[137]['must_be_completed']==[44] and events[45]['must_not_be_completed']==[46] and events[46]['must_be_completed']==[137,45]
    ROOT.mkdir(parents=True)
    save(ROOT/'27_prior_clean_B44_source_refs_exact_no_new_credit.json',dict(records=callbacks,
        clean_SC1_block44_sha256=sha(bank[44]),complete_clean_prior_confrontation_context_bound=True,
        no_current_English_comparison_no_duplicate_credit=True,new_credit=0,full_goal_complete=False))
    save(ROOT/'28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json',dict(
        source_packets={str(b):dict(path=str(p),sha256=sha(p.read_bytes())) for b,p in PACKETS.items()},
        clean_names=str(NAMES),clean_names_sha256=sha(NAMES.read_bytes()),records=rows,source_events=events,
        source_macro_counts=dict(FI=0,FA=0,FO=0),
        explicit_event_graph='EV137 requires44;EV45 excludes46;EV46 requires137 and45. This doesnot prove a total chronological order,outer eligibility ornatural activation.',
        complete_exchange_progression='Camille apologizes for Lil after the earlier confrontation;Hodram acknowledges andreassures,thenplans fleetstaffing andMediterraneanroutes. The port worker conveys an Amsterdam invitation. Lil challenges reported regional wealth andproposes finding treasure first;Hodram remains puzzled about the map key.',
        source_only_no_current_body_orname_comparison_no_localized_manuscript=True,
        retain_approved_Hodram_Joakim_Camille_names_no_new_kinship_rank_romance_orhidden_identity=True,
        native_fullpreambles_FE_silences_4800_8000_relatives_effects_entry_names_items_fonts_actual_andrelease_pending=True,
        twentyseven_prior_B44_source_refs_reused_no_duplicate_credit=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*PACKETS.values(),NAMES,Path(__file__)]}))
    for r in callbacks:print('B44',r['id'],r['source_Japanese'].replace('\n',' / '))
    print('Saved28first clean glosses/six identities and27exact prior source callbacks. Native controls/items/getters/context/currentEnglish remainpending;zero credit.')
