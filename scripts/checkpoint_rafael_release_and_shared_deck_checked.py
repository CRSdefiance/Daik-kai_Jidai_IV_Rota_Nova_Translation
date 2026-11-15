"""Save the verified175-record release andfour checked shared tutorials without duplicate credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_release_verified_20261104')
SHARED=Path('work/analysis/Shared_Deck_four_panel_checked_20261104')
FINAL=Path('translations/shared_deck_four_panels_contextual_final_v1.json')
NATIVE=Path('work/analysis/Shared_Deck_current_native_v5_20261104/native_andstorage_verification.json')
CONNECTED=Path('work/analysis/Shared_Deck_connected_current_20261104/connected_verification.json')
ACTUAL=Path('work/analysis/Shared_Deck_actual_UI_20261104/representative_UI_verification.json')

if __name__=='__main__':
    release=load(ROOT/'registered_release_verification.json');completion=load(ROOT/'completion_checkpoint.json')
    assert completion['new_credit']==175 and completion['counts']['completed']==10521
    assert release['candidate_sha256']=='ee04bf6f954ecbdb15b01fb68b5754c5c38366a767ce8a40aec8bd04f2ed985e'
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert (release['complete_stack_entries'],release['accepted_layers'])==(666,114)
    final,native,connected,actual=map(load,[FINAL,NATIVE,CONNECTED,ACTUAL])
    assert len(final['records'])==4 and final['all_five_individual_review_gates_pass_in_research']
    assert len(native['cases'])==len(connected['cases'])==8 and actual['complete_body_texture_andRGB_comparisons']==7
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    pinned={Path(r['path']).resolve() for r in pins};added=[]
    research=Path('work/analysis/Rafael_B36_B41_rebuilt_20261104/reviewed_RESEARCH_ONLY.nds')
    for path in [research,*Path('work/rf_story_1104').rglob('*.nds')]:
        if path.resolve() not in pinned:
            pins.append(dict(path=str(path.resolve()),reason='Preserve complete Rafael registered build/research parent;all ROMs retained. SHA256 '+sha(path.read_bytes())))
            pinned.add(path.resolve());added.append(str(path))
    pinbackup=ROOT/'pins_before_final_handoff.json';assert not pinbackup.exists();pinbackup.write_bytes(before);save(pins_path,pins)
    summary=('Rafael B36–B41 registered andcredited once:175 reviews,76 revisions/99 retentions,four wrap fixes/two ASCII-I fixes; '
        '10521 complete (6253 revisions/4268 retentions). Experimental ee04bf6f passes666 entries/114 accepted layers/six final stages,exact clean patch andown Rafael startup;main unchanged. '
        'Four shared Deck panels now passfive-gate research:one First Mate revision/three retentions/four wrap preferences. '
        'Allfour existing slots/all31 pointers stay fixed;eight native andeight connected cases pass.21400-frame ordinary UI run bindsseven live consumer bodies tocomplete texture/RGB;four special bodies remain offline-only. '
        'Registered data integration remains;two catalogue-field proposals stay separate pending editorial/deployment. No live jobs;full scope/all prior work/ROMs retained;no guide photos.')
    document=Path('docs/editorial_rafael_release_shared_deck_checked_20261104.md')
    text=f'''# Verified Rafael story release;shared tutorial data is next

Previous goal turn made progress:175 individual reviews/names were sealed,registered direct/shared plans andnine rejections passed,build12117 started,andfour shared Deck panels were reviewed. This turn integrates/credits175 once andfinishes the shared panel research. The full editorial objective remains active.

## Verified cumulative Rafael release

Candidate: `{release['candidate']}`. SHA256 `{release['candidate_sha256']}`. Profile: `{release['profile']}`. Canonical accepted base remains `{release['canonical_base']}`,SHA256 `{release['canonical_sha256']}`. All666 manifest entries,114 accepted layers and24 release checks pass. Allsix runtime/name/static stages,ASCII right bounds,earlier names/fonts/graphics andthe40 B42/B43 tutorials arepreserved. OnlySC0 B36–B41 differ from c555f555;ARM9,COMMON andallother files/components areexact tothat verified predecessor.

Clean-input patch: `{release['patch']}`,SHA256 `{release['patch_sha256']}`. Clean ROM SHA256 `{release['clean_input_sha256']}`. The complete reconstructed ROM isbyte-exact. Manifest SHA256 `{release['manifest_sha256']}`;registry SHA256 `{release['registry_sha256']}`. Complete release/startup/once-only credit/exact175 source-current-final bindings arein `{ROOT}`.

Build12117 isterminal exit0;verify10787 isterminal exit0. Its exact ee04bf6f research identity wascoldbooted4001frames before final reconstruction;the verified finalwhole-ROM identity links that fresh own-Rafael RAM andallten exact reviewed RGB pairs to the registered candidate. The explicit V2 Rafael startup verifier passescaptain0/route0,current staged payload/native getters andprotected names. No old RAM overlay. All generated stages,research parents,candidates andclean reconstructions arepinned;no ROM ispruned. Added pins atthis checkpoint: {len(added)}.

Credit175 once:76 prose revisions/99 justified word retentions. Four layout fixes andtwo full-width I-to-ASCII corrections have separate evidence. Eleven progressive-name retentions add no dialogue credit. Actual selected scope remains16 utterances/18 pages/40 body and40 header comparisons inone10001-frame initialized QA sequence;159 utterances areoffline-only. All177 pages and400 branch cases werechecked offline;343 archive loads and12 fresh/674 reused handoffs pass. Natural event activation,original locations,earned chronology,fullroutes andhardware remainunvisited. B40 isstill a later rematch. No expanded gameplay claim follows fromintegration.

Current coverage:10521 completed,6253 integrated revisions,4268 retentions;historical source/prose/draft counters10524. All prior keys andrecord prefixes remainexact. Main3cb827e4 isunchanged andrequires user acceptance beforepromotion. No live jobs remain.

## Four shared Deck/room explanations

Final research manuscript: `{FINAL}`. Four individual five-gate reviews:one First Mate terminology revision andthree justified retentions. The earlier single First Mate With-clause draft ispreserved andreceives no duplicate credit. Natural wording follows the complete clean Japanese panels andthe current assignment terminology. The later live Deck instructions explicitly use Navigator as the named companion class;the Oars prohibition isnot limited to the navigation-duty role.

All prose remains one logical paragraph plus fixed-record PAD. The consumer now uses the accepted Refit27-cell,pair-safe formatter and168x108 bitmap with60 visible body rows. Four record-bound ordinary phrase preferences keep other locations,in sailor fatigue,from the guild,andcannot be assigned together. No wording isshortened forstorage andno translator-authored line/control spacing isintroduced. The original compiler’s pre-LF parity guard andallword/width/row checks remainunchanged. The final native sheet wasdirectly viewed.

Final native/storage proof: `{NATIVE}`. Eight native mode4/mode16 cases execute current own-Rafael code with every instruction bound to current original sections/staged payload. Native glyph codes,complete pixels,accepted Y+1 offset,right bounds,ABI,input/pixel canaries andall4MiB unchanged memory pass. The actual resource descriptor ispitch42/height108 for4-bit andpitch168/height108 for16-bit. Current geometry/cleanup/crop bytes exactly reuse the qualified V712 allocation proof; no historical RAM isoverlaid. Fixture surface,metrics andzero-origin getter areexplicit offline boundaries,not actual allocation/GPU claims.

Allfour compiled bodies fit their existing slots at1257508/76,1257584/48,1257632/68 and1257700/76. All31 pointer values andallocation starts stayunchanged. The complete540-byte pool and27 other labels,including accepted Refit centering andSpritsail,remain intact. Complete parent inverse restores every unowned ARM9 byte. The fixed-slot data changes have no code,font,heap,pagination orlayout effect.

`{CONNECTED}` connects the actual current108-row constructor,each original stored selector,the original macro copy,context andrenderer forfourrooms/twosecondary states. All eight full source-connected cases pass complete words/glyphs/pixels,full4MiB equality,stack/input/pixel canaries. Native source checks run at every executed instruction. The9072-byte allocator return is an explicit isolated test contract;native constructor dimensions/palette/resource andallfollowing renderer code execute. No actual allocator orGPU approval isinferred fromthat bridge.

## Honest live UI coverage

An unmodified inherited five-ship Copenhagen test battery wascoldbooted withthe data-only research image. Its original SHA256 febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731 remainsunchanged;no savestate ornew money,roster,location,RNG orcondition override wasused. This inherited test state isnot earned progress. Ordinary touchscreen/buttons navigate Refitting,Cancel remodeling,ship selection,return toPort,Deck View,Crew Setup andManuel Almeida’s Helm comment/Sailor Info. Incidental text isobserved only,no new editorial credit. The one invalid full-screen touch wasrejected before any input/state change;the corrected bottom-screen coordinates andallactions arein the command journal.

Session18138 ended normally at21400frames,withno callback errors. `{ACTUAL}` bindsseven ordinary live help bodies to a unique actual21CRemodelCabinInfoView object,its native resourceheader andreal9072-byte texture. All168x60 body indices andactualRGB ink/blank masks exactly match independent current GameAsciiFont decoding withthe accepted Y+1 position. Both QA sheets wereopened. The seven IDs are1286/1281/1248/1278/1247/1277/1282;these are compatible existing Refitting descriptions,not the four revised special static bodies. Allfour special bodies remain explicitly live-unvisited;their complete controlled native andstored-selector checks supply their individual coverage. This representative same-consumer test follows the current efficiency scope;do not claim natural conditional activation orindividually visited everyline.

Capture/report/readonly pause RAM: `work/emulation_v193/Shared_Deck_actual_UI_20261104/`. Research image/run-plan andQA: `work/analysis/Shared_Deck_actual_UI_20261104/`. The image isresearch only,witha whole serialized inverse to c555f555;do not hand it offas registered orpromote it.

## Preserve failed prototypes ashistory

The initial pool planner correctly rejected its536-byte historical descriptor against the current540-byte pool. Later accepted Refit centering andSpritsail changes werepreserved. The old168x84 geometry probe wasinapplicable afterthe accepted108-row allocator/layout change. The old caption fixture lacked current runtime-helper allowance. The first direct fixture omitted the resourceheight,causing a zero-row paint despitecorrect glyph events;it also needed the already accepted Y+1 offset inits independent pixel oracle. These werehost test-contract defects,not ROM defects. Initial trees/scripts/diagnostics andallpreviews remain. Use finalv5 plusconnected-current evidence;do not repeat orweaken guards in the rejected prototypes. The current validated formatter removes the historical continuation indents,so no pool expansion,shortened prose orpointer relocation isneeded.

## Next integration

The four panel research reviews arecomplete,withzero newcoverage credit until registered integration. Use a separately registered source-owned ARM9 data stage,not the component-preserving SC0 extension. The existing Abkhaz/Elysion stage isfixed toits historical qualified fields;preserve it unchanged. A successor data driver can callall six prior stages unchanged,then applythese four bounded C-string slots andverifycomplete current/target identities andinverse. The latest verified ee04bf6f ARM9 equals the tested c555f555 ARM9,so reuse these exact consumer/font/source/pointer proofs afterchecking that dependency;no need torepeat the UI navigation.

For efficiency,consider integrating the two already source/native-qualified catalogue middle fields inthe same new data successor after finishing their two individual final editorial gates:Pedro de Valdes andBarbarossa Fazul Hayreddin. They remainseparate typed ownership/proof records;no field isyet deployed. Proposals/native previews: `work/analysis/Rafael_B36_B41_name_field_proposals_20261104/owned_fields_proposal.json` and`work/analysis/Rafael_B36_B41_name_fields_native_20261104/native_name_fields_verification.json`. Their progressive names areunchanged andfull catalogue UI remainsunvisited. Do not grant global207-name approval. No need torepeat their exclusive-field/native/font/negative-case proofs ifallrelevant dependencies match.

Then continue Rafael early story/alltutorials,retaining the245 later clean speeches,all later Hodram drafts andall widerstory/shared/town/random/player-text scope. No guide photos,pruning,commit/push ormain promotion. Graphics artwork andthe later older-record technical re-audit remainseparate.
'''
    checkpoint(mutation=ROOT/'shared_deck_checked_handoff_mutation_v1',batch_key='shared_Deck_four_panel_contextual_20261104',
        batch_updates=dict(new_credit=0,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
            all_five_individual_gates_pass_in_research=True,formatting_andintegration_pending=False,registered_integration_pending=True,
            native_storage=str(NATIVE),native_storage_sha256=sha(NATIVE.read_bytes()),connected_native=str(CONNECTED),
            actual_representative_consumer_UI=str(ACTUAL),actual_frames=21400,actual_consumer_bodies=7,actual_target_special_bodies=0,
            target_four_paragraphs_offline_only=True,native_mode_cases=8,native_connected_cases=8,wrap_preferences=4,
            all31_pointers_andall_nonpanel_bytes_exact=True,remaining=['Register source-owned fixed-slot ARM9 data successor','Clean-input patch/own startup andonce-only credit']),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='shared_Deck_four_panel_contextual_20261104',
            Rafael175_batch_registered_andcredited_once=True)},
        completed=10521,summary=summary,document=document,document_text=text,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Verified175-record release andfour checked shared panels saved;10521 completions;no live jobs,full goal active.')
