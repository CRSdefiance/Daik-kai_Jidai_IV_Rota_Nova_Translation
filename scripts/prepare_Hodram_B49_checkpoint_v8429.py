"""Reversible full-objective checkpoint after B49 actual/format/policy validation;integration still pending."""
from pathlib import Path
from scripts import prepare_Hodram_B49_checkpoint_v8413 as previous
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

PROOFS={**previous.PROOFS,
 'prior_native_manuscript':'translations/hodram_B49_editorial_manuscript_v2.json',
 'format_manuscript':'translations/hodram_B49_editorial_manuscript_v3.json',
 'manuscript':'translations/hodram_B49_editorial_manuscript_v4.json',
 'names':'translations/hodram_B49_speaker_name_review_v2.json',
 'format_approval':'work/analysis/Hodram_B49_format_v8423/formatting_approval.json',
 'tail_fixture':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
 'menu_actual':'work/analysis/Hodram_B49_menu_actual_v8418/four_actual_menus12_full_owned_backing_andhighlight_samples.json',
 'FE_binding':'work/analysis/Hodram_B49_FE_binding_v8420/two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json',
 'tail_comparison':'work/analysis/Hodram_B49_tail_comparison_v8421/both_bounded_tail_comparisons.json',
 'tail_difference_sheet':'work/analysis/Hodram_B49_tail_diff_view_v8422/sheet.json',
 'encoder_approval':'work/analysis/Hodram_B49_encoder_v8426/metadata_approval.json',
 'frozen':'work/analysis/Hodram_B49_policy_v8427/frozen_contract.json',
 'contract':'translations/hodram_B49_native_contract_v2.json',
 'policy_validation':'work/analysis/Hodram_B49_policy_validation_v8425b/policy_validation.json',
 'production_rebuild_positive':'work/analysis/Hodram_B49_rebuild_tools_v8428b/independent_reconstruction_positive.json',
}

SUMMARY="""Registered cumulative V8377 remains current; main V4701/canonical baseline andall earlier ROMs/translations are preserved. Exact counts remain7205completed/7208credited source-prose-drafts/4474integrated revisions/2731retentions;SC0368/SC1125/SC24915/SC3197/COMMON1600complete1603source-prose/routesubset5605. No new completion/source-prose credit,registered build,promotion,separate userpackage,pruning,commit orpush. Full objective remains active.

B49 nowhas allfive individual review gates true for14speeches andtwo canonical typedchoices,seven revisions/nine justified retentions,plus two scoped name retentions. Latest manuscriptv4 andnamesv2 preserve every approved word,source/current/final reference,source-qualified controls andruntime substitution. Automatic plan8394/native8395/stored8399 retain full216usable width,14single pages,complete leading/internal/trailing glyphs,source-bound silence/mixed ellipses,the three balanced New World direction rows,seven line-count infos andzero warnings/waivers. All36commands/eight relative sites/40fresh cases,raw8000query,typed2100menu,two item148 layouts/hides,seven effects/full4byte end andtails arebound;both clean/current block inverses,whole archive/ROM inverse,all324otherSC1blocks/allother files/components,325load-cache/650entrymodes/326actions andshipped caller census remain verified.

Whole-script initialized captures stillcover six source/sixEnglish pages/66complete body/name holds in20002frames. Newbounded possession-dialogue-tail fixtures8415 preserve eight original opening initializers34bytes,two sourceB49entrycommands,andthe original tail beginning atclean428/current402. The omitted eligibility prefix andouter skip areexplicit;23selected original commands/eight speeches/five internal relatives/two choices/FE/item148layout0/effects/end areunchanged apartfromconstant relocation. Four identical-input source/English accept/decline runs8416/actual8417 add40004frames/22page occurrences/134complete body-name-orabsent-FE-header holds. Menu native results are[2,0]/[2,1];normalends sourceaccept5219/English5218[0,0],bothdecline5938[0,1]. Togetherwhole/tail captures observeall14unique source/English speech displays andboth typedchoices. These aredisclosed initialized fixtures,not natural optional-event activation,earned possession/trade eligibility,original location,fullroute orhardware coverage. No runtime inventory/flags/RNG/roles/funds/results orsource-English controller retiming wasforced.

Actual menu8418 verifiesfourmenus/twelve full owned-caption backing samples/twenty-four visible labels,original60pxcaption views inside256x36backing,complete CP932/ASCII glyphs/blank guards/backgrounds,bothinput highlights,dismissal andresult forwarding. Alltwelve selected highlights werevisible. Later sailing-menu All right. callbacks areexplicitly separated bythe original B49menu interval andretained;no whole-backing blank/equality claim. Sixnewtail body sheets/four FE-item-return strips/menu sheet/two comparison strips/one difference sheet were directlyviewed8423. Mixedellipsis+ASCII R67 iscomplete inactual Hodram display. FE8419/8420 adds9862focusedframes,two original paint CPU/WRAM/TCM snapshots/four exactheld logical bitmaps/palette/bank-D VRAM/RGB holds. Original228x48/288stride/6x12/16pitch andabsent personal header persist. The outgoing-wristband line remains distinct fromthe following original item148 acquisition UI;bothlayout0 card/hide transitions wereviewed withoutclaiming legitimately earned inventory.

TotalB49actual coverage is69868frames/eight runs. Preserve every measured limitation:whole-script source5213/English5216[0,0],two duration differences,PRNG differences at324/416/424/980,finalseeds both1633251573,five components/actors equal,79of81laterRGBpairs equal withPorttooltip/sailinghighlight differences. Tailaccept hasone durationdifference,allobserved script-boundary seeds equalbutfinalseeds996112413/155404999 differ,78of81laterRGBpairs equal;5590A-button prompt,6130sailing first-row highlight,7750Depart first-row highlight differences wereviewed. Taildecline hasfour durationdifferences,twelve source-boundary PRNG differences despiteequalfinalseed3478759668,all69laterRGBpairs equal. Bothtailchoices havezero UIrequest differences/five checked components/wholeactors/captain1 equal;rawcalendar0/[0,0,0] staysuninterpreted. Matching samples do notprove every-frame causality,future RNG outcomes orbroad simulation. Allolder Gerhard/Rafael/Hodram/B48 limits remain.

The unchanged standard policy rejected manuscriptv3's inherited descriptive encoder natural-dialogue. Preserve rejectedv3/frozencontractv1/8425attempt. V8426 changesonly that rootmetadata to supported dialogue-relocatable-v1 inmanuscriptv4;source/prose/review/compiled/finalrefs/names/actualproofs areunchanged andstandardv2validates bothspeech/choice sets. Frozencontractv2/modulesv2 from8427 retainall435original dependencies andaddten,withall native/compiler/QA/source/choice bindings exact. No global guard isweakened;the mutable integrated builder isnot accidentally pinned asan editorial dependency. Policy8425b passes14speech compiler positives/two typedlabels/allfivegates/scopednames and838actualchanged-input expected rejections. All445frozen guards stayenabled;protected sources/ROMs/ledger/registry/pins/modules remainhash-exact. Independent production reconstruction helperv2/8428b matches the tested wholeblock andboth inverses. Preserve its failedv1/8428attempt:one inherited36byte menu replacement span wascorrected toactual26bytes;allguards stayedactive andno ROM commit occurred. Independent native/actual production readers,semantic precommit tests,atomic integration,registered cumulative build/cleaninputpatch/ownstartup andonceonly16credit remainpending.

Preserve fullall-four-story objective,earlier translated dialogue,sharedshop/town/random/Help/remainingprose,all207name/role/alias/custom-name risks andretrospectiveprematurewraps. Copyevery priorlead,family,history,source-name/item/cultural finding andtechnical limit. Graphics/all18plaques andlater older-record technical re-audit stayseparate."""

NEXT="""Continue fromverifiedV8430/currentregisteredV8377. B49 manuscriptv4,namesv2,frozencontractv2 andhodram_B49 profile/layout/plan/choices/names modulesv2 arecurrent;policy8425b has838rejections andindependent reconstruction helperv2/8428b passes. Allsixteen five-gate approvals andexactsource/current/finalrefs arecomplete butuncredited. Reuse allcompleted source/prose/layout/native/stored/controls/inverses/loaders/caller/wholeactual/boundedtail/menu/FE/policy checks. No unchanged replay isneeded. UseownV8377captain1input8380 forRAM-dependent independent readers;never overlay historicalRAM orborrowcaptain2.

Implement andvalidate independent production binding/native-font/actual-menu/FE/comparison/loader readers fromtrusted immutable source templates. Preserve actual capture schedules,resident payloads,complete glyph/owned backing masks,typed descriptor/palette/VRAM,allmeasured timing/PRNG/RGB differences andscope limits. Bindall16canonical IDs,14fullpreambles,eightrelatives,onequery,one22bytetypedmenu,sourceeffects,pictures/hides,fullterminal/tails andall324unowned blocks toone complete current image. Usehodram_B49_reconstruction_v2;v1's wrong36byte menu span ispreserved failed evidence.

Before registering a newowned B49stage,inspect existing integrated-builder hooks andHodram-outcome417dependency/builderguardv2 compatibility. Its exact original/ownedv2/v3 stage inverse is frozen;do not let a newB49addition silently disable orbreak the preceding six-record stage. Prefer an existing supported extension hook ifit preserves one whole-image atomic stage. Ifsource-locked guard/profile/import successors areneeded,retain every other frozen dependency andsemantic body,explicitly verify fullbuilder inverse/knownstages andchanged-builder negatives,prove the preceding fullV8377output remains byte-exact,andthen addonly theB49stage. Do not modify executed producers orpin mutable builder bytes accidentally into the neweditorial contract.

Validate one complete-NDS atomic commit andmeaningful semantic precommit rejections withwhole input object/serialized bytes preserved onfailure. Test canonical.source+fullV8377.rom aswellasdirectcurrentinput;compare bytes(parent.rom.save()),notparent.source diskbytes,andcommit image.rom=planned.rom onlyatend. Register cumulatively afterentireV8377/explicit Gerhard Adernkatz dependency. Build onlythrough build_integrated_release.py;verify completeaccepted stack,exactresearch reference,cleaninputpatch reconstruction andownstartup. Credit16onceonlyafter requiredgates:projected7221completed/7224source-prose/4481revised/2740retained/SC1141/routesubset5621,subjecttofinal arithmetic. Preserveall priorROMs/translations/drafts/proofs/failures/main4701/canonicalbaseline;no separateuserpackage,promotion,pruning,commit/push.

Fullobjective remainsallfourstories andearlier translateddialogue,sharedtown/shop/random scenes,Help/remainingprose,all207names/roles/aliases/customnames andretrospectiveearlybreaks. Allcopiedcontraction/questiontag/unscanned558plan/weak-before-row/COMMON750-752/preLF6435,wideractor104/105/113/147,JanusPasar/Pasha,ceramics17wrap,Cristina/Christina,HansRetzel/Letzel,Samwellmiddle,SourceItem/LocalProduct,Alexandria,AksumGoldSeal,Armadillo/SteelHide,HerophilusMedicine,イギリス,AlShin/AlFeridShin,Sailor151-159versusRetainer leads remain. Retainallolder normalendcarry/nineteenthcell/B47/B48/B50metadata andall timing/RNG/component/calendar/RGB/fixture-entry limits. Broadpracticaltown/randomcapture andhonestoffline/gameplay distinctions remainrequired;graphics/later older-record technicalre-audit separate."""

GATES='''def gates():
    from collections import Counter
    from dk4tool.dialogue.hodram_B49_profile_v2 import contract,validate_approved_batch
    from dk4tool.dialogue.hodram_B49_names_v2 import validate_scoped_names
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()};doc=data['manuscript'];rows=doc['records']+doc['typed_choice_records']
    assert prior['completed']==7205 and prior['candidate_sha256']==doc['current_ROM_sha256']==data['own_input']['current_ROM_sha256']==data['release']['candidate_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and data['release']['whole_clean_input_ROM_reconstruction_byte_exact'] and data['startup']['viewed']
    assert len(doc['records'])==14 and len(doc['typed_choice_records'])==2 and Counter(r['decision'] for r in rows)=={'revision':7,'retention':9}
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness','formatting']) for r in rows+data['names']['records'])
    assert doc['encoder']=='dialogue-relocatable-v1' and data['encoder_approval']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert data['encoder_approval']['only_root_encoder_metadata_changed'] and data['format_approval']['manuscript_sha256']==sha(Path(PROOFS['format_manuscript']).read_bytes())
    assert [r['english'] for r in rows]==[r['english'] for r in data['prior_native_manuscript']['records']+data['prior_native_manuscript']['typed_choice_records']]
    assert doc['names_packet_sha256']==sha(Path(PROOFS['names']).read_bytes()) and doc['source_current_final_references_complete']
    frozen=contract();validate_approved_batch(doc);validate_scoped_names(data['names'])
    assert data['policy_validation']['contract_sha256']==data['frozen']['contract_sha256']==sha(Path(PROOFS['contract']).read_bytes()) and data['policy_validation']['negative_count']==838
    assert data['policy_validation']['all_frozen_dependency_guards_remained_enabled'] and data['policy_validation']['all_protected_files_ROMs_registry_ledger_andsource_inputs_hash_exact'] and len(frozen['dependencies'])==445
    assert data['production_rebuild_positive']['entire_research_block_byte_exact'] and data['production_rebuild_positive']['source_andcurrent_full_block_inverse_exact']
    assert data['actual_view']['actual_frames']==20002 and data['tail_actual']['total_actual_frames']==40004 and data['FE_binding']['focused_actual_frames']==9862 and doc['total_actual_frames']==69868
    assert not data['tail_actual']['unresolved'] and data['tail_actual']['complete_body_name_orabsent_FE_header_holds']==134 and len(data['tail_actual']['groups'])==4
    assert not data['menu_actual']['unresolved'] and data['menu_actual']['all24_visible_source_English_label_samples_full_first_internal_final_glyphs_bounds_andnative_backgrounds_exact']
    assert data['FE_binding']['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model']
    assert data['format_approval']['all14_sheets_directly_viewed'] and data['format_approval']['all16_five_gates_true']
    for s in data['format_approval']['directly_viewed_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert data['stored']['all14_ink_planes_exact_to_already_viewed'] and data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    for g in data['tail_actual']['groups']:
        folder=Path(g['run_folder']);t=read(folder/'terminal.json');assert t['terminal'] and t['frames']==10001 and t['all_callbacks_readonly_andhost_slots_restored']
        for key in ['report','observer','menu_observer','readonly_menu_snapshots','run_plan']:assert sha(Path(t[key]).read_bytes())==t[key+'_sha256']
    for version in ['clean_Japanese','revised_English']:
        t=read(Path('work/analysis/Hodram_B49_FE_runs_v8419')/version/'terminal.json');assert t['terminal'] and t['frames']==4931 and t['all_callbacks_readonly_andhost_slots_restored']
        for key in ['report','observer','run_plan']:assert sha(Path(t[key]).read_bytes())==t[key+'_sha256']
    assert data['previous_final_review']['source_prose_and_completion_credit_added_once']==6
    return prior,data

'''

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_checkpoint_tools_v8429');assert not root.exists()
    path=Path('scripts/checkpoint_Hodram_B49_v8413b.py');source=path.read_text('utf8');a=source.index('PROOFS=');b=source.index('\ndef restore');c=source.index('def gates():');d=source.index("if __name__=='__main__':",c);p=source.index('        pending=dict(');q=source.index('        oldpending=',p)
    pending="""        pending=dict(status='B49-all16-five-gate-approved-frozen-policy838-independent-rebuild-positive-pending-independent-production-atomic-registered-integration',file_path='/data/SC1.DK4',blocks=[49],records=16,physical_speeches=14,typed_choice_labels=2,proposed_revisions=7,justified_retentions=9,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,all_sixteen_five_gates_true=True,exact_source_current_final_references_complete=True,automatic_body_pages=14,source_bound_ellipsis_forms=2,ordinary_New_World_wrap_scoped=True,source_macro_counts=dict(FI=0,FA=0,FO=0),line_count_infos=7,warnings=0,waivers=0,relative_sites=8,relocated_relative_cases=40,normal_end_value_carry_cases=25,native_whole_load_cache_paths=325,parent_entry_modes=650,total_actual_frames=69868,actual_emulator_runs=8,whole_script_actual_frames=20002,bounded_tail_actual_frames=40004,focused_FE_actual_frames=9862,whole_script_complete_holds=66,bounded_tail_complete_holds=134,unique_source_English_speech_displays=14,actual_menu_samples=12,actual_visible_label_samples=24,all_actual_limits_retained=True,policy_changed_input_rejections=838,frozen_dependencies=445,independent_reconstruction_positive=True,independent_production_native_actual_readers_semantic_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False)
"""
    result=derive(str(path),'scripts/checkpoint_Hodram_B49_v8429.py',{
        source[a:b]:'PROOFS='+repr(PROOFS)+'\nSUMMARY='+repr(SUMMARY)+'\nNEXT='+repr(NEXT)+'\n',source[c:d]:GATES,source[p:q]:pending,
        'Hodram_B49_checkpoint_v8413':'Hodram_B49_checkpoint_v8429',
        'editorial_handoff_verification_v8414':'editorial_handoff_verification_v8430',
        'editorial_handoff_verification_v8392':'editorial_handoff_verification_v8414',
        'Hodram_SC1B49_native_stored_references_actualsix_pending_focused_UI_registered_v8413':'Hodram_SC1B49_all16_format_policy838_pending_independent_atomic_registered_v8429',
        'unfinished_editorial_scope_v8413':'unfinished_editorial_scope_v8429',
        'superseded_by_native_stored_selected_actual_checkpoint':'superseded_by_format_policy_checkpoint',
        'Hodram_B49_native_stored_selected_actual_checkpoint':'Hodram_B49_format_policy_checkpoint',
        'B49 native14/storage/reference/actual6 verified;focused menu andFE next':'B49 all16fivegates/nativeactual69868frames/policy838 pass;production next',
        'new_emulator_runs=2,new_actual_frames=20002,new_research_ROMs=3':'new_emulator_runs=6,new_actual_frames=49866,new_research_ROMs=2',
        'B49native14/stored56/reference/actualsixpairs66holds;focusedUI_FE_policy_registered integration pending.':'B49all16fivegates/838policyrejections/69868actualframes;independentproduction_atomic_registered integration pending.',
        'V8413':'V8429','V8414':'V8430',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_prior_scope_leads_history_counts_families_records_andcurrent_registered_ROM_preserved=True,all_native_high_integer_constants_andmultiplicity_preserved=True,all_eight_B49_capture_jobs_terminal_andreaped=True,goal_turn_classification='progress',new_credit=0,full_goal_complete=False))
