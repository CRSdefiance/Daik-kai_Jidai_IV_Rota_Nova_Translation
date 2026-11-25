"""Publish303 contextual decisions and an initial full-width plan without completion credit."""
from collections import Counter
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/Maria_B58_B70_clean_20261109')
PROSE=Path('translations/maria_B58_B70_contextual_review_v2.json')

def main():
    doc=load(PROSE);plan_path=ROOT/'plan_v3/automatic_plans.json';plan=load(plan_path)
    release_path=Path('work/maria310_release_v1/registered_release_verification.json');release=load(release_path)
    names_path=ROOT/'scoped20_names_editorial_review_v3.json';names=load(names_path)
    assert len(doc['records'])==303 and Counter(r['decision'] for r in doc['records'])=={'revision':181,'retention':122}
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert doc['all303_paragraphs_read_in_ten_complete_exchanges']
    assert len(names['records'])==20 and all(not r['review']['formatting'] for r in names['records'])
    assert not plan['failures'] and len(plan['records'])==299 and sum(r['expected_native_pages'] for r in plan['records'])==301
    issues=[i for r in plan['records'] for i in r['base_QA']['issues']]
    assert not any(i['severity'] in ['error','warning'] for i in issues)
    tails=[dict(id=r['id'],lines=r['lines'],expected_pages=r['expected_native_pages'],
        finding='Five host rows leave a short continuation page; review phrase/page continuity before native approval. No prose shortening or weak-ending waiver is approved.')
        for r in plan['records'] if r['expected_native_pages']>1]
    assert {r['id'] for r in tails}=={'DK4_MES_B61_R0023','DK4_MES_B70_R0034'}
    glyphs=[dict(id=r['id'],current_nonASCII_characters=dict(Counter(c for c in r['current_comparison_paragraph'] if not c.isascii())))
        for r in doc['records'] if not r['current_comparison_paragraph'].isascii()]
    assert len(glyphs)==18
    assert doc['current_ROM_sha256']==release['candidate_sha256'] and not release['own_registered_startup_pending']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[PROSE,ROOT/'all303_clean_meanings_andindependent_drafts_v3.json',
        *[ROOT/n for n in ['B58_contextual_proposals_v1.json','B59_B61_contextual_proposals_v1.json','B62_B70_contextual_proposals_v1.json']],
        ROOT/'current_v1/current_effective.json',ROOT/'current_objects_v1/current_objects.json',
        ROOT/'scoped_names_macros_reference_v1.json',ROOT/'scoped_terms_reference_v1.json',names_path,
        ROOT/'contextual_prose_qualification_v1.json',ROOT/'final_exchange_reread_v1.json',
        ROOT/'formatting_v3/native_macro_measurements.json',ROOT/'formatting_v3/formatting_input_complete_indices_v1.json',
        ROOT/'formatting_v3/native_index_projection_v1.json',plan_path,ROOT/'plan_v3/diagnostics.json',release_path,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    proof=ROOT/'prose_initial_layout_checkpoint_v1.json';assert not proof.exists()
    save(proof,dict(source_objects=303,complete_exchanges=10,clean_meanings=303,independent_drafts=303,
        current_speech_bindings=299,current_choice_bindings=4,contextual_comparisons=303,
        proposed_revisions=181,justified_retentions=122,scoped_name_retentions=20,original_name_getters=40,
        reused_compatible_macro_alignment_cases=20,new_macro_alignment_cases=0,source_macro_occurrences=16,
        all_four_individual_prose_gates_pass=True,all_fifth_gates_false=True,
        host_speech_pages=301,host_speech_records=299,typed_choice_captions_not_rendered_as_speech=4,
        host_errors=0,host_warnings=0,source_line_count_information=118,
        current_nonASCII_target_records=glyphs,short_continuation_page_risks=tails,
        new_native_page_planes=0,new_directly_viewed_page_PNGs=0,new_batch_gameplay_observations=0,
        native_visual_storage_representative_gameplay_andregistration_pending=True,
        integrated_records_unchanged=20058,new_credit=0,full_goal_complete=False,evidence=evidence))
    summary=('Maria B58–B70 has303 whole-exchange editorial decisions:181 proposed revisions/122 justified retentions '
        'and20 scoped name retentions. Four prose gates pass;all formatting gates remain false. The full-width host '
        'plan has301 speech pages withzero errors/warnings;two short continuation-page risks remain,plus separate '
        'four-caption menu checks. Matching20 macro cases are reused. Fresh native/visual/stored/gameplay checks '
        'andregistration remain. Integrated20,058/registered465cb3c3/main/full scope are unchanged;zero new credit.')
    text='''# Maria303 contextual and initial-layout checkpoint — November 9, 2026

**All303 original objects in ten complete exchanges now have individual contextual decisions:181 proposed revisions and122 justified retentions.** Each has exact clean/current references,source meaning,exchange context,logical English and a specific rationale. The four prose gates pass;every formatting gate remains false. The release validator rejects the unformatted manuscript as required. No new review credit,ROM,gameplay coverage or promotion is claimed.

Continue from [the selected contextual manuscript](../translations/maria_B58_B70_contextual_review_v2.json). The immutable clean meanings and independent drafts were saved before this batch's current-English intake. Current English is now exposed:299 speeches are bound through the unchanged original native catalogue lookup andfour captions through their typed-object binder,on registered Maria310's own captain3 startup. There are no4100 style alternatives or dynamic selectors here. All earlier drafts,translations and executed attempts remain preserved.

The ten exchanges cover Cristina's London rescue,Gerhard/Janus/Charles recruitment,Julian's crown encounter,the miracle-pendant alternatives,the tomato gift,the banana/unknown-seed scene,Gerhard's lost sword andthe nukenin armor lead. Concrete corrections include reversed meal-payment perspective,still-Japanese former-sailor speeches,a false loan instead of a1000-gold gift,the wrong subject of the ninja death rule,misstated first-person actions,the paired fear-versus-Cristina comparisons,unsupported familiar/kinship andMaster addresses,missing Fernando result identities andthe explicit comic abridgment in Xien's boast. Branch-dependent Luck andSpirit results remain alternatives,not simultaneous rewards. Rumors,uncertain seeds andconditional item existence stay qualified.

Working English is retained with122 individual reasons,including urgent rescue fragments,the boy's direction,Mivor's theatrical responses,Janus's short negotiation/name misunderstanding,the animal cries,Fernando's baffled reaction,Gerhard's characterful Katzbalger description andformal/informal apologies. A complete final303-paragraph reread refined three awkward spoken collocations without changing facts or retention counts. The source is authoritative;passing structure alone is not prose approval.

Under `work/Maria_B58_B70_clean_20261109`, `scoped20_names_editorial_review_v3.json` has20 individual scoped name/role retentions andexact source fields/40 original nameplate/full-catalogue getters. Names in body andspeaker metadata are reconciled to Janus Pasar,Xien Yan,Julian Lopes andMivor Genz. Established Mihwa/美華 is retained from exact current consumers andearlier individual naming decisions;provisional Meihua is superseded andthis person remains distinct from Maria Huamei/華梅. Generic Shopkeeper,Trader,Shipwright,Boy,Lady andthe distinct Sailor/Retainer consumers are reviewed without turning internal regional metadata into surnames,nationality orservice relationships. This does not complete the global207-name review orapprove unused metadata.

`scoped_terms_reference_v1.json` binds the actual Silla Gold Crown,Tomato Seedling,Ninja Garb,Miracle Bullet Charm andSweeping Katzbalger item pointers,andthe exact Remodel/Luck/Spirit UI fields. The instruction now says Remodel,rather than old Modify orprovisional Refit. Gerhard says only old Katzbalger;the named inventory item is not silently inserted. Ninja Garb retains its rogue-ninja/black descriptors andreported armor function. The bullet pendant's reputation does not establish magic.

**Selected formatting input:** `formatting_v3/formatting_input_complete_indices_v1.json`. It marks all16 native token occurrences explicitly:11FI,oneFA andfourFO. Ordinary prose has no authored line breaks,alignment orpadding. The four choice source references include their complete native file/index metadata;299 speech indices come from the original binder,not invented catalogue indices for menu labels. `native_index_projection_v1.json` records this schema projection. Earlier incomplete formatting inputs remain historical.

`formatting_v3/native_macro_measurements.json` reuses the earlier20 original macro alignment cases after exact complete ARM9,COMMON,font,actor root/model block,native captain3 getter andfour default expansion matches. No macro case was rerun orrelabeled as new coverage. Current formatted-record expansions andpixels still need fresh checks. The failed preparation assumed a getter address was a raw data field;the selected producer verifies the actual native getter andunchanged instructions. The other stopped preparations concern zero-count token dictionaries,complete FE-preamble versus body-selector representation,typed reference metadata andlocal-variable scope. Their outputs do not approve a ROM orwaive any native check.

**Initial host layout:** `plan_v3/automatic_plans.json`, produced by `scripts.plan_maria303_v3`, has299 speech plans/301 expected pages,zero host errors/warnings and118 informational Japanese/English line-count differences. Progressive width remains216px;FE width228px. The12 FE bodies retain their distinct source controls,including explicitly labeled unseen boy voices,knocking,the dock/menu instruction,separate stat results andanimal cries. The matched fear comparisons stay on intact lines. The four captions in two menus are excluded from speech pagination andrequire their own menu checks.

Two concrete layout risks remain before approval: B61R23 andB70R34 each have five host rows andshort continuation pages. Review their phrase/page continuity with the selected prose;do not accept a weak-ending/orphan waiver,shrink good prose to a byte slot orrepeat historical engine investigation. There are18 current non-ASCII targets:ten untranslated sailor records,seven punctuation-only/mixed-punctuation cases andone full-width I in B59R56. Proposed paragraphs are ASCII;actual complete glyph rendering remains unproven for this batch. No native planes ornew PNG pages have been generated yet.

Next resolve those two page-boundary risks,then run fresh complete glyph/format/alignment/bounds/pagination checks on all299 bodies andseparate captions/names. Directly review every new page with readable sheets. Continue stored-command/allocation/branch/catalogue/load checks andrepresentative gameplay for distinct FE/progressive/menu transitions,pagination andthe corrected I. Existing Maria310 observations are not this batch's gameplay coverage. Do not exhaustively activate every conditional line orcollect guide photos.

The registered cumulative remains Maria310,`work/maria310_release_v1/all_routes_maria310_candidate.nds`,SHA-256 `465cb3c39c17c08844cbabe3f58e313a6388ea7ec7750877ee9b28eb4de8b05a`,with713 entries/114 accepted layers/48 checks andan exact clean-input patch. Preserve the market terminator allocation/pointers,the ASCII right-bound correction,the v2 multi-archive source25 guard andB54R507 storage amendment. Reconcile registry/current runtime again before building a successor. No main promotion without user acceptance.

Integrated totals stay20,058 =12,064 revisions +7,994 retentions;historical meaning/prose/draft total20,061 remains distinct. The303 in-progress objects are not new integrated credit. Native story objects remaining stay5,840 (Lil1,805/Maria4,035);shared shop/town/random/UI/player prose is separately tracked. Keep all unfinished storylines andearlier contextual passes,names,wrap/glyph work andother player-facing prose in scope. All ROMs,earlier translations,retentions andevidence are preserved. Deferred graphics artwork andthe later older-record technical re-audit remain separate. No process is live at this checkpoint;full goal active.
'''
    checkpoint(mutation=ROOT/'contextual_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria303:181 revisions/122 retentions;four prose gates pass;fresh native formatting next.',
            new_current_comparisons=303,proposed_revisions=181,justified_retentions=122,
            all_current_batch_five_gates_pending=False,all_current_batch_fifth_gates_pending=True,current_batch_not_yet_integrated=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Resolve two short-page risks;fresh-check299 bodies/four captions/20 names,view every page,thenstored/representative gameplay andregistration.'),
        additional_updates={'Maria_SC3_B58_B70_clean_20261109':dict(new_credit=0,current_comparisons=303,
            proposed_revisions=181,justified_retentions=122,source_only_no_current_English_read=False,
            current_English_not_consulted_for_this_scope=False,current_English_now_exposed=True,
            contextual_comparisons_names_terms_andall_five_gates_pending=False,all_four_prose_gates_pass=True,
            all_fifth_formatting_gates_pending=True,scoped_name_retentions=20,native_name_getters=40,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),
            selected_formatting_input='work/Maria_B58_B70_clean_20261109/formatting_v3/formatting_input_complete_indices_v1.json',
            selected_initial_plan=str(plan_path),selected_initial_plan_sha256=digest(plan_path),
            host_speech_pages=301,short_continuation_page_risks=tails,current_nonASCII_target_records=18,
            new_native_page_planes=0,actual_gameplay_observations=0,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria303_contextual_20261109.md',document_text=text,completed=20058,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Published303 contextual decisions andinitial full-width plan;20,058 integrated unchanged;zero new credit;full goal active.')

if __name__=='__main__':main()
