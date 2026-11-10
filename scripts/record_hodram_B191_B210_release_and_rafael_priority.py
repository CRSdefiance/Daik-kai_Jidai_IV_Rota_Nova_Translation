"""Record the completed release andunfinished early-game priority without duplicate credit."""
import gzip
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B191_B210_release_verified_20261104')
RAFAEL=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104')
LATER=Path('work/analysis/Hodram_B211_B230_clean_20261104')
LEDGER=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    mutation=ROOT/'priority_release_handoff_mutation_v1';document=Path('docs/editorial_hodram_B191_B210_release_rafael_priority_20261104.md')
    assert not mutation.exists() and not document.exists()
    release,completion=map(load,[ROOT/'registered_release_verification.json',ROOT/'completion_checkpoint.json'])
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert completion['new_credit']==373 and completion['counts']['completed']==10306
    assert release['candidate_sha256']=='88e9984f767a0fa14bde5e9ce07392d1fbcf44fb41a6815e4ca466740fb82a15'
    assert (release['complete_stack_entries'],release['accepted_layers'])==(664,114)
    prose_path=Path('translations/rafael_B42_B43_contextual_editorial_manuscript_v1.json');prose=load(prose_path)
    assert len(prose['records'])==40 and (prose['proposed_revisions'],prose['wording_retentions'])==(19,21)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    context_path=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')
    visual_path=context_path.with_name('direct_visual_andcontext_approval_v1.json');context,visual=map(load,[context_path,visual_path])
    assert context['candidate_sha256']==release['candidate_sha256'] and context['actual_captain_getter']==context['actual_route_word']==0
    assert visual['all_six_key_frames_directly_viewed'] and visual['context_sha256']==sha(context_path.read_bytes())
    before=LEDGER.read_bytes();prior=load(LEDGER);assert prior['records_editorially_completed']==10306 and not prior['full_goal_complete']
    assert prior['current_integrated_candidate']['sha256']==release['candidate_sha256']
    early_key='Rafael_SC0_B42_B43_early_tutorial_20261104';later_key='Hodram_B211_B230_clean_next_20261104';priority_key='editorial_execution_priority_20261104'
    assert not any(k in prior for k in [early_key,later_key,priority_key])
    ledger=dict(prior)
    ledger[early_key]=dict(file_path='/data/SC0.DK4',blocks=[42,43],total_editorial_objects=40,source_meanings_saved=40,logical_drafts=40,current_English_comparisons=40,
        proposed_revisions=19,justified_retentions=21,source_current_andindividual_findings=str(prose_path),source_current_andindividual_findings_sha256=sha(prose_path.read_bytes()),
        ordinary_actor_IDs=[0,4,5,6],ordinary_name_consumers=8,UI_terms=str(RAFAEL/'native_identity_and_UI_terms_v1.json'),
        current_Rafael_own_startup_context=str(context_path),current_Rafael_own_startup_context_sha256=sha(context_path.read_bytes()),
        actual_captain=0,actual_route=0,actual_context_frames=4001,actual_context_not_target_tutorial_gameplay=True,
        all_four_individual_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        remaining=['Qualified source00 full-preamble andRafael FI/FA/FO display binding','Fresh logical wrapping/native/visual pages','Stored relocation andrepresentative tutorial gameplay','Registered cumulative release/clean patch/own startup'],
        existing_opening_trade_andsea_reviews_keep_credit=True,new_credit=0,full_goal_complete=False,guide_photos=False)
    intake_path=LATER/'complete_clean_meanings_checkpoint_v1.json';intake=load(intake_path);assert intake['source_meanings_saved']==277
    ledger[later_key]=dict(**intake,checkpoint=str(intake_path),checkpoint_sha256=sha(intake_path.read_bytes()),
        native_ordinary_identity_checkpoint=str(LATER/'native_identity_checkpoint_v1.json'),native_UI_terms=str(LATER/'source_current_term_checkpoint_v1.json'),
        preserved_partial_drafts=114,preserved_draft_paths=[str(LATER/'B211_B215_64_clean_English_drafts_v1.json'),str(LATER/'B216_B220_50_clean_English_drafts_v1.json')],
        scheduling='Resume afterRafael early game/all tutorial priorities;preserve every saved record andproof without restarting.',prose_comparison_anddisplay_pending=True)
    ledger[priority_key]=dict(user_request='Prioritize early game,includingRafael’s storyline andall tutorials.',
        order=['Rafael B42/B43 resupply/first voyage andcrew assignment','Concrete early opening/tutorial wrap,glyph andlabel follow-ups while preserving completed reviews','Remaining shared beginner instructions/help/menu/town prose andRafael story progression','Resume preserved later-route work,thenremaining full scope'],
        current_batch=early_key,preserved_later_batch=later_key,no_scope_removed=True,graphics_andlater_older_record_technical_reaudit_separate=True,guide_photos=False)
    summary=('B191–B210 registered andcredited once:373 reviews,154 revisions/219 retentions;355 pages/four wrap fixes. '
        'All664 manifest entries,114 accepted layers,six final stages,exact clean patch andown startup pass.10306 complete;experimental88e9984f/main unchanged. '
        'User priority Rafael early game/all tutorials:40 B42/B43 comparisons saved,19 revisions/21 retentions;current ownRafael captain0/route0 context verified andviewed. '
        'Fresh formatting/native/visual/stored/tutorial gameplay remain;zero newtutorial credit. Later277 meanings/114 drafts preserved. Full scope/allROMs/evidence preserved;no live jobs or guide photos.')
    ledger['latest_checkpoint']=summary
    assert all(ledger[k]==v for k,v in prior.items() if k!='latest_checkpoint')
    protected={release['candidate']:release['candidate_sha256'],release['parent']:release['parent_sha256'],release['patch']:release['patch_sha256'],
        'translations/release_stack.json':release['registry_sha256'],'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    assert all(sha(Path(p).read_bytes())==h for p,h in protected.items())
    text=f'''# Registered B191–B210 release;Rafael early tutorials are next

The completed Hodram batch is integrated andcredited once:373 contextual reviews,154 revisions and219 individually justified retentions.70 scoped name/term retentions add no dialogue credit. All355 speech pages,21 captions and36 distinct name strings pass native/direct visual checks. Four layout corrections preserve prose. All540 relative cases,325 archive loads andfull serialized inverses pass;strict FE checks need no terminal-event exception. Reuse the [completed research](editorial_hodram_B191_B210_checked_20261104.md).

Experimental candidate: `{release['candidate']}`,SHA256 `{release['candidate_sha256']}`. Profile: `{release['profile']}`. All{release['complete_stack_entries']} manifest entries,{release['accepted_layers']} accepted layers and{release['passing_release_checks']} release checks pass. Allsix final runtime/name/static stages,including ASCII right bounds,remain. Onlytwenty SC1 blocks differ fromthe registered d14c24ba parent;allotherfiles/components,ARM9,COMMON,fonts,graphics andearlier names remain exact. Canonical main isunchanged andrequires user acceptance before promotion.

Patch: `{release['patch']}`,SHA256 `{release['patch_sha256']}`. Clean input SHA256 `{release['clean_input_sha256']}`. Applying the patch reconstructs the entire candidate byte forbyte. Manifest SHA256 `{release['manifest_sha256']}`;registry SHA256 `{release['registry_sha256']}`. Primary release/own-startup/once-only completion/exact373 per-record bindings: `work/analysis/Hodram_B191_B210_release_verified_20261104/`.

Actual research coverage remains six initialized English coldboots/98006frames,468 complete body-plane comparisons,204 record/page equivalences,36 headers,four menu samples andnine directly viewed QA sheets. All128 town,20 letter and17 parrot speech calls match the copied source command order. Book indices0/2 andtwo distinct two-choice defaults are observed;remaining branches are explicitly unvisited. These fixtures do not establish natural activation,original town layout/economic effects,earned progress,full routes orhardware behavior. The candidate’s ownordinary4001-frame Hodram startup passes allten exact priorRGB pairs andits ownfinal RAM/payload/getter checks. The first startup launch rejected capture-every0 before creating artifacts;the corrected positive interval preserves the required exact capture schedule. Both logs remain.

## Current priority: Rafael early game andall tutorials

All40 source speeches inSC0 B42/B43 now have complete source/current contextual comparisons:19 proposed revisions/21 justified retentions. Their source meanings andlogical drafts were saved before current-English extraction. Exact references andindividual findings: `translations/rafael_B42_B43_contextual_editorial_manuscript_v1.json`. The four prose gates pass;allformatting gates remain false andzero completion credit isadded.

Corrections include natural planning banter,Claudio’s explicit first-person boarding fantasy rather than an apparent attack instruction,Rafael’s personal loan-repayment promise,fleet growth rather than enlarging ships,andthe Sail Handler’s wind adjustment. The First Mate term matches the visible duty selector;an existing adjutant tooltip isqueued separately. Current captain prose,Ready?,Good grief,the recruiting exchange andthe exact X/Deck View instruction remain where they already work. Their legacy ordinary breaks will be regenerated. The current First isalready ASCII;preserve the registered glyph correction without counting it asa newfix.

Current native context isnow the candidate’s ownordinary Rafael coldboot,not Hodram RAM. No saves,savestates,roster,money,location orRNG overrides. Captain0/route0,complete staged payload,current getter code andreadonly RAM pass;allsix key QA frames were directly viewed. Context/approval: `work/analysis/Rafael_early_tutorial_registered_context_20261104/`. This isstartup/opening coverage,notB42/B43 gameplay. The explicit-protagonist runtime successor rejects a wrong requested captain;the original Hodram-only runtime remains strict andunchanged.

Next qualify the complete source00 preamble andRafael macro/default-name display dependencies,thenplanfresh wrapping andinspect every generated page. Keep the fullcaptain clause/name together where the validated width permits;do not shorten good prose tofit. Check native leading/internal/trailing glyphs,bounds,guards,pagination,stored relocation andrepresentative tutorial transitions. Integrate through a registered cumulative successor afternecessary checks pass. Existing completed opening117,trade12 andsea-actions26 retain credit;onlyconcrete wrap/glyph/label follow-ups need additional checks.

Source/draft/current records andUI bindings: `work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/` and`work/analysis/Rafael_early_tutorial_B42_B43_current_20261104/`. Thenprioritize remaining shared tutorial/help/menu/beginner prose andRafael’s story progression. Do not assume numeric block order proves early gameplay.

Later B211–B230 work remains saved:277 source meanings,114 logical drafts,23 ordinary actor bindings/46 consumers,18 equipment terms,two Amsterdam aliases andCharm. Style208 qualification,remaining drafts,current comparison anddisplay remainpending. Resume afterthe early-game priorities without restarting it.

Coverage is10306 completed:6158 integrated revisions/4148 retentions;historical source/prose/draft counters10309. Allprior keys,translations,retentions,ROMs andevidence arepreserved. No live jobs,main promotion,commit/push,pruning orguide photos. Every storyline/shared/town/random/player-facing text remains inthe full goal;graphics artwork andthe later older-record technical re-audit stayseparate.
'''
    updates={document:text}
    for name in ['editorial_handoff_current.md','editorial_efficiency_workflow.md','translation_progress.md','known_issues.md','todo.md']:
        path=Path('docs')/name;updates[path]='# Current verified editorial checkpoint - 2026-11-04\n\n'+summary+'\n\nContinue from [the verified release andRafael tutorial checkpoint]('+document.name+'). Reuse completed checks;earlier entries below arehistorical.\n\n'+path.read_text(encoding='utf-8')
    mutation.mkdir();backup=mutation/'ledger.before.json.gz';backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);plan=[]
    for i,(path,content) in enumerate(updates.items()):
        old=path.read_bytes() if path.exists() else None
        if old is not None:(mutation/f'{i}.before').write_bytes(old)
        plan.append(dict(path=str(path),before_sha256=sha(old) if old is not None else None,after_sha256=sha(content.encode('utf-8'))))
    save(mutation/'mutation_plan.json',dict(ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),documentation=plan,protected=protected,new_completion_credit=0,all_previous_ledger_entries_preserved=True))
    assert LEDGER.read_bytes()==before
    for entry,(path,content) in zip(plan,updates.items(),strict=True):
        assert (sha(path.read_bytes()) if path.exists() else None)==entry['before_sha256'];path.write_text(content,encoding='utf-8',newline='\n');assert sha(path.read_bytes())==entry['after_sha256']
    staged=LEDGER.with_name('editorial_review_current_v1.pending_rafael_priority_handoff.json');assert not staged.exists();staged.write_bytes(encoded);os.replace(staged,LEDGER)
    assert sha(LEDGER.read_bytes())==sha(encoded) and all(sha(Path(p).read_bytes())==h for p,h in protected.items())
    save(mutation/'verified_mutations.json',dict(completed=10306,new_completion_credit=0,new_unfinished_priority_entries=[early_key,later_key,priority_key],all_previous_keys_andcounts_preserved=True,main_unchanged=True,full_goal_complete=False,guide_photos=False))
    print('Verified373-review release and40-comparison Rafael tutorial priority saved;10306 completions preserved;full goal active.')
