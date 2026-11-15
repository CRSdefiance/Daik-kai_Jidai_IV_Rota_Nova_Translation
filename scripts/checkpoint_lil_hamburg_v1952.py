"""Record81 full-context Hamburg prose reviews; native/release credit pending."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Hamburg_checkpoint_v1952')
DOC=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')
CHOICES=Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v1.json')
SOURCE=Path('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json')
PROBE=Path('work/analysis/lil_Hamburg_body_probe_v1951c/body_only_prose_layout_research.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,choices,source,probe=map(read,(DOC,CHOICES,SOURCE,PROBE))
    rows=doc['records']+choices['records']
    ids=[r['id']for r in rows]
    assert len(ids)==len(set(ids))==81 and len(probe['rows'])==79
    assert probe['manuscript_sha256']==sha(DOC.read_bytes())
    assert not any('error'in r for r in probe['rows'])
    assert all(all(r['review'][k]for k in('source','context','localization','naturalness'))
        and r['review']['formatting']is False and r['source_meaning']and r['localization_note']for r in rows)
    assert sum(r['editorial_decision']=='revise'for r in rows)==46
    assert sum(r['editorial_decision']=='retain-wording'for r in rows)==35
    assert all(all(r['source_Japanese'].count(k)==r['english'].count('{MACRO:'+k+'}')for k in('FI','FA','FO'))for r in doc['records'])
    raw=LEDGER.read_bytes()
    ledger=read(LEDGER)
    before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1750,1866)
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not set(ids)&set(ledger['contextual_story_natural_dialogue_pass_v1871']['record_IDs'])
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']+=81
    ledger['records_with_source_prose_drafts']+=81
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']+=81
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    drafts=ledger['active_source_prose_drafts']
    for path,records in((DOC,doc['records']),(CHOICES,choices['records'])):
        drafts['manuscripts'].append(str(path))
        drafts['route_record_subsets_pending'][str(path)]=[r['id']for r in records]
    drafts.update(status='116-reviewed-COMMON-and81-Hamburg-source-context-prose-open',
        note='Stockholm51,London111 andSpeyer59 integratedV1945. Hamburg B74:79 speeches/two labels full-exchange reviewed;46 revisions35 retentions. Conservative bodies pass;private Gerhard/FE controls,full native fonts/choice/relocation/revised gameplay/release pending.')
    for unit in ledger['coverage_units']:
        if unit['id']=='Lil-Hamburg-B74-actual-context-unreviewed':
            unit.update(status='original-gameplay-captured;source-prose-reviewed-in-separate81-entry-unit',
                source_prose_unit='Lil-Hamburg-recruitment81-source-prose',source_inventory_alone_not_editorial_completion=True)
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=429,completed_route_records=348,
            next='Complete B74 private Gerhard/FE controls,full native font and choice checks,typed relocation and representative revised gameplay;then integrate through the preserved full registry. Continue the full all-routes/shared/random/player prose objective.')
    ledger['coverage_units'].append(dict(id='Lil-Hamburg-recruitment81-source-prose',file_path='/data/SC2.DK4',blocks=[74],record_IDs=ids,
        status='source-context-prose-reviewed;native-controls-fonts-map-revised-actual-release-pending',
        manuscripts=[str(DOC),str(CHOICES)],source_context=str(SOURCE),proposed_revisions=46,proposed_retentions=35,
        completed_entries_added=0,source_prose_reviews_added=81,full_goal_complete=False))
    ledger['formatting_watchlist']['Lil_Hamburg_recruitment81']=dict(status='source-prose-reviewed;full-native-display-pending',
        manuscripts=[str(DOC),str(CHOICES)],source_context=str(SOURCE),body_only_probe=str(PROBE),
        pending_scene_presentation_prefixes_and_record_IDs={p:[r['id']for r in doc['records']if r['source_presentation_prefix_hex']==p]for p in('10','fe')},
        actual_original79_speech_context_captured=True,original_Gerhard_portrait_and_three_FE_panels_actually_viewed=True,
        body_only_probe_not_full_Gerhard_or_FE_consumer_approval=True,typed_choice_IDs=[r['id']for r in choices['records']],
        complete_native_glyphs_bounds_pagination_private_scope_and_revised_transitions_pending=True)
    ledger['next_route_scene_editorial_packet']=dict(file_path='/data/SC2.DK4',block=74,source_context=str(SOURCE),
        manuscripts=[str(DOC),str(CHOICES)],source_prose_review_complete=True,editorial_review_complete=False,
        actual_original79_speeches_captured=True,actual_revised_scene_pending=True,source_relocation_reference_map_pending=True,
        note='Preserve the captured original79-speech recruitment/tutorial context. Map exact B74 Gerhard10 andFE3 system panels,then full native/fonts/typed choice and relocation/revised/release checks. No need tovisit every conditional line separately.')
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread']==fresh['fresh_pass_records_integrated']==221
    fresh['record_IDs']+=ids
    fresh.update(fresh_pass_records_explicitly_reread=302,fresh_pass_records_pending_native_actual_release=81,
        latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),
        coverage_note='Stockholm51,London111 andSpeyer59 reread and integrated. Hamburg81 reread asonecompleteexchange,source/prose reviewed,full native/revised/release pending. Other historical reviews require explicit reconciliation.')
    summary=('V1952 Hamburg81 clean-Japanese full-exchange prose review:46 proposed revisions and35 justified retentions. '
        'The wife misunderstanding,manners clash,Lil\'s defense ofCamille,limited apology,naval-admiral/private-fleet history,reluctant recruitment,title/first-name joke andboth battle-lesson choices preserve the emotional progression. '
        'Restore Ardelknatts/Camille,shipping/officers,private-fleet superlative,pirates laying low rather than vanishing,andthe distinction between named officers andhired sailors. '
        'Current native terms areBattery,Quarters andBoarding Leader. No literaluncle,marriage,formalGrandAdmiral rank,retirement orpermanent prior mentorship isinvented. '
        'All79 body-only paragraphs encode afterone faithful FE312 concision refinement;all source mechanics andruntime substitutions remain. Gerhard10/private source scope,FE3 native paper geometry/fonts/pagination,choice,typed relocation andrepresentative revised release gates remain pending. '
        'No newROM orcompletion credit:1750 historical completions(1316 revised434 retained),1947 source/prose reviewed. Fresh contextual pass302 reread,221 integrated,81 pending. '
        'RegisteredV1945,its exact clean-input patch andall prior ROMs remain preserved.116 incompleteCOMMON,allbroader routes/shared/town/random/player prose,separate graphics/all18plaques andlaterolder-recordtechnical re-audit remainopen. Fullgoalactive;V1492promoted.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append(dict(id='V1952-Hamburg81-source-context-prose',proof=str(ROOT/'checkpoint_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=81,full_goal_complete=False))
    for key in('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','unresolved_graphics_work',
        'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_with_source_and_prose_pass']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==1947
    assert len(set(fresh['record_IDs']))==302
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1952_pending.json')
    assert not pending.exists()and LEDGER.read_bytes()==raw
    save(pending,ledger);os.replace(pending,LEDGER)
    Path('docs/lil_hamburg_v1952_source_review.md').write_text('# V1952 Hamburg recruitment full-exchange review\n\n'+summary+
        f'\n\nManuscript: {DOC.as_posix()}\n\nChoices: {CHOICES.as_posix()}\n\nSource: {SOURCE.as_posix()}\n\nBody-only probe: {PROBE.as_posix()}\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as stream:stream.write('\n\n## V1952 Hamburg81 source/context/prose\n\n'+summary+'\n\nSee [review](lil_hamburg_v1952_source_review.md).\n')
    text=HANDOFF.read_text(encoding='utf-8')
    text=text.replace('# Current editorial handoff - V1948','# Current editorial handoff - V1952',1)
    text=text.replace('1866 source/prose reviewed.**','1947 source/prose reviewed.**',1)
    text=text.replace('Fresh V1871 contextual pass:221 explicitly reread and integrated(Stockholm51 +London111 +Speyer59).',
        'Fresh V1871 contextual pass:302 explicitly reread;221 integrated(Stockholm51 +London111 +Speyer59),81 Hamburg entries pending full native/revised/release checks.')
    text=text.replace('reviewed:1518 COMMON +348 SC2. No active reviewed-incomplete route drafts.',
        'reviewed:1518 COMMON +429 SC2.81 Hamburg source/prose entries remain reviewed-incomplete.')
    start=text.index('### Exact next work')
    end=text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    work=f'''## Current working unit: Hamburg B74 - V1952

{summary}

- Source: {SOURCE.as_posix()};79 speeches,123 native commands andone two-label choice at3504. B74clean/current hashes andevery complete preamble remain exact inregisteredV1945.
- Prose: {DOC.as_posix()};choices:{CHOICES.as_posix()}.46 revisions35 retentions;all retained wording machine-matches old English after onlystorage whitespace,ASCII I andpunctuation normalization. Per-record source/context/localization/naturalness true,formatting false.
- Body-only probe:{PROBE.as_posix()};79/79 encode. V1 FE312 exceeded four conservative rows;v2 usesAs usual whilekeeping both controls,normal-sailing comparison,automatic firing andenemy-range trigger. This isnot fullFE geometry approval.
- Gerhard10 original portrait/nameplate atframe52110 andthreeFE panels73560/74550/74880 actually viewed. Original source/context proof1935b covers79 speeches,join panel andtutorialchoice0. No need toredo equivalent original gameplay. FE mustkeep itsseparate original paper consumer.
- Native UI terms:02086314 role8 Boarding Leader,role9 Gunner;all4MiB unchanged. CleanARM9 offsets12FFFC/130008 map海兵詰所/武装砲台 tocurrentQuarters/Battery;do not restorelegacyMarine Quarters/Gun Deck innew tutorial prose.
- Naval admiral isexplicit source. Great describesCamille\'s admiration,not aformalGrandAdmiral rank;pastprivate-fleet command doesnot establish retirement. Pirateslaylow ratherthan literallyvanish. Wife isamistakenquestion immediatelydenied;おじさん isnot literaluncle. Gerhard andLil retaintheir mutualdislike afterhis apology andconditional offer.

### Exact next work

1. BindB74 privateGerhard10 andFE3 complete controls tooriginal source/runtime andthe existing actual captures. Globalprofiles stayunchanged. ProveFE paper geometry/fonts/pagination separately fromprogressive dialogue.
2. Runall79 complete nativefont/macro checks,typed choice UI/VM checks andfull123-command relocation/reference proof. Resolve actual warnings narrowly;approve individual formatting gates andbatch gate metadata onlyafterthe checks.
3. Use representative revised gameplay andfocused tests forthe distinct FE/joins/choice/transition behavior. Integrateafternecessarychecks througha newprofile inheritingthe completeV1945 stack;verify exactclean-input patch andstartup beforecompletioncredit.
4. Continueevery remaining storyline,earlier translation,shared town/shop/randomscene andplayer-facing prose. Historical1529 reviews needexplicit reconciliation;116 COMMON remainincomplete. Graphics/all18plaques andlater older-recordtechnical re-audit remainseparate/open.

Current verifiedsnapshot:E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY/frame_093780_arm9_ram.bin;wholeROM exactregisteredV1945. Events74/128 complete,B25aftermath incomplete. Amsterdamdye andnativecatalogPedro デ Valdes remainunresolvedseparateleads. Alltestjobs terminal;preserveallROMs andearliertranslations,V1492promoted.

'''
    HANDOFF.write_text(text[:start]+work+text[end:],encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        body_probe=str(PROBE),source_prose_reviews_added=81,proposed_revisions=46,justified_retentions=35,
        historical_completed_unchanged=1750,source_prose_reviewed_after=1947,fresh_contextual_reread=302,fresh_contextual_integrated=221,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        no_ROM_orfull_native_revised_actual_orcompletion_claim=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_reviewed=1947,historical_complete=1750,fresh_contextual_reread=302,integrated=221,
        Hamburg_pending=81,full_goal_remains_active=True))
