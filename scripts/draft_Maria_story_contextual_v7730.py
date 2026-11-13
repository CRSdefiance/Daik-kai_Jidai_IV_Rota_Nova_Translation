"""Whole-arc decisions on67 speeches; native catalogue wording is the real predecessor."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_contextual_v7730')
SOURCE=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json')
NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
OUTPUT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v1.json')
NAME_OUTPUT=Path('translations/maria_B34_B108_B35_speaker_name_review_v1.json')
# None means retain the effective paragraph, including its established native I escape.
# Each reason is an individual contextual decision, not a generic retention label.
DECISIONS={
34:{
5:(None,"Retain the effective catalogue paragraph: it already restores famous FA, the gruff safety advice, Kuhn/Pereira and the risk of becoming involved. The shorter raw storage is not the shipped wording."),
10:("Whoever wins, it won't do us any good. What a pain... (Sigh.)","Restore the exasperated sigh and make the local speaker's lack of benefit conversational; the next speech explains exploitation rather than indifference to the outcome."),
13:(None,"Retain Maria's brief Why? It naturally asks why either side's victory does nothing for the locals and leaves the explanation to the next speaker."),
17:("They came from far away to expand their own countries. Whoever wins, they'll just take advantage of us. The locals won't gain a thing.","Restore distant foreign national expansion, local exploitation and no local benefit; replace the compressed lands/either victor phrasing with the port worker's direct speech."),
20:(None,"Retain Xien's reflective conclusion that neither side cares about the local people. It follows the explanation without inventing a policy, rank or family relationship."),
23:(None,"Retain Maria's single CP932 ellipsis as a thoughtful silence between the local explanation and the formal report; no spoken assent or resolve is inserted."),
34:("Portugal and the Netherlands... Both are looking to expand into East Asia.","Preserve the source Netherlands name and East Asia, and its expansion ambitions; seek control overstates the specific claim. Richard's measured report stays distinct from the port worker."),
42:("It looks like we'll need to act before any harm comes to our homeland.","Restore Maria's tentative assessment while preserving the preventive motive and prospective action; do not add a plan, alliance or battle."),
},
108:{
4:("Ugh... Uuugh... (Thud.)","Restore the weak groaning and explicit written collapse sound omitted by the short English. The parenthetical sound is source-supported, not an invented injury mechanism."),
14:(None,"Retain Xien's startled W-what!? as the source stammered reaction. Its conditional selection remains separate from the other reaction variants."),
20:("W-what!?","Restore Julian's stammer; preserve this brief alternative reaction without assuming it plays alongside Xien and Richard."),
34:(None,"Retain Richard's Someone collapsed! It states the observed event and alarm naturally without adding a diagnosis or an identity."),
43:("What's wrong?","Maria is concerned about the collapsed person; What now? can imply irritation rather than her question about what happened."),
47:(None,"Retain the injured man's H-help me... It preserves the stammer, urgency and unfinished breath before any explanation."),
51:("Those are some terrible injuries. What happened to you?","Keep Xien's severe assessment and concerned question while avoiding the compressed clinical wounds are grave."),
54:("Let's treat your wounds first. It may hurt, but try to bear it.","Restore Maria's care-first priority and polite request to endure pain, rather than the abrupt commands Treatment first/Bear the pain. No treatment method is invented."),
57:(None,"Retain Th-thanks... The injured man's weak gratitude is brief and appropriate after Maria offers care."),
61:("It looks like someone beat you. My name is FA. Would you mind telling me what happened?","Retain the effective catalogue's beating inference, FA introduction and voluntary question, while fixing the awkward These wounds look like someone beat you. Do not hardcode Maria's surname."),
64:("What! You're with FO... Then you'll believe me, won't you?","Restore the informant's hopeful appeal for belief after recognizing FO; the old categorical Then you will believe me changes the interpersonal uncertainty."),
68:("I... I used to work for Kuhn. But his dirty tricks started weighing on my conscience... I ended up helping the local people.","Restore first-person responsibility for helping residents and the moral discomfort that prompted it. Remove passive help went to the villagers and preserve a former worker without inventing rank or recruitment."),
71:("After that, they treated me like a traitor... I practically had to run away to get out.","Preserve the traitor treatment and flight from Kuhn's service in the speaker's own voice; remove the unnatural his service was abandoned without adding a new pursuit detail."),
75:("But how did you get hurt? This wasn't the work of some roadside thief, was it?","Xien asks how the injuries happened, then doubts an ordinary highway robbery explanation. The current who injured you asks for a culprit before the man's explanation."),
79:("Those injuries are clearly a professional's work... Do you know something about Kuhn he wants kept secret?","Keep Maria's inference of a professional attack and question about a dangerous secret. Professional wounds is not natural English; no weapon, assassin identity or technique is supplied."),
82:("You're sharp... I know what Kuhn's planning. If word got out, he'd be in real trouble.","Restore that this man knows Kuhn's plan and that disclosure would endanger Kuhn, in conversational speech; ruin is stronger than the source's trouble."),
85:("Kuhn's plan... No doubt something vile.","Retain Xien's compact suspicious judgment and pause; only correct the older Kuen spelling to the project-established Kuhn, without inventing the plan's contents."),
88:("…Tell me what he's planning. I guarantee your safety.","Make Maria the explicit speaker of the safety guarantee, preserving her deliberate promise rather than an impersonal guaranteed result. This promise is not verified game protection."),
92:("Thank you... Now that it's come to this, you're the only one I can turn to. So... have you heard of the Argot Company?","Preserve his present reliance on Maria and transition into the company question; No one else can help asserted more knowledge about all possible helpers."),
96:("There's a small company by that name around the North Sea. Their admiral is... Lil Argot, if I remember correctly.","Keep Xien's recalled small North Sea company and tentative admiral name; restore conversational recollection without implying the company is defunct."),
100:("Kuhn's using the Argot Company to stop FO from expanding into Southeast Asia.","State the reported active plan and diversion plainly; preserve FO and Southeast Asia instead of the stiff passive entry is being blocked."),
103:(None,"Retain Maria's How? It naturally asks how Kuhn is using the company and leads directly to the false-information explanation."),
107:("He fed the Argot Company false information, claiming FO was involved in dishonest trade.","Identify Kuhn's misinformation as the actor's report and the allegation as false. Do not assert actual wrongdoing or invent a commodity such as slaves, drugs or weapons."),
111:("They say the Argot Company's young leader has a strong sense of justice. I heard she was furious, saying she'd never forgive FO.","Restore both the reported young female leader's sense of justice and the secondhand account of her anger. Avoid turning a heated declaration into a newly invented sworn vow."),
114:("…While FO has its hands full with the Argot Company, it can't make a move into Southeast Asia. That's what Kuhn is counting on.","Make Xien's strategic inference and the diversion explicit; FO remains the company macro, not a guessed fixed name or a completed war."),
125:(None,"Retain Julian's That villain! It is a short angry moral reaction to the revealed deception, with no new threat, profanity or action."),
132:("But... that's a dangerous plan. If it ever came to light, Kuhn would face enemies on both sides.","Restore Maria's contrast and hypothetical exposure; Once exposed made disclosure sound inevitable. Preserve the two-sided danger without claiming a battle already occurred."),
136:("That's why he can't let anyone who knows the secret leave alive. If they find me... I'm dead.","Restore the causal link and conditional lethal risk; When found incorrectly assumes capture. The man's fear does not establish an executed assassination or game outcome."),
140:("The Argot Company, you said...? Does its leader seem to have caught on to his plan?","Restore Maria's confirming recall and question about signs of the leader's awareness; do not suggest knowing participation in the scheme."),
144:("That, I don't know...","Keep the man's admitted limit about the company's awareness, without making him claim total ignorance of the plan he has just explained."),
147:("FI, this sounds worth looking into.","Restore Xien's tentative recommendation to FI as a natural complete line, retaining the runtime given-name macro and no promised investigation result."),
},
35:{
6:("Excuse me. Forgive the sudden interruption...","Preserve Bergstrom's courteous unexpected approach in natural speech; This is sudden does not itself express the source apology."),
10:(None,"Retain Maria's direct Who are you? after the stranger's unexpected approach; the question is appropriately guarded without adding hostility."),
15:(None,"Retain the effective catalogue introduction as Bergstrom of the Swedish Navy and the question to the recently talked-about Admiral FA. The source supplies no new rank or full-name introduction."),
18:("…What if I am?","Restore Maria's guarded conditional response in idiomatic English, including the source hesitation, rather than Suppose so?"),
22:("I just want to see for myself whether you're our enemy.","Make Hodram's stated purpose a natural first-person reply. It is a question of possible enmity, not an already declared war."),
25:("Whether I'm your enemy... That's entirely up to you.","Preserve Maria's cool statement that his choices determine whether she is his enemy, replacing the abstract Our enmity."),
28:(None,"Retain Hodram's single CP932 ellipsis as the silent reaction to Maria's pointed reply; no threat, agreement or submission is supplied."),
32:("Then let me ask you something in return. You said you were with the Swedish navy. Do you know the Argot Company, up in the North Sea?","Restore Maria's reciprocal question and the North Sea link to Sweden; no family, formal alliance or precise current scene location is invented."),
36:("The Argot Company... I know of them.","Retain Hodram's guarded acknowledgment without the wooden They are known to me or a claim of intimate knowledge."),
40:("I'm sorry to interrupt... What about the Argot Company?","Keep Camille's polite, hesitant intervention and request to know what concerns the company; What happened to Argot overcommits the question to a particular mishap."),
43:(None,"Retain Maria's direct Who are you? for the new participant. The repeated question is motivated by a different arrival, not redundant prose to delete."),
47:(None,"Retain the effective catalogue's Camille introduction and explicit nonmembership in the fleet while accompanying it for an unspecified reason. It already avoids the old raw Kamil and invents no rank or relationship."),
51:("I know the Argot Company well... Would you mind telling me what's happened?","Make Camille's familiarity and polite request personal and natural, replacing the impersonal Argot is well known to me."),
54:("…It might be worth talking this over.","Maria tentatively judges the usefulness of discussing the situation, rather than judging Camille's personal worth as You may be worth telling suggests."),
58:("Kuhn and Pereira control Southeast Asia. It seems FO and the Argot Company have been caught up in their feud.","Restore the explicit regional context and Maria's apparent rather than certain conclusion about entanglement; preserve FO and both companies without inventing battle or alliance."),
61:("So... it was true.","Keep Camille's quiet confirmation of an existing suspicion, with the source pause before the realization rather than a new claim to know the whole plot."),
65:(None,"Retain Wait... You knew about this? Who exactly are you? Maria's sharper follow-up fits Camille's recognition while remaining a question, not a spy accusation."),
68:(None,"Retain the effective catalogue's young Argot member, closeness to its admiral and temporary separate travels. The exchange deliberately leaves the relationship unspecified; no romance, kinship, resignation or Swedish fleet membership is added."),
72:("Understood. Does Admiral Argot know that Kuhn is using her?","Retain Maria's acknowledgment and question about the admiral's knowledge; only correct Kuen to the project-established Kuhn. Knowing cooperation is not assumed."),
76:("I don't think she knows yet... Damn... So it really was true...","Restore Camille's belief that she still does not know and his frustrated realization; She may not know weakens the source's stated belief. The cause of his separation remains unstated."),
79:("So you don't know the whole story either. Kuhn's plot has brought FO and the Argot Company to the brink of a clash.","Preserve Maria's assessment of partial knowledge and impending conflict; nearly driven to war overstates the source clash. Keep the event prospective."),
83:(None,"Retain the effective catalogue's respectful Admiral FA, acknowledgment of the complicated situation and practical question about Maria's intended response; no superior rank or command is invented."),
87:(None,"Retain the effective catalogue's explicit direct conversation without an intermediary and polite request for Camille to guide her; this preserves Maria's purposeful tone without inventing an escort agreement."),
91:("I'm not sure I can... But Lil... I think she's staying somewhere around Batavia.","Preserve Camille's hesitation about guiding Maria and both uncertainty and approximation in Lil's whereabouts; should be staying suggests a stronger expectation than the source thinks."),
95:("Batavia... I'll try there, then. Thank you.","Preserve Maria's decision to try Batavia and her thanks. This is intended travel, not verified arrival or guaranteed presence of Lil."),
98:(None,"Retain the effective catalogue's gentle question about Camille going himself and the opportunity it presents. It supplies neither an order nor a reason for his separation from Lil."),
101:("…I'm sorry. I just can't see her right now...","Preserve Camille's apology, present inability to meet her and trailing hesitation; do not invent why, a breakup, betrayal or a future promise."),
104:("…All right. As you wish.","Keep Hodram's quiet acceptance and respect for Camille's choice, restoring the source pause and natural acknowledgment rather than a formal command response."),
},
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not NAME_OUTPUT.exists()
    source,effective,names=map(read,[SOURCE,EFFECTIVE,NAMES]);assert effective['source_packet_sha256']==sha(SOURCE.read_bytes())
    assert source['all67_clean_whole_context_glosses_precede_current_English_exposure']
    by={r['id']:r for r in effective['effective_current_records']};rows=[]
    for group in source['groups']:
        block=group['block'];assert set(DECISIONS[block])=={r['source_record_index'] for r in group['records']}
        for src in group['records']:
            old=by[src['id']];english,reason=DECISIONS[block][src['source_record_index']]
            retention=english is None;english=old['effective_predecessor_paragraph'].replace('Ｉ','I') if retention else english
            assert '\n' not in english and '\r' not in english and english.strip()==english and english
            for token in ['FI','FA','FO']:
                assert english.count(token)==bytes.fromhex(src['source_hex'])[1:].count(token.encode()),(src['id'],token)
            row=deepcopy(src);row.update(english=english,decision='retention' if retention else 'revision',decision_reason=reason,
                predecessor_effective_reference=deepcopy(old),effective_predecessor_paragraph=old['effective_predecessor_paragraph'],
                retained_native_fullwidth_I_escape_normalized_for_logical_prose_only=retention and 'Ｉ' in old['effective_predecessor_paragraph'],
                exact_macros_preserved=True,speaker_andcomplete_six_byte_preamble_preserved_forlater_compilation=True,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                formatting_native_stored_whole_VM_actual_production_registry_gates_pending=True,new_source_prose_orcompletion_credit=0)
            if retention:assert english==old['effective_predecessor_paragraph'].replace('Ｉ','I')
            else:assert english!=old['effective_predecessor_paragraph'].replace('Ｉ','I')
            rows.append(row)
    assert len(rows)==67
    dependencies={str(p):sha(p.read_bytes()) for p in [SOURCE,EFFECTIVE,NAMES,Path(__file__)]}
    doc=dict(format='dk4-contextual-editorial-manuscript-v1',file_path=source['file_path'],route=3,source_dependency_chain=[34,108,35],
        current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],current_ARM9_sha256=source['current_ARM9_sha256'],
        current_COMMON_sha256=source['current_COMMON_sha256'],records=rows,source_current_packet=str(SOURCE),effective_packet=str(EFFECTIVE),names_packet=str(NAMES),
        complete_clean_exchanges_glossed_before_current_English=True,reviewed_effective_catalogue_templates_notjust_raw_storage=True,
        exact_source_FA4_FO7_FI1_runtime_macros_preserved=True,all_English_logical_paragraphs_without_manual_linebreaks=True,
        no_compiled_bodies_orROM_changes=True,all67_formatting_gates_false=True,native_glyph_fullwidth_I_escape_compilation_pending=True,
        source_branch_variants_not_claimed_all_naturally_played=True,existing_system_only_unlock_earned_false=True,
        evidence=dependencies,new_credit=0,full_goal_complete=False)
    save(OUTPUT,doc)
    reasons={
1:"Retain Hodram/Bergstrom and full-catalogue Joakim. Clean ホドラム/ベルグストロン/ヨアキム and both original getters support the approved names. The spoken self-introduction uses the source surname only; do not add a rank.",
3:"Retain Maria Li and full-catalogue Maria Huamei Li. All three source fields and original captain-special-object getters are bound; FA is Li, not the stale base-profile Lee. No hardcoded substitution is introduced.",
9:"Retain approved Camille and current Overijssel/Marinus. Clean カミル/オーフェルアイセル/マリヌス and both distinct getters are bound. Preserve membership in Argot, temporary accompaniment of Hodram and unspecified closeness to Lil without romance or kinship.",
10:"Retain Xien Yan in this scope: clean シエン/ヤン, null middle field and both current getters are bound. His reflective voice does not establish a new age, family relationship or title. No unsupported Yang respelling.",
26:"Retain Julian Lopes in this scope: clean ユリアン/ロペス and null middle field agree with the current original getters; preserve the conditional startled/angry reactions without inventing his presence in every branch.",
74:"Retain Richard Townsend in this scope: clean リチャード/タウンゼント and null middle field support both original getters. His formal country report and alarm do not supply an invented military rank.",
116:"Retain Port Worker for this Southeast Asian source actor. 出港所の兄貴 is a familiar port-worker role, not a biological brother; 東南アジア is regional metadata, not a surname. Keep the wider seven Port Worker consumers open.",
155:"Revision needed, replacement pending broader consumer audit: clean 配下 is a subordinate/follower role and 東南アジア is regional metadata. Original progressive getter says Sailor while catalogue says Retainer. This informant reports former service under Kuhn; that does not establish a nautical occupation, noble household or current loyalty. Do not globally overwrite this shared actor from one scene; bind all151–159 and relevant consumers before choosing a consistent label.",
}
    name_rows=[]
    for actor,reason in reasons.items():
        name_rows.append(dict(actor_ID=actor,decision='revision-pending-broader-consumers' if actor==155 else 'retention-in-this-exchange',
            reason=reason,clean_current_static_fields=deepcopy(next(r for r in names['complete_clean_andcurrent_static_name_fields'] if r['actor_ID']==actor)),
            original_getters=[deepcopy(r) for r in names['native_sixteen_progressive_and_full_name_consumers']['rows'] if r['actor_ID']==actor],
            source_speech_keys=[dict(id=r['id'],file_path=r['file_path'],source_reference=r['source_reference']) for r in rows if r['source_selector']==actor],
            name_asset_changed=False,actual_scene_headers_andfull_catalogue_UI_pending=True,new_credit=0))
    save(NAME_OUTPUT,dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],records=name_rows,
        native_proof=str(NAMES),native_proof_sha256=sha(NAMES.read_bytes()),all207_names_roles_aliases_review_still_active=True,
        proposed_generic_label_not_selected_from_one_scene=True,no_name_ROM_assets_changed=True,seven_contextual_retentions_one_unresolved_shared_role=True,
        evidence=dependencies,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);counts={v:sum(r['decision']==v for r in rows) for v in ['revision','retention']}
    save(ROOT/'67_whole_exchange_draft_decisions_and8_name_findings.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        names=str(NAME_OUTPUT),names_sha256=sha(NAME_OUTPUT.read_bytes()),records=67,decisions=counts,source_chain=[34,108,35],
        effective_catalogue_matches_reviewed=8,all67_source_context_localization_naturalness_true_formatting_false=True,
        full_context_retentions_individually_justified=True,uncredited_until_necessary_native_actual_production_release_checks_pass=True,
        no_ROM_build_orpromotion=True,evidence=dependencies,new_credit=0,full_goal_complete=False))
    print('DRAFT',counts,'total',len(rows),'names:7retentions/1shared-role unresolved;all formatting gates false;zero new credit.')
