"""Complete first-source gloss; this is not an English manuscript or credited review."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_clean_gloss_v8075')
SOURCE=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json')
GLOSSES={
5:'Rafael hears a commotion over at the trade house and decides to investigate.',
12:'Lil sharply calls out to him: hey, you.',
15:'Camille calls Lil by name and objects that she must not start a fight.',
20:'Lil insists that matters like this must be stated clearly and tells Camille to keep quiet.',
32:'Janus wonders what is happening and remarks on the strangely hostile atmosphere.',
38:'Rafael asks whether she needs something from him.',
43:'Lil incredulously repeats his question, then demands whose permission they obtained to do business in the North Sea.',
47:'Claudio confronts her with blustering menace: what is she talking about, and is she trying to make them angry? The familiar older-man self-reference does not establish brothers or kinship.',
51:'Rafael hesitantly apologizes and says he has not quite grasped the situation.',
55:'Lil bluntly asks whether he is an idiot.',
67:'Janus laughs lightly and calls that a harsh assessment.',
74:'Lil says she will explain only once and orders him to listen carefully.',
77:'Rafael gives an absent or mild yes, all right.',
82:'Lil explains that people everywhere are working to make money, and this sea region is no exception.',
86:'Camille urges her to put it more tactfully.',
90:'Lil refuses the correction and asserts that this area is Argot company territory; she asks whether he understands. Her claim belongs to her confrontational argument, not an independent ownership finding.',
93:'Rafael responds with a hesitant acknowledgment.',
98:'Lil questions whether this man is all right and whether he really is an admiral, expressing disbelief at his demeanor.',
107:'Claudio pauses, then confirms that this is so.',
112:'Janus emphatically and politely confirms that Rafael is a fine admiral. The exaggerated phrasing can sound wry in this exchange; it does not prove hidden contempt.',
118:'Lil says this has taken the wind out of her sails or been an anticlimax.',
122:'Lil decides that they apparently are not bad people and offers to explain the situation.',
126:'She points out that the North Sea covers a fairly large area.',
129:'Claudio agrees with that observation.',
142:'Lil describes the northern area as the haunt of a navy man named Hodram Bel... something, for the time being. The forgotten surname fragment and present-tense qualification are intentional; the familiar older-man term is not an uncle relationship.',
158:'She says the admiral called Clifford is in charge around イギリス. Review the established geographical consumer before choosing England or Britain; do not silently enlarge the region.',
175:'Around Germany, Martin シュパイヤー of the Hanseatic League is, in her casual estimation, somehow keeping things running.',
183:'Lil would like her company to acquire most of the remaining areas from now on. This is a prospective ambition, not already established control.',
187:'Rafael asks whether trade is fair or equally open once one contracts with a town. This is his question about the situation, not a new unconditional gameplay guarantee.',
192:'Lil says she already understands that; what she wants is to be left alone for a while.',
196:'Claudio calls that a very self-serving request.',
200:'Rafael hesitates and says that is a little difficult.',
205:'Lil asks whether they are, after all, aiming at the world.',
208:'Rafael readily confirms that they are.',
213:'Lil complains that his response is deflating.',
225:'Janus says they certainly do have ambitions or a goal.',
238:'In one source branch, Lil suggests going to Africa or the New World to the west instead.',
244:'In the alternative source branch, she stresses how large the world is and suggests the western New World or solving the mysteries of the far East. Branch selection must be proved before treating this as one spoken sequence.',
250:'Rafael acknowledges that this is one way of looking at it.',
255:'Lil returns to her point: leave her company alone for a while.',
259:'If they insist on direct competition, that is another matter, but she has plans of her own in that case. She asks whether he understands; do not invent a specific attack, military guarantee or perpetual trading ban.',
262:'Camille tries to rein Lil in again.',
266:'Rafael says he more or less understands and gently identifies her intent as seeking an agreement with them. 協定 must be reviewed against the actual pact/mechanic; it does not by itself prove a formal alliance.',
271:'Lil is flustered that he is perceptive about this and objects that his phrasing makes her seem to be approaching them from the weaker position.',
275:'Rafael chuckles and observes that she hates to lose or is very competitive.',
279:'Lil asks whether he is making fun of her.',
283:'Rafael politely denies it.',
296:'Arcadius quietly chuckles.',
311:'Julio sighs and addresses FI, suggesting that it might be wiser to go earn money in other regions. Preserve the substitution and the tentative strategic advice.',
328:'Lil asks whether the Spanish Valdes is their enemy.',
331:'Rafael considers this, says Spain is targeting Portuguese territory, and concludes that they are indeed enemies.',
336:'Lil seizes on their common enemy as a reason not to fight here, affirming her own argument. No signed alliance or new relationship follows solely from this statement.',
343:'Rafael gives another hesitant acknowledgment.',
356:'Janus sums up her meaning as telling them to try somewhere else.',
363:'Lil briskly concludes the matter, asks whether they understand, says her company is busy and leaves.',
367:'Camille calls for Lil to wait, apologizes for the disturbance, excuses the departure and calls after Lil again.',
381:'Arcadius dryly compares the aftermath to a storm having passed. Preserve the metaphor and humor without inventing a weather event.',
388:'Claudio says he dislikes this but leaves the decision to FI and will follow that decision. Preserve the substitution and his grudging loyalty.',
392:'Rafael decides to leave this sea region until later. He cannot really dislike Lil, and jokes that she seems frightening when angry. Do not add romance or a binding promise absent from the source.',
405:'Arcadius qualifies the decision as sensible provided the North Sea is not the only region they have left. This is conditional, not a declaration that it is the last region.',
409:'Rafael proposes heading for another sea region for the time being.',
}
if __name__=='__main__':
    assert not ROOT.exists();source,names=map(read,[SOURCE,NAMES]);g=source['groups'][0]
    assert len(g['records'])==len(GLOSSES)==61 and {r['source_record_index'] for r in g['records']}==set(GLOSSES)
    assert len(names['records'])==7 and not g['completed_coverage_overlap'] and not source['inventory_failures']
    assert g['source_event_records'][0]['event_ID']==49
    rows=[]
    for i,r in enumerate(g['records']):
        rows.append(dict(**r,first_clean_source_gloss=GLOSSES[r['source_record_index']],
            previous_physical_source_ID=None if i==0 else g['records'][i-1]['id'],
            next_physical_source_ID=None if i+1==len(g['records']) else g['records'][i+1]['id'],
            physical_neighbors_not_assumed_simultaneous_spoken_path=True,current_English_body_andname_fields_still_unread=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'61_first_clean_glosses_seven_source_identities_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),clean_names=str(NAMES),clean_names_sha256=sha(NAMES.read_bytes()),
        records=rows,source_event_records=g['source_event_records'],source_event_anddependencies=g['source_event_anddependencies'],
        complete_exchange_progression='Trade-house commotion; Lil confrontation and Camille restraint; regional competition explanation; prospective territorial request; Rafael recognizes proposed agreement; shared Spanish enemy; abrupt departure and storm joke; qualified decision to sail elsewhere.',
        source_actors={str(r['source_actor_ID']):[v.get('text') for v in r['fields']] for r in names['records']},
        source_branch_pairs_to_verify=[[238,244]],
        source_EV49_requires39_excludes151_not_proof_ofnatural_activation=True,
        source_control_0xC281_native_extent_andparent_scope_requires_review=True,
        full_event39_context_native_entry_predicates_queries_paths_names_voices_current_comparison_andlocalized_manuscript_pending=True,
        unknown_pact_geography_andproper_name_consumers_not_invented_from_gloss=True,
        Camille_is_user_approved_given_name_no_invented_kinship_orbiography=True,
        current_English_never_exposed_for_this_batch=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,Path(__file__)]}))
    print('61 first clean glosses/seven original identities recorded;source branches/native context/prerequisite/current-English comparison pending. No manuscript orcredit.')
