"""Prepare completion credit only after exact release and viewed fresh startup."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
SUMMARY='''V3342 completes 63 contextual reviews in registered cumulative experimental V3338: 27 revisions and 36 individually justified retentions across Lil SC2 B131/B133. The 61 speeches include 18 real static Rafael actor00 speeches, 60 progressive speeches overall and one unlabeled FE notice; two labels belong to one original2100 menu. All records retain exact clean, predecessor-current, effective-runtime and integrated references, fresh source glosses, whole-exchange context and all five review gates. Both complete clean exchanges and fresh glosses preceded old-English comparison. B131 preserves Lil's tentative Old Parchment/Red Dye experiment, the revealed map to the North Sea Proof and alternate Camille/Fernando reactions. B133 preserves Rafael's gentle courtesy, Lil's prickly humor, Claudio's brusque defense and the full separate acceptance/refusal exchanges. The offer remains two percent Nantes for one percent Lisbon. No invented relationship, rank, noble status, romance or earned progress.

All112 commands,24 relative spans,120 relocated skips and exact inverse restoration pass. Only SC2 B131/B133 change from V3300;334 other blocks,all other files/components,ARM9,COMMON,font,graphics,BSS/cache and123040 staged bytes remain exact. Both images pass336 whole loaders/cache hits and672 parent modes;three shipped-entry censuses pass. All61 relocated dispatches,five predicate pairs and one FE null actor preserve original operands/results and unowned RAM without role,event,RNG,roster,health or outcome fixtures. There are no source2000 pauses,dynamic selectors,4100 objects or event queries in this batch.

Actor00 is a proven leading control byte,not an empty C string. All366 clean/current/compiled whole4000 cases,including108 actor00 cases,forward the nonempty body after the selector. The scoped formatter permits exactly one source-owned leading00 only for this profile;the shared encoder remains unchanged and rejects NUL. Body,trailing andduplicate NULs remain forbidden. FI6/FO1 use actual Lil captain2 substitutions,not Rafael-route widths. All61 complete native speech planes,two labels,488 logical/compiled and244 final stored-target macro cases preserve complete leading/trailing/internal characters,independent ink/blank paper,origin,bounds andsingle-page behavior. The initial17-cell acceptance lost20 leading-H pixels on102px paper;the faithful18-cell successor Hmm... fine, then. passes all108px planes without padding or a glyph waiver. One menu preserves source0/1/cancel,getters,geometry,eight current/reviewed style planes andthree final VM returns. All10 native sheets were viewed or hash-match viewed predecessors;three phrase-flow findings are resolved,with only19 row-count notes. All22 source-consumer,28 formatter and50 compiler negatives pass before mutation. Every failure,draft,producer andproof remains preserved.

V3338 rebuilds the complete canonical cumulative stack with521 manifest batches and114 accepted layers. The clean-input patch reconstructs the whole ROM byte forbyte. Two fresh targeted headless cold boots complete4001 Lil New Game and17401 town/Refit frames;31 whole framebuffers match V3300,five actor/captain controls anddonor hashes pass,andthe current six-frame sheet was viewed. Shared actual progressive/menu/FE rules inherit through exact code/assets/B74/B22 bindings. These actual gameplay samples remain distinct from offline native proofs. No selected B131/B133 scene,new individual nameplate,earned item/map,share exchange,contract,recruitment,profit,full-route orhardware verification is claimed. The inherited town battery remains unearned.

Coverage is4,797 fresh rereads/integrated/completed,with3,169 historically revised and1,628 retained. Source/prose4,800 includes2,970 SC2;all3,198 reviewed route objects are integrated,withzero pending reviewed route records. No duplicate source/prose credit is added. The remaining B135-B140 lead contains194 physical speeches andstill requires source/entry/copy classification andwhole-exchange review. Every wider untouched storyline,shared shop/town dialogue,random scene andremaining player-facing prose remains in scope. COMMON750-752 callers,canonical Maria32,SourceItems/LocalProduct,five named-target leads,rawB141/SC3B109 classification andthe exact-record Proof of Supremacy/Proof of Conquest editorial reconciliation remain open. No completed record is silently renamed orrecounted. Unresolved graphics/all18 plaques remain separate;retain the later older-record technical re-audit andqueued0D validation gap without asserting anold runtime defect. Preserve every ROM,earlier translation,draft,executed producer/proof/failure andclean/canonical input. V1492 remains promoted;V3338 is experimental. Full goal active;all jobs terminal.'''
if __name__=='__main__':
    old=Path('scripts/complete_lil_B122_B127_v3304.py');new=Path('scripts/complete_lil_B131_B133_v3342b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    a=t.index("SUMMARY='''");z=t.index("if __name__=='__main__':",a);t=t[:a]+'SUMMARY='+repr(SUMMARY)+'\n'+t[z:]
    pairs={
      'lil_B122_B127_completion_v3304':'lil_B131_B133_completion_v3342b','lil_B122_B127_contextual_final_review_v1':'lil_B131_B133_contextual_final_review_v1',
      'lil_B122_B127_editorial_manuscript_v6':'lil_B131_B133_editorial_manuscript_v5','lil_B122_B127_choice_manuscript_v5':'lil_B131_B133_choice_manuscript_v6',
      'lil_B122_B127_release_v3301':'lil_B131_B133_release_v3339','lil_B122_B127_startup_v3303':'lil_B131_B133_startup_v3341',
      'editorial_handoff_verification_v3297':'editorial_handoff_verification_v3328','Lil-B122-B127-159':'Lil-B131-B133-63',
      'all519_manifest_batches':'all521_manifest_batches','equal_V3251':'equal_V3300','actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs',
      "registered_prose_owner='lil_B122_B127_editorial'":"registered_prose_owner='lil_B131_B133_editorial'",
      '# Current editorial handoff - V3296':'# Current editorial handoff - V3327',
      "Path(doc['original2000_wait_proof']),Path(doc['conditional_return_proof'])":"Path(doc['whole_typed_speech_proof'])",
      'lil_B122_B127_registration_v3299b':'lil_B131_B133_registration_v3337b',
      'lil_B122_B127_reference_census_v3291/all312_commands64_relative_sites_and_shipped_entry_census':'lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census',
      'lil_B122_B127_loader_v3290/whole_SC2_and_six_selected_blocks_initial_entry_proof':'lil_B131_B133_loader_v3331/whole_SC2_and_two_selected_blocks_initial_entry_proof',
      'both_source2000_pauses_and_two2100_menus_and_conditional_returns_preserved=True':'source00_full_bodies_and_one2100_menu_preserved=True',
      'source2000_pauses_and_two2100_menus_and_conditional_returns_preserved=True':'source00_full_bodies_and_one2100_menu_preserved=True',
      'blocks=list(range(122,128))':'blocks=[131,133]',
      "for k in ['lil_B122_B127_v3286','lil_B122_B127_v3296']":"for k in ['lil_B131_B133_v3327']",
      'lil_B122_B127_v3304':'lil_B131_B133_v3342',
      'previous_current_integrated_candidate_before_V3300':'previous_current_integrated_candidate_before_V3338',
      "ledger['unfinished_editorial_scope_v3296']":"ledger['unfinished_editorial_scope_v3327']",
      "inventory['B122_B127_reference_ready_v3296']":"inventory['B131_B133_fresh_context_review_checkpoint_v3327']",
      'lil_B122_B127_completed_v3304':'lil_B131_B133_completed_v3342',
      'unfinished_editorial_scope_v3304':'unfinished_editorial_scope_v3342',
      'lil_B122_B127_scope_reconciliation_v3286':'lil_B131_B133_scope_reconciliation_v3327',
      'V3304':'V3342',
    }
    # Keep the summary verbatim;adapt only executable boilerplate.
    a=t.index('if __name__');prefix=t[:a];t=t[a:]
    for a,b in sorted(pairs.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    counts={4734:4797,4575:4734,4737:4800,3142:3169,1592:1628,2907:2970,3135:3198,159:63,55:27,104:36}
    t=re.sub(r'(?<!\d)(4734|4575|4737|3142|1592|2907|3135|159|55|104)(?!\d)',lambda m:str(counts[int(m[0])]),t)
    t=t.replace('==(4797,4734,63)','==(4797,4734,63)')
    t=t.replace('Inherited actual shared progressive/menu/FE/pause rules plus two current opening/town cold boots;155planes/fourlabels/twopauses/14predicates/conditionalreturns separately offline native-tested. No selected B122-B127 scene or earned progress.','Inherited actual shared progressive/menu/FE rules andtwo fresh opening/town cold boots;61speech/twolabels/source00/predicates separately offline native-tested. No selected B131/B133 scene or earned progress.')
    t=t.replace('COMMON750-752callers,Proofterminologyconsistency,canonicalMaria32,B133source00 andevery wider untouched prose family remainopen.','COMMON750-752callers,Proofterminologyconsistency,canonicalMaria32,B135-B140 andevery wider untouched prose family remainopen.')
    t=t.replace('Continue wider untouched route/shared shop-town/random/help/player prose;Proof terminology consistency,source00 B133 andcanonicalMaria32 stayopen.','Continue B135-B140 andevery wider untouched route/shared shop-town/random/help/player prose;Proof terminology consistency andcanonicalMaria32 stayopen.')
    a=t.index("next_focus='Continue every wider");z=t.index("')\n",a)+2
    t=t[:a]+"next_focus='Continue194 physical B135-B140 speech leads with entry/copy classification andwhole-exchange review,then every wider untouched storyline/shared shop-town/random/help/player prose. Keep Proof terminology consistency,canonicalMaria32,COMMON750-752callers,SourceItems/LocalProduct,five namedtargets,rawB141/SC3B109,graphics separation andlater technical audit open.')"+t[z:]
    a=t.index("    note='Experimental profile '");z=t.index("    for i,p in enumerate(documents):",a)
    t=t[:a]+"""    note='Experimental profile '+release['profile']+'. Candidate '+release['candidate']+', SHA-256 '+release['candidate_sha256']+'. Canonical base '+release['canonical_base']+', SHA-256 '+release['canonical_base_sha256']+'. Clean-input patch '+release['patch']+', SHA-256 '+release['patch_sha256']+'. Manifest521batches/114acceptedlayers:fullV3300 plus61speech/two-label manuscripts. DeltafromV3300:SC2blocks131/133 only;allotherfiles/components exact.50compiler negatives;release3339/startup3341 pass. Freshcoldboot:title/character selection,Lilopening,town/Refit. V1492remainspromoted.\\n\\n'
    section='## V3342:63 Lil B131/B133 objects completed in V3338\\n\\n'+SUMMARY+'\\n\\n'+note+'Finalreview: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinishedscope: '+inv.as_posix()+'.\\n\\n'
"""+t[z:]
    t=t[:t.rindex('    print(')]+"    print('V3342:63 completed inregisteredV3338;27revisions/36retentions;4797reread/integrated,4800source-prose. Full widergoal remains active.')\n"
    t=prefix+t
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_completion_tools_v3342');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
