"""Prepare one pending-credit checkpoint for33 native-approved B170 reviews."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_checkpoint_tools_v4279')
SUMMARY='''V4279 records33 fresh contextual/native reviews for the complete Lil SC2 B170 Yifa collision,argument,apology,flattery,Taoist-training and ship-passage exchange:21 proposed revisions and12 individually justified retentions. All33 clean Japanese speeches were read and individually glossed as one exchange before predecessor English comparison. Preserve the abrupt collision and rushed apology,Lil's insistence,Yifa's irritation,sudden admission of fault,Lil's flustered acceptance and vain response to flattery,the tentative request for advice,explicit Admiral boast,FO fleet explanation and admiration. Keep money as a question,Yifa running away because her teacher repeatedly scolded her during Taoist training,her refusal to quit,wish to travel while continuing practice and become much stronger,Lil's qualified sympathy,explicit request aboard Lil's ship,full determination-never-to-lose test,prior harsh-training endurance,agreement,names and work-hard encouragement. Remove unsupported big sis kinship and the teacher's male pronoun. Use native-bound Yifa in spoken introductions without adding catalogue-only Sol. Add no teacher gender,name,school,nationality,degree,abuse,expulsion,named spell,price,reward,romance or numeric skill threshold. Every12 retained wording has an individual contextual reason;the working short reactions and banter stay intact.

Fresh source/current contracts bind33 complete progressive preambles,selectors02/19 (Lil2/Yifa25),FI1/FO1,45 commands,twelve nonrelative leaves,two original630x resource words/20 boundary cases,six isolated presentation/pause structural sites,one C200 clean/current pair,one two-byte2000 pause at36/resume38,one later A000 and both consecutive endwords1852/1856. Four original progressive/full-name getters preserve owned scratch rings/writes and all4MiB restoration;both names are Lil Argot/Yifa Sol. The207-entry/eight-voice catalogue is rebound by exact runtime,COMMON,EV2,font and snapshot. Source19 remains Yifa's selector. Taoist arts is bound to two exact completed COMMON Yifa records. The source supplies Lil's Admiral claim here and leaves the teacher's gender unspecified;お姉さん is a familiar address to a female stranger,not a sister relationship. Source event170/action171 and its getter are bound without claiming eligibility. No relative sites,predicates,FE or typed choices exist in this block;the zero-site census makes no branch-execution claim. A000 raw words1019/2001 and C200 stay intact;full effect,figure,pause and normal-return behavior remain unexecuted. Keep the later older-record technical re-audit separate.

Native approval V4278 covers all33 complete216x64 progressive planes and264 logical/compiled alignment cases. The final proof freshly checks16 alignment cases/two changed complete records and reuses248 exact cases/31 byte-identical records from the original264-case native proof,with exact runtime,source,English,encoded bytes,font plane and preview hashes bound. All33 QA plans are fresh and all five final sheets were viewed. Complete leading/internal/final glyphs,unique cells,zero row origins,four-row bounds and single-page consumption pass.13 source-consumer,two missing-macro and14 formatter rejection controls pass. Eleven narrow row-count notes exempt no glyph,bounds,pagination,macro,control,weak-ending,orphan or blank-page issue. Keep Come over here together and express Lil's qualified sympathy as I guess I understand;all source meanings and21/12 decisions remain intact. No authored breaks,padding,wording waiver or shared guard/metric change. No B170 actual gameplay or transition coverage is claimed yet.

Coverage becomes5725 fresh contextual rereads:5692 integrated/completed and33 pending. Source/prose becomes5728,including3872 SC2 and unchanged64 SC3;reviewed/completed route objects4126/4093. Historical completed decisions stay3614 revised/2078 retained. B170 is credited once as pending,with no completion credit. The latest verified experimental cumulative build remains V4251,545 manuscript batches/114 accepted layers,with its exact clean-input patch. Promoted main remains V4204. Registry,builder,promoted pointer,canonical input,all prior completions and every earlier ROM/translation/draft/executed producer/proof/failure remain unchanged.

Remaining B171-B180 has198 physical speeches and zero typed-choice-command leads,not a full Lil/project denominator. Every wider storyline,shared shop/town exchange,random scene,Help and other player-facing prose stays open. Preserve COMMON750-752,canonical Maria32 SC3 B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active;all jobs terminal.'''
NEXT='Complete B170 relocation and stored/native references,representative paired source/English content with the original figure,pause,resources,later A000,C200 and normal return;then atomic compiler tests,registered cumulative build,exact clean-input patch and fresh registered startup. Keep both source ends and distinguish decoder coverage from actual reachability. Continue B171-B180 and every wider editorial family. V4204 remains promoted main;V4251 remains the latest verified cumulative candidate. Preserve every ROM,translation,draft and executed producer/proof/failure.'

if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/checkpoint_lil_B169_v4231.py')
    new=Path('scripts/checkpoint_lil_B170_v4279.py')
    assert not new.exists()
    text=old.read_text(encoding='utf-8')
    a=text.index("NEXT = '")
    b=text.index("if __name__ == '__main__':",a)
    text=text[:a]+'NEXT = '+repr(NEXT)+'\nSUMMARY = '+repr(SUMMARY)+'\n\n'+text[b:]
    changes={
        'Stage36 native-approved whole-exchange reviews':'Stage33 native-approved whole-exchange reviews',
        'lil_B169_checkpoint_v4231':'lil_B170_checkpoint_v4279',
        'work/analysis/promotion_v4226/promotion_receipt.json':'work/analysis/editorial_handoff_verification_v4259/verified_handoff.json',
        'lil_B169_native_approval_v4230':'lil_B170_native_approval_v4278',
        'lil_B169_editorial_manuscript_v4':'lil_B170_editorial_manuscript_v5',
        'Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36':'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33',
        'len(rows) == 36':'len(rows) == 33',
        '(5656,5656,0)':'(5692,5692,0)','}) == 36':'}) == 33',
        "== 3803":"== 3839","== 5659":"== 5695",
        '# Current editorial handoff - V4226':'# Current editorial handoff - V4258',
        '= 5695':'= 5728','= 3839':'= 3872',
        '5692 fresh rereads:5656 integrated/36 pending;source/prose5695. B169 credited once as pending':'5725 fresh rereads:5692 integrated/33 pending;source/prose5728. B170 credited once as pending',
        '36-Lil-B169-native-approved':'33-Lil-B170-native-approved',
        'blocks=[169],records=36':'blocks=[170],records=33',
        'proposed_revisions=19,retentions=17,source_prose_reviews_added=36':'proposed_revisions=21,retentions=12,source_prose_reviews_added=33',
        'actual_selected_B169_IDs':'actual_selected_B170_IDs',
        'fresh_pass_records_explicitly_reread=5692,fresh_pass_records_integrated=5656':'fresh_pass_records_explicitly_reread=5725,fresh_pass_records_integrated=5692',
        'fresh_pass_records_pending_native_actual_release=36':'fresh_pass_records_pending_native_actual_release=33',
        'reviewed_route_records=4093,completed_route_records=4057':'reviewed_route_records=4126,completed_route_records=4093',
        'lil_B169_v4231':'lil_B170_v4279','row_count_notes=14':'row_count_notes=11',
        'unfinished_editorial_scope_v4208':'unfinished_editorial_scope_v4258',
        'blocks=[169],count=36':'blocks=[170],count=33','incomplete_route_source_prose_count=36':'incomplete_route_source_prose_count=33',
        'B169_fresh_context_review_checkpoint_v4231':'B170_fresh_context_review_checkpoint_v4279',
        'remaining_B170_B180_unreviewed_uncredited':'remaining_B171_B180_unreviewed_uncredited',
        'physical_speeches=231':'physical_speeches=198',
        'earlier_B169_uncredited_leads_are_historical_after_V4231':'earlier_B170_uncredited_leads_are_historical_after_V4279',
        'source_prose_pending_records=36':'source_prose_pending_records=33',
        'unfinished_editorial_scope_v4231':'unfinished_editorial_scope_v4279',
        'incomplete_route_source_prose=36':'incomplete_route_source_prose=33',
        'remaining_B170_B180_physical_speeches=231':'remaining_B171_B180_physical_speeches=198',
        'lil_B169_scope_reconciliation_v4231':'lil_B170_scope_reconciliation_v4279','source_prose_reviews_added=36':'source_prose_reviews_added=33',
        '## V4231:36 B169 contextual/native reviews':'## V4279:33 B170 contextual/native reviews',
        '# Current editorial handoff - V4231':'# Current editorial handoff - V4279',
        "checkpoint='V4231'":"checkpoint='V4279'",'new_source_prose_reviews=36':'new_source_prose_reviews=33',
        'proposed_revisions=19,justified_retentions=17':'proposed_revisions=21,justified_retentions=12',
        'fresh_reread=5692,fresh_integrated=5656,fresh_pending=36,source_prose=5695,completed=5656':'fresh_reread=5725,fresh_integrated=5692,fresh_pending=33,source_prose=5728,completed=5692',
        'historical_revised=3595,historical_retained=2061':'historical_revised=3614,historical_retained=2078',
        'V4231 staged:5692 reread/5656 integrated/36 pending;5695 source/prose. Promoted V4204 unchanged':'V4279 staged:5725 reread/5692 integrated/33 pending;5728 source/prose. Latest V4251 and promoted V4204 unchanged',
    }
    for item in changes:assert item in text,item
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    compile(text,str(new),'exec')
    new.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),
        expected_counts=dict(fresh=5725,integrated=5692,pending=33,source_prose=5728,completed=5692,SC2=3872,SC3=64,
                             route_reviewed=4126,route_completed=4093,historical_revised=3614,historical_retained=2078),
        no_credit_change_until_checkpoint_applied=True,full_goal_complete=False))
    print('B170 pending-credit producer prepared;33 native-approved reviews,21 revisions/12 retentions;latest V4251 and main V4204 preserved.')
