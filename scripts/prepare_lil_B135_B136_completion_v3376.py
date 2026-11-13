"""Prepare completion-only credit withfull evidence andremaining scope preserved."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
SUMMARY='''V3376 completes35 contextual reviews in registered cumulative experimental V3372:16 revisions and19 individually justified retentions across Lil SC2 B135/B136. Every speech retains exact clean,predecessor-current,effective-runtime andintegrated references,a fresh gloss,whole-exchange context andallfive review gates. B135 preserves the customer's distress,Espinosa's price exploitation andfalse respectable-business claims,Gilberto's intimidation,Lil's challenge andthe conditional Camille coda ofshared resolve. B136 preserves the tablet halves,their perfect fit,Lil's tentative map-to-Proof discovery andEmilio's food-driven mishearing withits deadpan correction. Japanese chizu/map versus chiizu/cheese becomes chart versus cheese tart;the documented tart is aphonetic vehicle,not anactual item orplot fact. Exact item pointers bind UpperStoneTablet176/LowerStoneTablet183;Goddess' Temptation matches two related completed records. One effective-current registered Camille replacement is retained withits rawstorage provenance separate. No invented rank,kinship,noble status,romance or earned progress.

All61 commands,four relative spans,20 relocated native skips andinverse restoration pass. Only SC2 B135/B136 differ fromV3338;334otherblocks,allotherfiles/components,ARM9,COMMON,font,graphics,BSS/cache and123040stagedbytes remain exact. Bothimages pass336wholeloaders/cachehits and672parentmodes;three entrycensuses pass. All35 relocated static dispatches andonepredicatepair preserve operands/results/unownedRAM without role,event,roster,RNG,health oroutcome fixtures. NoFE,source00,2100,2000,dynamicselector,4100 oreventquery occurs. All35 complete nativeplanes,280logical/compiled and140final stored-target macro cases preserve full leading/trailing/internal glyphs,independentink/blankpaper,origins,bounds andsinglepage behavior. FO1 usesLilcaptain2 context. Five concretephrase findings are resolved,includingonefaithful conditionalrefinement;allfivefinalsheets wereviewed orhash-match viewedpredecessors. Only15row-count notesremain. All21source-consumer,14formatter and28compiler negativespass beforemutation. Failedgenerators,partialblocks,drafts,producers andproofs remainpreserved.

V3372 rebuilds the fullcanonical cumulative stack with522manifestbatches/114acceptedlayers. Its clean-inputpatch reconstructs thewholeROM byteforbyte. Twofresh targetedheadless coldboots complete4001LilNewGame and17401town/Refitframes;31wholeframebuffers matchV3338,fiveactor/captainchecks anddonorhashes pass,andthecurrentsix-framesheet wasviewed. Sharedactual progressive displayrules inheritthroughexact runtime/COMMON/EV2/font/B74/B22bindings. Actual gameplay samples remain distinctfromoffline nativeproofs. NoselectedB135/B136 scene,newindividualnameplate,druguse,item/mapacquisition,Proofdiscovery,victory,recruitment,profit,full-route orhardwareverification isclaimed. Theinheritedtownbattery remainsunearned.

Coverage is4,832fresh rereads/integrated/completed,with3,185historically revised and1,647retained. Source/prose4,835 includes3,005SC2;all3,233reviewedrouteobjects areintegrated,zero pendingreviewedrouteobjects. Nonewsource/prosecredit isaddedatcompletion. RemainingB137-B140 leadshave159physicalspeeches requiringentry/copyclassification andwhole-exchange review. Everywideruntouched storyline,sharedshop/town dialogue,randomscene andremainingplayer-facingprose staysinscope. COMMON750-752callers,canonicalMaria32,SourceItems/LocalProduct,fivenamedtargets,rawB141/SC3B109 andexact-recordProof ofSupremacy/Proof ofConquest editorialreconciliation remainopen. Nocompletedrecord issilentlyrenamed orrecounted. Graphics/all18plaques remainseparate;retain thelaterolder-recordtechnicalre-audit/queued0Dvalidationgap withoutassertinganoldruntimedefect. PreserveeveryROM,translation,draft,executedproducer/proof/failure andclean/canonicalinput. V1492remainspromoted;V3372isexperimental. Fullgoalactive;alljobsterminal.'''
if __name__=='__main__':
    old=Path('scripts/complete_lil_B131_B133_v3344b.py');new=Path('scripts/complete_lil_B135_B136_v3376b.py');assert not new.exists();t=old.read_text(encoding='utf-8');a=t.index('SUMMARY=');z=t.index("if __name__=='__main__':",a);t=t[:a]+'SUMMARY=__SUMMARY__\n'+t[z:]
    changes={
      'lil_B131_B133_completion_v3342b':'lil_B135_B136_completion_v3376b',
      'lil_B131_B133_editorial_manuscript_v5':'lil_B135_B136_editorial_manuscript_v6',
      "MENU=Path('translations/lil_B131_B133_choice_manuscript_v6.json')":"MENU=None",
      'lil_B131_B133_release_v3339':'lil_B135_B136_release_v3373',
      'lil_B131_B133_startup_v3341/current_B131_B133_scoped_startup_verification.json':'lil_B135_B136_startup_v3375/cold_boot_Lil_startup_town_verification.json',
      'lil_B131_B133_startup_v3341':'lil_B135_B136_startup_v3375',
      'editorial_handoff_verification_v3328':'editorial_handoff_verification_v3362',
      'Lil-B131-B133-63':'Lil-B135-B136-35','[131,133]':'[135,136]',
      "doc,menu=map(read,[DOC,MENU])":"doc,menu=read(DOC),{'records':[]}",
      'all521_manifest_batches':'all522_manifest_batches','equal_V3300':'equal_V3338',
      'actual_selected_B131_B133_IDs':'actual_selected_B135_B136_IDs',
      '# Current editorial handoff - V3327':'# Current editorial handoff - V3361',
      "Path(doc['whole_typed_speech_proof'])":"Path(doc['native_progressive_proof'])",
      'lil_B131_B133_registration_v3337b':'lil_B135_B136_registration_v3371b',
      'lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census':'lil_B135_B136_reference_census_v3366b/all61_commands4_relative_sites_and_shipped_entry_census',
      'lil_B131_B133_loader_v3331':'lil_B135_B136_loader_v3365b',
      'source00_full_bodies_and_one2100_menu_preserved=True':'all35_static_progressive_source_controls_preserved=True',
      'for p in [DOC,MENU]:':'for p in [DOC]:','proofpaths=[DOC,MENU,':'proofpaths=[DOC,',
      'choices=str(MENU)':'choices=None','latest_contextual_choice_draft=str(MENU)':'latest_contextual_choice_draft=None',
      "for k in ['lil_B131_B133_v3327']":"for k in ['lil_B135_B136_v3361']",
      'lil_B131_B133_v3342':'lil_B135_B136_v3376',
      'previous_current_integrated_candidate_before_V3338':'previous_current_integrated_candidate_before_V3372',
      "ledger['unfinished_editorial_scope_v3327']":"ledger['unfinished_editorial_scope_v3361']",
      'B131_B133_fresh_context_review_checkpoint_v3327':'B135_B136_fresh_context_review_checkpoint_v3361',
      'lil_B131_B133_completed_v3342':'lil_B135_B136_completed_v3376',
      'unfinished_editorial_scope_v3342':'unfinished_editorial_scope_v3376',
      'lil_B131_B133_scope_reconciliation_v3327':'lil_B135_B136_scope_reconciliation_v3361',
      'lil_B131_B133':'lil_B135_B136','V3342':'V3376',
      '(4797,4734,63)':'(__FRESH__,__INTEGRATED__,__PENDING__)',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    counts={4797:4832,4800:4835,3169:3185,1628:1647,2970:3005,3198:3233,63:35,27:16,36:19}
    t=re.sub(r'(?<!\d)(4797|4800|3169|1628|2970|3198|63|27|36)(?!\d)',lambda m:str(counts[int(m[0])]),t).replace('__FRESH__','4832').replace('__INTEGRATED__','4797').replace('__PENDING__','35')
    t=t.replace('Inherited actual shared progressive/menu/FE rules andtwo fresh opening/town cold boots;61speech/twolabels/source00/predicates separately offline native-tested. No selected B131/B133 scene or earned progress.','Inherited actual shared progressive rules andtwofresh opening/town coldboots;35speech/onepredicate separately offline native-tested. No selected B135/B136 scene orearnedprogress.')
    a=t.index("next_focus='Continue194");z=t.index("')\n",a)+2;t=t[:a]+"next_focus='Continue159 physical B137-B140 speech leads withentry/copy classification andwhole-exchange review,then everywider storyline/sharedshop-town/random/help/playerprose. Keep Proofconsistency,Maria32,COMMON3,SourceItems/LocalProduct,fivenamedtargets,rawB141/SC3B109,graphicsseparation andlater technicalaudit open.')"+t[z:]
    t=t.replace('B135-B140','B137-B140').replace('B135/B133','B135/B136')
    a=t.index("    note='Experimental profile '");z=t.index('    for i,p in enumerate(documents):',a)
    t=t[:a]+"""    note='Experimental profile '+release['profile']+'. Candidate '+release['candidate']+', SHA-256 '+release['candidate_sha256']+'. Canonical base '+release['canonical_base']+', SHA-256 '+release['canonical_base_sha256']+'. Clean-input patch '+release['patch']+', SHA-256 '+release['patch_sha256']+'. Manifest522batches/114acceptedlayers:fullV3338 plus35speech manuscript. DeltafromV3338:SC2blocks135/136 only;allotherfiles/components exact.28compiler negatives;release3373/startup3375 pass. Freshcoldboot:title/character selection,Lilopening,town/Refit. V1492remainspromoted.\\n\\n'
    section='## V3376:35 Lil B135/B136 objects completed in V3372\\n\\n'+SUMMARY+'\\n\\n'+note+'Finalreview: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinishedscope: '+inv.as_posix()+'.\\n\\n'
"""+t[z:]
    t=t[:t.rindex('    print(')]+"    print('V3376:35completed inregisteredV3372;16revisions/19retentions;4832reread/integrated,4835source-prose. Fullwidergoal active.')\n"
    t=t.replace('SUMMARY=__SUMMARY__','SUMMARY='+repr(SUMMARY));compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B135_B136_completion_tools_v3376');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
