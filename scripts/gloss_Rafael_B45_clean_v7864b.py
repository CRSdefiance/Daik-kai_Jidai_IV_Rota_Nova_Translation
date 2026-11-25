"""Fresh complete Japanese exchange gloss before any current B45 English is read."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_clean_gloss_v7864b')
SOURCE=Path('work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json')
GLOSSES={
5:"Rafael notices Julio is missing and wonders where he went. The polite name suffix does not establish family,rank or a formal title.",
9:"The companion calls from a short distance that he is right here. The repeated call and old-fashioned Japanese voice make the response lively and reassuring.",
13:"Rafael realizes the companion is at the trade house/trading facility. Keep this facility distinct from ordinary retail food or liquor shops;final approved English UI terminology still needs binding.",
18:"As a first step,the companion suggests trying to sell trade goods here. If Rafael has something bought in Lisbon,he may try selling that. The trailing but leads into the next speech's condition;do not imply he must possess cargo or sell all of it.",
21:"To sell here,an agreement is necessary. In the following explanation this means securing the local right to trade,not an ordinary sales contract with a buyer.",
24:"Rafael politely repeats agreement as a question,showing that this is new to him. Do not turn his uncertainty into fear,insolence or an already completed transaction.",
29:"Go to a palace or governor's office,pay the agreement fee to the ruler who governs that town,and obtain the right to trade. Preserve both types of office,the local scope,payment and permission;no precise fee or extra legal condition is supplied.",
33:"The companion recommends arranging such agreements in various towns. Early on,paying the minimum agreement amount should be sufficient. Keep that early-stage qualification and avoid promising a permanently optimal fee or fixed market-share benefit.",
37:"The companion says he has already taken care of the agreement with Ceuta,but Rafael should handle the next ones himself. This refers to Ceuta specifically;it does not establish a family relationship,new rank or a universal exemption.",
52:"The information panel states that FO's market share in Ceuta is20percent and that trading can be conducted according to that share. Preserve the exact city,20percent and the original FO company substitution. This is local trading share,not ownership of the company;the wording does not itself give a precise transaction formula or demonstrate every mechanic.",
58:"The companion says that if Rafael has anything he wants to sell,he should go ahead and sell it. Preserve the conditional choice;do not turn it into an order to liquidate all cargo or invent a deadline.",
61:"Rafael politely agrees to do that. He is accepting the advice,not reporting that a sale or profit has already happened.",
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['source_only_no_current_English_exposed_orused'] and not source['inventory_failures']
    group=source['groups'][0];assert group['block']==45 and group['physical_speech_objects']==12 and group['completed_coverage_overlap']==0
    records=[]
    for original in group['records']:
        row=deepcopy(original);index=row['source_record_index'];assert index in GLOSSES and row['source_decode_error'] is None
        row.update(fresh_clean_source_gloss=GLOSSES[index],
            full_source_exchange_context='A novice asks where his companion went;the companion explains selling trade goods,local agreements andfees,Ceuta arrangements andmarket share,then invites an optional sale. Original branches anddisplay consumers still need binding before treating the12 stored speeches asone actually executed path.',
            source_gloss_not_derived_from_current_English=True,
            review=dict(source=True,context=False,localization=False,naturalness=False,formatting=False),
            kind='system-FE-distinct-consumer-pending' if row['source_selector']==254 else 'progressive-speaker-consumer-pending',
            current_English_body_unread=True,new_credit=0)
        records.append(row)
    assert len(records)==len(GLOSSES)==12 and {r['source_selector'] for r in records}=={0,6,254}
    assert sum(bytes.fromhex(r['source_hex'])[1:].count(b'FO') for r in records)==1
    assert all(not any(m in bytes.fromhex(r['source_hex'])[1:] for m in [b'FI',b'FA']) for r in records)
    ROOT.mkdir(parents=True);save(ROOT/'twelve_fresh_clean_exchange_glosses_before_current_English.json',dict(
        file_path='/data/SC0.DK4',route=0,route_identity='Rafael',block=45,records=records,
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        clean_block_sha256=group['clean_block_sha256'],source_event_records=deepcopy(group['source_event_records']),
        all12_complete_clean_Japanese_speeches_read_before_current_English=True,
        source_controls_stored_paths_not_assumed_all_executed_in_one_natural_scene=True,
        source_event45_action46_has_no_explicit_requires_or_excludes_but_outer_conditions_remain_unreviewed=True,
        opening44_to45_immediate_chronology_oractivation_not_proved=True,
        actor0_Rafael_actor6_Julio_source_mention_native_names_androles_still_require_binding=True,
        original_source_macros=dict(FI=0,FA=0,FO=1),
        one_FE_information_panel_and20percent_runtime_formatting_need_distinct_native_checks=True,
        no_current_English_comparison_localized_manuscript_orcomplete_prose_approval=True,
        source_names_macros_branches_controls_current_consumers_actual_display_andrelease_pending=True,
        new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    print('Rafael B45:12 complete clean-source glosses before current English;actor0/6 andone FE panel,FO1. Branches/names/native consumers/current comparison pending;zero credit.')
