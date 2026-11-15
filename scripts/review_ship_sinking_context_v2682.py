"""Fresh contextual retentions of sixteen named-vessel sinking announcements."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.ship_sinking_native_plan_v1330 import compiled,PROFILE
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_sinking_editorial_v2682')
PACKET=Path('work/analysis/ship_sinking_context_v2681/all16_clean_current_context_catalog.json')
OUT=Path('translations/ship_sinking_contextual_editorial_manuscript_v1.json')
NOTES={
2058:('Admiral,the named ship has sunk!','Retain the clear professional announcement and explicit Admiral address. The original ship name remains the only runtime substitution. Has sunk states the completed sinking without inventing crew deaths,an attacker or defeat of the entire fleet.'),
2059:('Admiral,the named ship is going under.','Retain is going under and the distressed trailing pause. The source 沈んでいきます describes the ongoing sinking,so it must not become the completed has sunk used in other variants. The named vessel is not arbitrarily called our flagship or an enemy ship.'),
2060:('Admiral,the named ship has sunk,an excited familiar report!','Retain the complete familiar report and address. The source emphatic よっ carries urgency in the exclamation;no invented child age,dialect,relationship or crew fate is needed.'),
2061:('Admiral,the named ship was sunk!','Retain the passive was sunk for 撃沈された. It distinguishes a vessel sunk by hostile action from the neutral has sunk reports without naming a weapon,attacker or casualties. The feminine ending does not require an artificial gendered English dialect.'),
2062:('Admiral,the named ship was sunk!','Retain the terse urgent passive report. It preserves the source explicit address and sunk-by-action wording;the English stays focused on the named vessel without adding blame,weapon details or a fleet-wide result.'),
2063:('Admiral,the named ship was sunk,an emphatic older-style report!','Retain the passive result and explicit address. The older familiar ending is carried by emphatic delivery without manufactured antique English,kinship or a new rank. No crew-death statement is added.'),
2064:('Admiral,the named ship sank!','Retain the short emotional sank report. The drawn-out source dismay is naturally conveyed by the exclamation without inventing a speaker age or relationship. It does not claim that every ship or crew member was lost.'),
2065:('Admiral,the named ship has sunk,a polite emphatic announcement!','Retain the measured completed-action report. Its explicit Admiral and the source vessel name remain complete;the polite emphasis needs no invented title,archaic tag or extra outcome.'),
2066:('We have sunk the named enemy ship!','Retain the complete passive English report. The original firing-ship context establishes our side action,so passive sentence order does not change the event. Enemy ship and the whole name remain explicit;no whole-fleet victory or crew fate is added.'),
2067:('Named enemy ship sunk!','Retain the concise conventional battle callout. The Japanese is itself a short excited announcement;the fragment is natural here. It identifies the enemy vessel and completed sinking without invented details.'),
2068:('Admiral! We have sunk the named enemy ship!','Retain the explicit Admiral address and enthusiastic sent to the bottom idiom. This naturally conveys the successful sinking in the original projectile-hit context. The bottom refers to the vessel;it does not claim the crew died or the battle has ended.'),
2069:('We have sunk the named enemy ship!','Retain the clear completed sinking announcement. Passive English changes sentence order,not the source action or its target. The source feminine ending does not justify a gendered English dialect,new relationship or rank.'),
2070:('We did it! The named enemy ship is sunk!','Retain We did it and has gone down to preserve the rough triumphant voice and completed enemy sinking. Gone down is ordinary nautical English. The celebration does not become a claim of total victory or the enemy crew deaths.'),
2071:('We have sunk the named enemy ship,an emphatic older-style report!','Retain the natural complete report and named enemy vessel. The original caller supplies our action;the English passive needs no forced old-fashioned dialect,kinship,rank or extra casualty statement.'),
2072:('The named enemy ship is sunk,a familiar excited report!','Retain the short excited has gone down announcement. It expresses sinking naturally and keeps the enemy identification and whole runtime name. It does not add an Admiral address absent from this variant.'),
2073:('We have sunk the named enemy ship,a polite emphatic report!','Retain the composed complete sinking report. The confident polite delivery is natural without an invented Admiral address,rank or archaic ending. The named ship remains the target;the whole enemy fleet and crew fate are not asserted.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    packet=read(PACKET);owner=packet['registered_prose_owner_binding'];prior={r['message_id']:r for r in read(owner['manuscript'])['records']}
    cp=Path(packet['source_context']);context=read(cp);rows=[]
    for s in packet['records']:
        n=s['message_ID'];r=deepcopy(prior[n]);assert r['source_hex']==s['source_hex'] and compiled(r).hex()==s['current_hex']
        gloss,note=NOTES[n]
        r['historical_source_prose_predecessor_fields']={k:r[k] for k in ['current_reference','current_text_hex','current_English'] if k in r}
        r.update(file_path='/COMMON/MESFILE.DK4',source_reference=s['source_reference'],current_reference=s['current_reference'],
            current_hex=s['current_hex'],current_text_hex=s['current_hex'],current_stored_English=s['current_stored_English'],
            current_English=s['current_stored_English'][1:],source_Japanese=s['clean_Japanese'],source_meaning=gloss,localization_note=note,
            historical_editorial_decision=prior[n]['editorial_decision'],editorial_decision='retain-wording',
            fresh_retained_wording_justification=note,context=r['context']+' Fresh source/provider context: '+context['scope'],
            registered_prose_owner=owner['stage'],registered_manuscript=owner['manuscript'],registered_compiler=owner['compiler'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        rows.append(r)
    ROOT.mkdir(parents=True);ordinary=ROOT/'complete_event_context.json'
    save(ordinary,dict(storage_neighbors=packet['neighbors'],context_only_no_extra_credit=True,
        own_or_source_side_report='Original active-mobile loop,Hull-zero and side predicate precede role1 reports2058-2065;flagship outcomes are processed separately. Preserve ongoing2059versus completed reports and do not add ship ownership where the source omits it.',
        enemy_projectile_report='Original positive-to-zero Hull transition and firing/target side predicates precede direct-actor reports2066-2073. The source virtual getter supplies the target name and55DC4 supplies the speaker. These are alternatives,not dialogue replies.',
        historical_pilots='Earlier gunnery attempts without sinking notices are nonactivation evidence only;no sinking credit may be inferred from a stale message buffer.',
        full_goal_complete=False))
    save(OUT,dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        consumer_layout_profile=PROFILE,review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',
        source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
        current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
        source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof=str(cp),native_context_proof_sha256=sha(cp.read_bytes()),
        fresh_ordinary_supplement=str(ordinary),fresh_ordinary_supplement_sha256=sha(ordinary.read_bytes()),registered_prose_owner_bindings=[owner],
        prior_manuscripts=[dict(path=owner['manuscript'],sha256=owner['manuscript_sha256'])],revised_IDs=[],retained_count=16,
        formatting_review_pending=True,current_native_and_representative_reconciliation_pending=True,records=rows,
        completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False))
    save(ROOT/'fresh16_editorial_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        new_individual_glosses_and_retention_reasons=16,new_prose_revisions=0,native_and_representative_completion_pending=True,
        completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('16sinking reports freshly reread andindividually retained;progressive2059,passive/active results andvoice distinctions preserved. Native/representative reconciliation pending.')
