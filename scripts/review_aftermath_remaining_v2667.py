"""Fresh full-event review of34 incomplete aftermath records;one tone revision."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled

ROOT=Path('work/analysis/aftermath_remaining_editorial_v2667')
PACKET=Path('work/analysis/aftermath_remaining_context_v2666b/all34_clean_current_context_catalog.json')
OUT=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v1.json')
NOTES={
1994:('The named town has surrendered.','Retain the clear completed-action report. The original argument is the complete CTown name,not a ship or faction. It follows the representative white-flag reply when a physical First Mate participates;the original empty-duty path has only this fallback report. No capture,casualties or permanent ownership terms are invented.'),
1995:('Admiral! The named town has surrendered!','Retain the excited report and explicit Admiral address. Moving the address to the end is natural English and preserves both facts and the familiar emphatic delivery. The whole native town name remains intact.'),
1996:('The named town has surrendered,a rough familiar report.','Given up is natural informal surrender language within the complete demand/white-flag/report event. It preserves the named town and rough voice without inventing an old dialect,new rank or relationship.'),
1997:('The named town has surrendered,an emphatic older-style announcement.','Retain the concise natural surrender announcement. The emphatic delivery does not justify invented age,kinship or antique English. No additional battle result is supplied.'),
1998:('I hear the named town says it wants to surrender.','Retain They say and wants to surrender:ってさ reports a wish rather than turning it into a completed-action claim. They is ordinary report framing,not a new named messenger. The town name is the runtime argument;the source variant remains tentative within the larger surrender event.'),
1999:('The named town has surrendered,a polite emphatic announcement.','Retain the complete,measured report. The polite emphasis works without an invented Admiral address,title or forced archaic ending. Preserve the whole source-provided town label.'),
2000:('We have defeated the enemy flagship.','Retain the clear flagship-destruction report in the original enemy-defeat outcome context. 撃破 identifies defeat of the vessel;destroyed is a conventional naval report here. It does not assert crew deaths or the destruction of an entire fleet. Do not replace it with captured,the distinct mode0 outcome.'),
2001:('Enemy flagship defeated!','Retain the short conventional battle callout. The flagship is explicit and destroyed concerns the vessel,not the crew or every enemy ship. No separate sinking statement is added.'),
2002:('Enemy flagship defeated!','Retain the concise excited battle report. The source is itself a brief callout,so a fragment is natural in this immediate outcome. It keeps the exact flagship referent and does not invent casualties.'),
2003:('Enemy flagship defeated!','Retain the source-matched short callout. This voice has the same brief Japanese wording as the other terse alternatives;artificially different facts or extra boasting would distort it. Defeat of the vessel is separate from capture.'),
2004:('The enemy flagship has sunk!','Retain sank because this variant explicitly says 沈んじゃった. The familiar matter-of-fact report fits the source. No death of the enemy admiral or crew is implied as a stated fact.'),
2005:('We have defeated the enemy flagship,a polite emphatic report.','Retain the complete collective report and flagship. The confident polite voice works without an invented rank or archaic tag. Destroyed refers to the original vessel outcome,not total destruction of the fleet or its people.'),
2006:('Admiral,our flagship has been struck! We cannot stop the flooding anymore!','Retain both the explicit address and urgent uncontrolled flooding. Our identifies the original own-flagship branch. It does not prematurely announce sinking,abandonment or deaths;the following defeat report belongs to its own table.'),
2007:('Admiral,the flagship has been hit! We cannot stop the flooding!','Retain the urgent familiar wording and cannot stop the water coming in. This expresses 浸水 naturally without adding a pump failure,weapon type or casualty. The ship is not yet declared sunk in this line.'),
2008:('Admiral,this flagship is finished! The flooding will not stop!','Retain finished and uncontrolled flooding as the older familiar speaker fearful judgment. No invented kinship,age or extra technical damage is added. The judgment is not rewritten as an already completed sinking.'),
2009:('Admiral,it is hopeless! The water will not stop coming in!','Retain the panicked We are done for sentiment in its existing contraction and the water report. This preserves the frightened voice without assigning a child age. It does not assert that everyone has died.'),
2010:('Admiral,this flagship cannot hold out any longer! We cannot stop the flooding!','Retain the measured but urgent warning. Cannot hold out much longer is natural for the source imminent failure and keeps it distinct from an accomplished sinking. No repair equipment or additional damage is invented.'),
2022:('Further fighting is pointless. Please surrender without resistance.','Retain the complete courteous demand. Please surrender carries the appeal to comply willingly in natural American English without adding safe-conduct terms,prisoner promises or a new rank.'),
2023:('Further resistance is pointless. Surrender without resistance.','Retain the stern direct command. Resistance is useless is an idiomatic threat in this situation;the following Surrender supplies the explicit demand. No guarantee about consequences is invented.'),
2024:('There is no point fighting anymore! Please give up without resistance!','Retain the familiar urgent demand. Give up is natural surrender language in this exchange and the ongoing battle supplies the further-fighting context. No new insult or Admiral address is added.'),
2025:('Further resistance is pointless! Surrender without resistance!','Retain the assertive demand. The source feminine ending does not require an artificial gendered English dialect. Its command stays distinct from the polite Please of2022.'),
2026:('You have no chance of winning! Hurry up and surrender!','Retain You cannot win in its existing contraction and the rough impatient Surrender already. Already gives the original さっさと its impatient force without inventing threats about punishment or treatment.'),
2027:('Further resistance is pointless. Surrender obediently.','Retain the stern measured command. Resistance is useless and Surrender carry the original admonition without manufactured archaic English,age or kinship. No promise of lenient treatment is added.'),
2028:('There is no point fighting anymore! Just give up without resistance!','Retain the familiar emphatic request with anymore and Just surrender. It preserves the pleading insistence of してよ without inventing a relationship,child age or personal grievance.'),
2029:('You have no chance of winning now! You would do well to surrender as soon as possible!','Revise the bare second command to I suggest you surrender at once. The original するがよろしかろう is an emphatic courteous recommendation;the former Surrender at once flattened this voice into the same direct order as2023/2027. The new phrasing preserves urgency and the hopeless situation while restoring advisory formality. I is ordinary implicit speaker judgment,not an added named character,rank or relationship.'),
2030:('I cannot let any more of our people die for nothing. This ship will surrender.','Retain the personal refusal to sacrifice more people and the explicit ship surrender. This original ship captain or model spokesperson announces its own ship decision. More is in the source;do not invent numbers,names or deaths beyond that stated concern.'),
2031:('I cannot allow so many comrades to die in vain. There is no choice;we surrender.','Retain the serious refusal and reluctant decision. So many expresses the original 多く concern;we have no choice preserves やむをえん. It does not invent a personal friendship,rank or a count of casualties.'),
2032:('It is hopeless. Admiral,this ship is surrendering.','Retain the despair,explicit Admiral address and ship surrender. The trailing hesitation suits the source emotional decline. It is a ship decision,not a claim that the entire player fleet surrendered.'),
2033:('We cannot fight any longer. Admiral,this ship is surrendering.','Retain the exhausted opening and explicit ship decision. The original hesitation is conveyed naturally by the pause in the English paragraph,without carrying Japanese vertical staging into authored layout. No crew-death claim is added.'),
2034:('It does not look as though we can win by fighting on. Admiral,this ship will surrender.','Retain the familiar pessimistic We are not going to win this sentiment in its existing contraction and the explicit ship surrender. In this ongoing losing fight it naturally expresses 勝てそうにねえ without inventing a new battle result or expanding surrender to every ship.'),
2035:('We cannot waste any more of our people lives. We surrender.','Retain the refusal to sacrifice more people and reluctant surrender. The English idiom die for nothing preserves the concern about wasted lives without inventing casualty counts. No Admiral address is added where absent.'),
2036:('It is hopeless;everyone will be defeated. I am sorry,I am surrendering.','Retain the panic,prospective danger and apology. They are going to get us all in its existing contraction preserves the fear without falsely stating everyone is already dead. We are surrendering this ship makes the original ship-spokesperson decision explicit in context;it does not surrender the entire fleet or invent a child age.'),
2037:('Knowing when to withdraw is important. Admiral,this ship is surrendering.','Retain the composed observation about knowing when to stand down and the explicit ship decision. This preserves the polite resigned voice without inventing a strategic victory,new title or moral lecture. The source leading pause need not become a leading blank row.'),
2192:('There is no alternative. Raise the white flag.','Retain the resigned acceptance and concrete white-flag order. The original town representative speaks between the member demand and town-name report. The line adds no terms of surrender,ownership deal,kinship or new rank.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    packet=read(PACKET);owner=packet['registered_prose_owner_binding'];prior={r['message_id']:r for r in read(owner['manuscript'])['records']}
    cp=Path(packet['source_context']);context=read(cp);rows=[]
    assert set(NOTES)==set(packet['selected_IDs'])
    for source in packet['records']:
        n=source['message_ID'];row=deepcopy(prior[n]);assert row['source_hex']==source['source_hex'] and compiled(row).hex()==source['current_hex']
        gloss,note=NOTES[n]
        if n==2029:row['english']='You cannot win! I suggest you surrender at once!'
        row.update(file_path='/COMMON/MESFILE.DK4',source_reference=source['source_reference'],current_reference=source['current_reference'],
            current_hex=source['current_hex'],current_stored_English=source['current_stored_English'],
            source_Japanese=source['clean_Japanese'],source_meaning=gloss,localization_note=note,
            fresh_retained_wording_justification=note if n!=2029 else None,
            editorial_decision='revise' if n==2029 else 'retain-wording',
            historical_editorial_decision=prior[n]['editorial_decision'],
            registered_prose_owner=owner['stage'],registered_manuscript=owner['manuscript'],registered_compiler=owner['compiler'],
            context=row['context']+' Fresh source/current proof: '+str(cp)+'. '+context['scope'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        row['proposed_compiled_hex']=compiled(row).hex()
        if n!=2029:assert row['proposed_compiled_hex']==row['current_hex']
        else:assert row['proposed_compiled_hex']!=row['current_hex']
        # Old case-bound formatting waivers are historical evidence only and
        # are re-evaluated against the current native matrix before approval.
        row['historical_formatting_waivers']={k:row[k] for k in ['qa_waivers','qa_waiver_reason','case_bound_qa_waivers'] if k in row}
        for key in ['qa_waivers','qa_waiver_reason','case_bound_qa_waivers']:row.pop(key,None)
        rows.append(row)
    ROOT.mkdir(parents=True)
    ordinary=ROOT/'complete_event_context.json';save(ordinary,dict(storage_neighbors=packet['neighbors'],
        context_only_no_extra_credit=True,separate_event_families_not_one34line_conversation=True,
        town_three_turn_exchange='Assigned physical First Mate demands surrender;original town representative orders the white flag;the member reports the named town surrender. Empty-duty fallback has only the report.',
        flagship_defeat_and_flooding='Separate original result selectors;flooding is followed by the already-reviewed flagship-defeat family. Do not infer every defeat means sinking or death.',
        ship_surrender='Original flagship captain or ship-model spokesperson announces its own ship surrender before the original status change. Different voice alternatives are not replies to each other.',
        broader_story_random_shared_and_player_prose_still_in_scope=True,full_goal_complete=False))
    save(OUT,dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',consumer_layout_profile='battle-aftermath-portrait-postmacro-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',
        source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
        current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
        source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof=str(cp),native_context_proof_sha256=sha(cp.read_bytes()),
        fresh_ordinary_supplement=str(ordinary),fresh_ordinary_supplement_sha256=sha(ordinary.read_bytes()),registered_prose_owner_bindings=[owner],
        prior_manuscripts=[dict(path=owner['manuscript'],sha256=owner['manuscript_sha256'])],revised_IDs=[2029],retained_count=33,
        formatting_review_pending=True,current_native_and_representative_reconciliation_pending=True,registered_revision_integration_pending=True,
        records=rows,completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False))
    save(ROOT/'fresh34_editorial_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        fresh_individual_glosses_and_reasons=34,proposed_prose_revision_IDs=[2029],justified_retentions=33,
        native_formatting_representative_scope_and_registered_integration_pending=True,
        completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('34fresh individual contextual reviews:33retentions and2029advisory-tone revision. Native/release completion pending;zero completion credit.')
