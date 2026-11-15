"""Fresh whole-exchange clean-Japanese glosses before B47 current English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_clean_gloss_v7973')
SOURCE=Path('work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B47_clean_context_v7972/complete_clean_SC0_B37_EV0_andcoverage_before_current_English.json')
GLOSSES={
    5:"Speaker06 says Hayreddin's real intentions are still unclear, but this should make travel through the Mediterranean manageable. Cautious practical relief, not certainty about trust, friendship, alliance, or unrestricted trading rights.",
    17:"Speaker04 agrees: if pirates like those attacked every time they entered the Mediterranean, no number of lives would be enough. Preserve the conversational hyperbole and reference to repeated danger, without literal extra lives or a new pirate identity.",
    44:"Speaker06 cautions against approaching the Ottoman side because the risk is too great. Preserve the warning and its political target; do not turn it into an absolute inability to enter all Mediterranean ports.",
    48:"Rafael asks why. A brief sincere question that invites the elder speaker's explanation; no invented family address or rank.",
    53:"Speaker06 explains that roughly the eastern half of the Mediterranean is now Ottoman territory, meaning the domain of Pasha's forces. If they were targeted, they would almost certainly be unable to win. Preserve roughly, the eastern-half scope, the identification of the forces, and the conditional warning.",
    63:"Rafael draws the practical conclusion that they should leave the Mediterranean, which is strongly influenced by the Ottoman Pasha forces, until later. This is one stored alternative; its exact condition and exclusivity remain unproved until native branch mapping.",
    70:"The other stored Rafael alternative says they should leave the Mediterranean until later because of the strong influence of both Spain's Valdes forces and the Ottoman Pasha forces. Preserve both powers; do not merge this with the Ottoman-only alternative or assume which one actually runs.",
    77:"Speaker06 says there is no need to force a trading contract and that avoiding needless provocation is the wiser course. Preserve the practical advice and local contract context, not a universal ban on all contracts or an instruction to pay a bribe.",
    81:"Speaker06 qualifies the advice: large cities may have capable navigators, so they cannot simply ignore them. They should at least visit to look for companions. Preserve may and the limited purpose, without guaranteeing recruitment or equating every city with an available recruit.",
    92:"Speaker04 calls that a wise course. Brief measured approval of the preceding qualified plan, not praise for a trading conquest or a new promise.",
    102:"Speaker05 agrees: if they are to venture into other sea regions, they need to strengthen their ships and, of course, train themselves too. Preserve the conditional plan and both ship and personal preparation.",
    106:"Speaker06 agrees and repeats the reminder to visit large cities and gather navigators. Keep the reminder connected to the earlier exception for seeking companions, without adding a list of recruit names or a compulsory route.",
    110:"Rafael reacts to how much there is to do. Youthful, slightly overwhelmed realization within a practical planning exchange, not despair or a claim that all preparations are already finished.",
    122:"Speaker04 notes that things are getting busy. A polite, lightly wry transition from advice to the work ahead; precise personality and localized name still require clean identity/getter review.",
    129:"Rafael resolves to give it his best. Short energetic shared resolve after being overwhelmed, without a newly invented ambition, conquest, title, or destination.",
}
EXCHANGE="""B47's original EV0 event47/category5/action48 requires event37. Event37/category3/action38 selects the complete B37 exchange and requires event36. These are original source dependencies; block adjacency does not prove chronology, current location, all outer conditions, or natural gameplay activation.

The complete clean B37 context contains 72 stored speech objects and 120 commands. Rafael considers common opposition to Spain, faces the Algiers pirates, and follows advice to stand his ground. His bold and initially comic declaration develops into a risky challenge to become strong enough to face Hayreddin and Spain's formidable fleet. Hayreddin grants passage through the Mediterranean while telling the youths to trade in other regions, warns about the Spanish Valdes and Ottoman powers, offers possible assistance against Spanish attacks only in his own waters without guaranteeing it, and forbids interference in his territory. The youths reflect on the daring bargain and the need to grow stronger. These summarize the stored whole source exchange, not a newly verified complete branch playthrough, universal alliance, free trading treaty, guaranteed protection, or a new completion credit for B37.

B47 moves from guarded relief about Mediterranean passage to caution about the Ottoman side, an explanation of Pasha's territorial strength, and Rafael's conclusion that the region should wait. Two stored alternatives mention either the Ottoman forces alone or both Valdes and the Ottoman forces. Exact native predicates, relative spans, branch composition and observed selection are still pending. Next comes advice to avoid forcing trading contracts or provoking those powers, qualified by a reason to visit large cities anyway: they may have skilled navigators to recruit. Ship improvements and personal training join that preparation. Rafael briefly feels the size of the task, a polite speaker remarks on the work ahead, and Rafael ends with renewed resolve.

Preserve that progression and every qualification. Do not invent kinship, ranks, relationships, a permanent alliance, guaranteed recruitment, a ban on all Mediterranean visits, an immediate destination, or a completed future ambition. Actor00 is Rafael and the source names Julio/Claudio in surrounding context; original source identity fields and native display consumers still need explicit binding for this batch, especially actor04. Use source selectors until that binding is approved. Ottoman and Spanish territorial/force references are source assertions, not independent historical claims."""
if __name__=='__main__':
    assert not ROOT.exists()
    source,context=map(read,[SOURCE,CONTEXT]);group=source['groups'][0];prerequisite=context['groups'][0]
    assert not source['inventory_failures'] and not context['inventory_failures']
    assert group['block']==47 and len(group['records'])==15 and len(group['commands'])==48 and group['completed_coverage_overlap']==0
    assert prerequisite['block']==37 and len(prerequisite['records'])==72 and len(prerequisite['commands'])==120
    assert len(group['source_event_records'])==1 and group['source_event_records'][0]['must_be_completed']==[37]
    assert set(GLOSSES)=={r['source_record_index'] for r in group['records']}
    rows=[]
    for original in group['records']:
        assert original['current_English_body_unread'] and original['source_Japanese'] and not original['source_decode_error']
        row=deepcopy(original)
        row.update(source_gloss=GLOSSES[row['source_record_index']],full_clean_exchange_context=EXCHANGE,
            source_gloss_mode='fresh-clean-Japanese-whole-exchange-with-complete-clean-prerequisite',
            source_gloss_not_current_English_derived=True,whole_source_exchange_andoriginal_prerequisite_reread=True,
            source_native_names_roles_controls_display_andcurrent_comparison_pending=True,
            native_branch_composition_ofstored_alternatives_pending=True,new_source_prose_orcompletion_credit=0)
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'15_fresh_clean_glosses_complete_B37_context_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        prerequisite_context=str(CONTEXT),prerequisite_context_sha256=sha(CONTEXT.read_bytes()),
        file_path='/data/SC0.DK4',block=47,records=rows,complete_source_exchange_context=EXCHANGE,
        source_objects=15,source_commands=48,prerequisite_context_only_speeches=72,
        all15_glosses_fresh_before_current_English_exposure=True,
        all48_controls_relative_predicates_names_native_display_current_comparison_actual_andrelease_pending=True,
        two_stored_Rafael_alternatives_not_assumed_both_spoken_oractual_selected=True,
        B37_context_not_editorial_completion_oractual_gameplay_credit=True,
        no_ROM_registry_ledger_orcompletion_mutation=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXT,Path(__file__)]},full_goal_complete=False))
    print('15 fresh clean B47 glosses aftercomplete72-speech B37 context;current English remains unread.Native names/branches/current comparison/display/actual/release pending;zero credit.')
