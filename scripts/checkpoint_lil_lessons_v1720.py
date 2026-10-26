"""Record64 source/prose reviews while preserving all unfinished native gates."""
from copy import deepcopy
from pathlib import Path
import json
import os

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lessons_checkpoint_v1720')
PACKET=Path('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
MANUSCRIPT=Path('translations/lil_lessons_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_lesson_choices_editorial_draft_v1.json')


if __name__=='__main__':
    assert not ROOT.exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');raw=ledger_path.read_bytes()
    ledger=read(ledger_path);before=deepcopy(ledger)
    doc,menus,packet=map(read,(MANUSCRIPT,CHOICES,PACKET))
    rows=doc['records']+menus['records'];ids=[r['id'] for r in rows]
    assert len(ids)==len(set(ids))==64
    assert sum(r['editorial_decision']=='revise' for r in rows)==45
    assert sum(r['editorial_decision']=='retain-wording' for r in rows)==19
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in rows)
    assert len([r for r in doc['records'] if r['source_presentation_prefix_hex']=='fe'])==9
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1568)
    assert not any(u['id']=='Lil-sailing-lessons64-source-prose' for u in ledger['coverage_units'])
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']
    assert packet['current_ROM_sha256']=='251594f89f950f1deb68d6359b6861d6f4a96eb8e9a9045c148d6d6cb64b1201'
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==144
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_review.json',before)
    ledger['coverage_units'].append({'id':'Lil-sailing-lessons64-source-prose','file_path':'/data/SC2.DK4',
        'blocks':[120,23],'record_IDs':ids,'speech_objects':60,'choice_labels':4,
        'status':'source-context-prose-reviewed;native-branches-FE-layout-relocation-integration-and-actual-pending',
        'manuscripts':[str(MANUSCRIPT),str(CHOICES)],'source_context':str(PACKET),
        'proposed_revisions':45,'proposed_retentions':19,'completed_entries_added':0,'full_goal_complete':False})
    ledger['records_with_source_and_prose_pass']+=64
    ledger['records_with_source_prose_drafts']+=64
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']+=64
    drafts=ledger['active_source_prose_drafts']
    for path,records in [(MANUSCRIPT,doc['records']),(CHOICES,menus['records'])]:
        drafts['manuscripts'].append(str(path));drafts['route_record_subsets_pending'][str(path)]=[r['id'] for r in records]
    drafts.update(status='144-reviewed-COMMON-and64-Lil-lesson-source-prose-drafts-open',
        note='B22 opening49 is complete in V1711. B120/B23 lessons now have60 speech/system drafts and4 choice-label drafts;all64 remain incomplete. Earlier144 COMMON and broader prose remain open.')
    ledger['lil_lessons_editorial_v1720']={'source_context':str(PACKET),'speech_manuscript':str(MANUSCRIPT),
        'choice_draft':str(CHOICES),'native_choice_labels':'work/analysis/lil_lesson_choices_v1718/native_two_choice_labels.json',
        'allocation_probe':'work/analysis/lil_lessons_editorial_v1719/allocation_probe_NOT_visual_approval.json',
        'new_source_prose_reviews':64,'proposed_revisions':45,'proposed_retentions':19,
        'all9_FE_panels_separate_consumer_review_pending':True,
        'nested0100_lengths_choice_offsets_external_references_and_branch_gameplay_pending':True,
        'new_completed_entries':0,'full_goal_complete':False}
    ledger['formatting_watchlist']['Lil_sailing_lessons64']={'status':'source-prose-drafts-open',
        'source_context':str(PACKET),'manuscripts':[str(MANUSCRIPT),str(CHOICES)],
        'no_shortening_to_fit_old_slots':True,'nineteen_fixed_allocation_encodes_not_visual_approval':True,
        'forty_one_fixed_failures_including_nine_FE_panel_profile_rejections':True,
        'all_nested_branch_lengths_choice_labels_speaker_headers_controls_and_macros_must_be_preserved':True,
        'leading_trailing_glyphs_uniform_left_origin_bounds_pages_and_transitions_pending':True}
    ledger['next_route_scene_editorial_packet'].update(source_context=str(PACKET),source_prose_review_complete=True,
        editorial_review_complete=False,manuscripts=[str(MANUSCRIPT),str(CHOICES)],
        note='B120 andlinkedB23 source/prose now reviewed. Next native tasks:mapFE panelconsumer andnested0100/2100 references;full fonts/layout andactualbranches before release.')
    summary=('V1720 adds64 clean-source/context/prose reviews for Lil B120/B23 lessons:60 speeches/system objects plus4 choice labels,45 proposed revisions19 retentions. '
        'Complete recursive original-native inventory finds27 B120 and33 B23 speech commands,including nested0100 branches;independent raw header counts match. '
        'All124 nested command offsets/extents/ancestor paths match clean/current. Eight original two-choice clean/current label pointers/counts/ABI/guards pass. '
        'Current macro/catalog outputs are captured with actual Lil state and whole4MiB preservation;FE macro probes do not certify their distinct panel consumer. '
        'Correct B23 admiral-offer direction and surprise about unfinished lessons,restore omitted explanations,and use established Sail Handler/Half Open/Full Open. '
        'Drafts keep complete English;19 fit old allocations and41 fail capacity orFE-profile gates. No warnings waived,no renderer orROM changed,andno completion credit. '
        '1424 complete(1076 revised348 retained),1632 source/prose reviewed,144 reviewed-incomplete COMMON plus64 route drafts andbroader untouched prose. '
        'V1711/exact patch remains current experimental;V1492 promoted. Full editorial goal active,separate graphics/all18 plaques andlater older-record re-audit remain open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1720-Lil-lessons64-source-prose',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':64,'full_goal_complete':False})
    assert ledger['current_integrated_candidate']==before['current_integrated_candidate']
    assert ledger['unresolved_graphics_work']==before['unresolved_graphics_work']
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']
    assert ledger['completed_editorial_record_counts_by_file']==before['completed_editorial_record_counts_by_file']
    assert ledger['records_with_source_and_prose_pass']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==1632
    assert ledger['goal_status']=='active' and ledger['full_goal_complete'] is False
    pending=ledger_path.with_name('editorial_review_current_v1720_pending.json')
    assert not pending.exists() and ledger_path.read_bytes()==raw
    save(pending,ledger);assert read(pending)==ledger and ledger_path.read_bytes()==raw
    os.replace(pending,ledger_path)
    handoff_path=Path('docs/editorial_handoff_current.md');handoff=handoff_path.read_text(encoding='utf-8')
    save(ROOT/'handoff_before_review.json',{'text':handoff,'sha256':sha(handoff_path.read_bytes())})
    assert handoff.startswith('# Current editorial handoff - V1715')
    handoff=handoff.replace('# Current editorial handoff - V1715','# Current editorial handoff - V1720',1)
    handoff=handoff.replace('1568 source/prose reviewed. Exact earlier144','1632 source/prose reviewed;64 new B120/B23 lesson drafts remain incomplete. Exact earlier144',1)
    old='Next: create clean Japanese/current/runtime context packet for B120 and linked lesson branches,then review prose and source controls before authoring. Alternatively complete exact earlier144 pending COMMON entries where original contexts are available.'
    new=('Next:source/prose for B120 andB23 is NOW REVIEWED in translations/lil_lessons_editorial_manuscript_v1.json (60 speeches/system records) and translations/lil_lesson_choices_editorial_draft_v1.json (4 labels). '
        '45 proposed revisions19 retentions;none complete. Full clean/current/native-catalog context:work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json. '
        'Original two-choice pointer/count proof:work/analysis/lil_lesson_choices_v1718/native_two_choice_labels.json. '
        'Map FE system-panel consumer and full nested0100/2100 length/reference/branch behavior before authoring relocation or new profiles. '
        'B22 profile is only an allocation probe here:19 encode,41 reject capacity/FE;do not shorten faithful prose,waive warnings automatically,or add FE globally. '
        'Full nativefonts,actual branch selection/pages/transitions,registered integration andexactpatch all remain pending. '
        'Use Sail Handler andHalf Open/Full Open consistent with docs/crew_roles_v326.md andcurrentHELP83. B23 R44 incorrectly said Want my job;draft restores Camille offering to become admiral. '
        'Alternatively complete exact earlier144 pending COMMON entries where original contexts are available.')
    assert old in handoff;handoff=handoff.replace(old,new,1)
    handoff+='\n\n## Latest source/prose checkpoint V1720\n\n'+summary+'\n\nEvidence:work/analysis/lil_lessons_checkpoint_v1720/checkpoint_receipt.json. No emulator currently live;all current jobs terminal. No new ROM orfinal guide captures this checkpoint. Failed V1715 completion producer expected retain instead of actual retain-wording;V1715b completed correctly,with both sources preserved.\n'
    handoff_path.write_text(handoff,encoding='utf-8')
    Path('docs/lil_lessons_v1720_source_review.md').write_text('# V1720 Lil sailing andcrew lesson source review\n\n'+summary+'\n\nSee current handoff for exact files and next native gates. No new ROM orcompletion claim.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1720 Lil lessons64 source/prose review\n\n'+summary+'\n\nSee [source review](lil_lessons_v1720_source_review.md).\n')
    paths=[PACKET,MANUSCRIPT,CHOICES,Path('work/analysis/lil_lesson_choices_v1718/native_two_choice_labels.json'),
        Path('work/analysis/lil_lessons_editorial_v1719/allocation_probe_NOT_visual_approval.json')]
    save(ROOT/'checkpoint_receipt.json',{'candidate':packet['current_ROM'],'candidate_sha256':packet['current_ROM_sha256'],
        'source_prose_reviews_added':64,'completed_entries_added':0,'completed':1424,'revised':1076,'retained':348,
        'source_prose':1632,'reviewed_incomplete_COMMON':144,'pending_new_route_texts':64,
        'proofs':{str(p):sha(p.read_bytes()) for p in paths},'no_ROM_registry_or_graphics_change':True,
        'all_jobs_terminal':True,'ledger_sha256':sha(ledger_path.read_bytes()),
        'handoff_sha256':sha(handoff_path.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('64 new source/prose reviews recorded:1632 reviewed,1424 complete;all64 new drafts remain open. V1711 unchanged;full goal active.',flush=True)
