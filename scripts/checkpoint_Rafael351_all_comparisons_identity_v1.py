"""Save all351 individual comparisons,scoped identities andtwo real catalogue defects;no credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

DOC = Path('translations/rafael_B121_B140_contextual_comparison_v1.json')
NAMES = Path('translations/rafael_B121_B140_scoped_names_review_v2.json')
IDENTITY = Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
BUILD = Path('work/analysis/Rafael516_registered_build_v1_20261105')
LIVE = BUILD/'OS_live_all351_comparisons_checkpoint.json'

if __name__ == '__main__':
    doc,names,identity,live = map(load,[DOC,NAMES,IDENTITY,LIVE])
    assert (len(doc['records']),doc['proposed_revisions'],doc['justified_retentions'],doc['four_gate_passes']) == (351,197,154,225)
    assert len(doc['pending_name_term_IDs']) == 126 and doc['remaining_current_comparisons'] == 0
    assert all(r['review']['source'] and r['review']['context'] and r['review']['naturalness'] and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records']) == len(identity['actors']) == 22 and len(identity['fresh_actors']) == 14
    assert len(identity['qualified_reused_actors']) == 8 and len(identity['dynamic_roles']) == 6
    assert identity['scoped_name_review_sha256'] == sha(NAMES.read_bytes())
    particles = identity['two_unlocalized_full_name_particles']
    assert [p['actor_ID'] for p in particles] == [30,59]
    assert [p['proposed_pointer_field_offset'] for p in particles] == [1183560,1184488]
    assert all(p['proposal_only_not_a_ROM_orfield_write'] and p['never_rewrite_the_shared_Japanese_string_globally'] for p in particles)
    assert live['confirmed_live_by_OS'] and live['PID'] == 56664 and live['session'] == 20868
    assert not (BUILD/'completion.json').exists()
    summary = ('Rafael early story/all tutorials remain first. All351 B121–B140 complete-exchange comparisons arenowsaved: '
        '197 proposed revisions/154 justified retentions,225 four-prose-gate passes and126 intake name/role/item/UI holds;allfresh display gates pending. '
        'All351 clean drafts preserved. Found invented Ganges location,unsupported jade superlative,wrong figurehead-use assertion, '
        'uncertainty/idiom/nickname/subject losses,andfive full-width I letters acrosscurrentprose. '
        '22 publicnames reviewed with14 fresh/eight exact native reuses;six dynamic selectors/37 source entries bound withoutrole assignments. '
        'Fullcatalogue Dinis/Garcia stillcontain Japanese デ;scoped two-pointer de proposals saved,butno ROM/data write. '
        'Two mistaken draft rationale names corrected toactual Fernando Dias/Julian Lopes withoutchanging ROM names orrepeating getters. '
        '680-entry build20868/PID56664 remainsfreshly OS-confirmed live,collector errors empty;registry9bc4dd5e/core27ce unchanged. '
        '11845 integrated;verifiedcc71/main unchanged. No guidephotos,pruning orpromotion;full scope/ROMs/evidence preserved.')
    document = f'''# Rafael351 all comparisons and scoped-name findings — November 5, 2026

Rafael’s early story andall tutorials remain first. Full scope remains active,includingevery route,unfinished earlier contextual pass,shared town/shop/random exchange,names,glyphs/wrapping andremaining player-facing prose. Preserve alltranslations,ROMs andevidence. No guide photos,pruning,main promotion orcommit/push.

`{DOC}` nowcontains **all351 individual complete-exchange comparisons:197 proposed revisions and154 justified retentions**. Allsource/context/naturalness gates pass;225 records have allfour prose gates. The126 remaining intake flags cover scoped names,roles,items andUI labels. All formatting gates remainfalse. The351 clean-source meanings/drafts,the earlier125 tutorial decisions,andall exact source/current references andindividual reasons arepreserved. Nothing iscredited orintegrated yet.

Newstory findings include aninvented Ganges location wherethe Japanese onlysays India;an unsupported most-prized-jade claim;loss ofthe oldman’s personal youthful deed andhearsay aboutthe reward’s value;andconfusion between proposing a statue asafigurehead andasserting itsoriginalidentity. The bandit’s food idiom concerns lost livelihood,notliteral starvation. The political confrontation retains its slave-trade/plunder context andthe Proofs sought as apretext bythe greatpowers. No modernized motive,newrank orrelationship isadded.

The Cristina exchange retains the source’s private asides andgender/identity-reveal context. Correct source-specific Cristina/Clau spellings withoutforcing everyClaudio address intoa nickname:Arcadius explicitlycries Claudio duringthe ambush. Preserve the rescue child’s real grandfather whilekeeping the stranger’s familiar farewell distinct froma sibling relationship. Many existing short reactions,full clauses andpersonality calls alreadywork andhaveindividual retention reasons.

The treasure argument preserves Claudio’s enthusiasm,deflation andRafael’s later remorse. Julio’s legend qualifications andRafael’s mistaken certainty aredifferent viewpoints;do notcorrect the latter intoJulio’s position. Only inlegend couldmistakenlyassert nonexistence;the proposal says itisonly alegend. Localize the drinking-joke idiom asmaking Rafael thebutt ofjokes overdrinks. Avoid anunspecified tavern location andale type. B136 R76 hasanactual missing first-person subject inthe current Why amsuch afool sentence. Five full-width`Ｉ` letters acrossB128/B139/B136 haveproposed ASCII replacements;other currentJapanese punctuation forms areseparatelymarked forASCII rendering,notallcalled factual translation errors.

## Scoped names androles

`{IDENTITY}` is thelatestidentity receipt;`{NAMES}` isthelatest22-name review. Eight exact priorname proofs arereused,withfullARM9/COMMON/font/actor-array/individual-field equality. Fourteen actors havefresh clean/current intrinsic getters because theyarenewlyscoped orthe older complete ARM9 dependency differs. No newname data waswritten. Public names/roles areindividuallyretained withsource/context reasons;the full207-entry review remainsopen.

The six source selectors207,208,209,214,215,220 map toroles0,1,2,7,8,13. All37 ordinary/style source entries retain those native contracts. Inthisownstartup,role0 resolves toRafael andtheothers fall back toSailor151/voice4. Thisdoesnotassign thoseactors inoriginalconditional scenes,change rosters orprove natural activation. Never indexthese selectors inthe ordinary207-entry actor table.

Two **actualfull-catalogue text defects** areseparate fromthecorrect progressive headers:

- Actor30:current`Dinis デ Albuquerque`;proposed`Dinis de Albuquerque`.
- Actor59:current`Garcia デ Oviedo`;proposed`Garcia de Oviedo`.

The qualified proposal changes onlythe two middle-particle pointerfields atARM9 offsets1183560 and1184488 toequivalent existing read-only ASCII`de` data. It doesnotoverwrite shared Japanese strings,alter progressive names,allocate space ormodify anyROM. Thedata proposal isnotnative target/display/gameplay/registered-release proof. Implement itthroughan appropriately registered owned-data workflow,withthe existing eight stages preserved;do nothide itinsidea stage whoseownership excludes theseactors. Itisin-scope name/text-rendering work,notdeferred graphics artwork orthe later technical re-audit.

Preserved host-side corrections:identity helperv1 rejected the mistaken surname-column4 selection beforeanyoutput/ROM write;v2 usesactualparticle-column8. V2’s native data/labels werecorrect,buttwo human rationale strings incorrectlynamed actors20/26. Thealignment successor corrects those notes to**Fernando Dias andJulian Lopes**,preserving everygetter/field/role result andrerunningno native code. Keep thefailure andoldnotes ashistory;useonlythelatestaligned receipt/name manuscript.

## Continue efficiently

Reconcile the126 intake flags againstthe nowreviewed22 publicnames andsix role contracts;many no longerneednewinvestigation. Resolve the20 existingtutorial UI/itemlabel holds andremaining named items/towns/pirate references usingexactnative/current evidence. Inparticular,bindStaff ofGuidance,Snowfall Robe,sextant,Cape Verde,Sao Jorge,Vels/Valdes,Full/Half/Anchor,Map/Auto Travel andFlagship Priority ratherthan choosing a prose spelling inisolation. Both corrected full-name particles stillneedtarget checks andregistration. Thenformat the substantial351-object batch andfreshlycheck everychanged page;thereisno newbody/nameplane/gameplay approval fromthesecomparison/getter steps.

The earlier516-object cumulative build isunchanged. **Session20868/PID56664** remainsfreshly OS-confirmed live by`{LIVE}`;collector errors areempty. Registry9bc4dd5e,originalcore27ce0796,all114 accepted layers andall eight finalstages remainlocked. Poll thissamehandle/PID orits authoritativecompletion;quiet output isnotterminal anddoesnotauthorize a duplicate restart. This351 batchandthe two particle proposals arenotinthe runningbuild.

Onterminal0,follow [the registered516 checkpoint](editorial_Rafael516_build_next351_20261105.md):preparedfinal verifier,complete680-entry manifest,exactclean-input patch,ownplanned-startup identity/RAM binding andbothFernan getters beforeonce-only516credit. Reuse the4001-frame plannedcapture iffinalhash equalsa51c79e4. Original679’s MemoryError remainshistorical;preserve itandallROMs.

Integrated totals remain11845=6836 revisions+5009 retentions;historical source/prose11848 unchanged. Verified experimentalcc71ec06 andmain3cb827e4 remainunchanged. Fullgoal active.
'''
    evidence = {str(p):sha(p.read_bytes()) for p in [DOC,NAMES,IDENTITY,LIVE]}
    checkpoint(mutation='work/analysis/Rafael351_all_comparisons_identity_checkpoint_20261105',
        batch_key='Rafael_SC0_B121_B140_clean_20261105',
        batch_updates=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),contextual_comparisons=351,
            proposed_revisions=197,justified_retentions=154,four_prose_gate_passes=225,remaining_comparisons=0,
            pending_name_term_IDs=doc['pending_name_term_IDs'],scoped_names=str(NAMES),scoped_names_sha256=sha(NAMES.read_bytes()),
            scoped_identity=str(IDENTITY),scoped_identity_sha256=sha(IDENTITY.read_bytes()),
            scoped_public_names_reviewed=22,fresh_actor_getter_sets=14,exact_actor_getter_sets_reused=8,
            dynamic_selectors=[207,208,209,214,215,220],unlocalized_full_name_particles=2,
            two_full_name_pointer_proposals_only_no_ROM_writes=True,all_fifth_formatting_gates_pending=True,
            remaining_comparisons_UI_holds_andall_fifth_gates_pending=False,
            remaining_name_item_UI_holds_particle_fixes_andall_fifth_gates_pending=True,evidence=evidence,new_credit=0),
        additional_updates={
            'Rafael516_registered_cumulative_20261105':dict(new_credit=0,build_live_receipt=str(LIVE),
                build_live_receipt_sha256=sha(LIVE.read_bytes()),build_live_at_OS_checkpoint=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='All351 contextual comparisons saved;names/roles bound,two particle defects andUI/item holds remain',
                registered_build_live=True,registered_build_session=20868,registered_build_PID=56664,
                next_action='Poll20868/PID56664;reconcile126 holdflags withlatest22-name/six-role evidence,bindremainingUI/items andvalidate scoped catalogue de fixes. Fresh351 formatting afterward.')},
        summary=summary,document='docs/editorial_Rafael351_all_comparisons_names_20261105.md',document_text=document,completed=11845,
        protected={'translations/release_stack.json':'9bc4dd5e408f4e474844d25b1602d2cc4560db371d7c5ee4a92af8b3753cc6c9',
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            'out/all_routes_combined_help97_rafael330_20261105_candidate.nds':'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'})
    print('Checkpoint saved:351 comparisons/197 revisions/154 retentions,22 names/six roles;two catalogue particle corrections proposed.680 build20868/PID56664 live;11845 integrated,no newcredit orpromotion.')
