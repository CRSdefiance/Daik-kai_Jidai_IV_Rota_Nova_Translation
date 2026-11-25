"""Faithful natural fatigue increase/recovery status prose with one original amount."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
CONTEXT=Path('work/analysis/fatigue_status_source_v1587/source_amounts_and_original_expedition_context.json')
OUT=Path('translations/fatigue_status_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/fatigue_status_review_v1588')
if __name__=='__main__':
    assert not OUT.exists() and not ROOT.exists()
    context=read(CONTEXT);canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    review={308:('Fatigue increased by %s.','Fatigue increased by the supplied amount.',
        'Replace an unrelated split trade-good-description fragment with a complete,natural system message. Preserve exactly one original amount placeholder;do not turn the change into a total or invent percent,points,currency or health effects.',[3,5]),
        309:('Fatigue decreased by %s.','Fatigue recovered by the supplied amount;the original setter reduces the fatigue level.',
        'Express Japanese fatigue recovery naturally as decreased fatigue. Replace the telegraphic minus notation with an ordinary sentence,retain the positive magnitude placeholder and add no recovery beyond the source action.',[5,10,15])}
    rows=[]
    for n,(english,meaning,note,amounts) in review.items():
        row=deepcopy(next(r for r in context['records_and_neighbors'] if r['message_id']==n))
        assert bytes.fromhex(row['source_hex']).count(b'%s')==1
        assert english.count('%s')==1 and english==' '.join(english.split())
        row.update(id=f'COMMON_MESSAGE_{n}',source_family='fatigue-change-system2',speaker='Speakerless original546B8 system status',
            context=context['context'],consumer='original-signed-fatigue-action-ABF50-full-width-amount-546B8-modal',
            english=english,source_meaning=meaning,localization_note=note,editorial_decision='revise',canonical_source_hex=base[n].text.hex(),
            native_argument_count=1,source_native_macros=[],original_actual_amount_values=amounts,
            source_amount_format='ABF50-positive-full-width-CP932-decimal',compiled_hex=english.encode('ascii').hex(),
            authored_as_one_unwrapped_paragraph=True,review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-font-release-actual-events-pending')
        rows.append(row)
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'fatigue-status-one-source-amount-v1','file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':context['candidate'],'current_ROM_sha256':context['candidate_sha256'],
        'current_COMMON_sha256':context['COMMON_sha256'],'current_ARM9_sha256':context['ARM9_sha256'],
        'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),'records':rows,'revised':2,'retained':0,
        'no_authored_line_breaks_or_alignment':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1348,1492,144)
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not {308,309}&(done|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_review.json',before);save(OUT,doc)
    ledger['records_with_source_and_prose_pass']+=2;ledger['records_with_source_prose_drafts']+=2
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=2
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],308,309])
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted(set(drafts['native_message_IDs'])|{308,309})
    drafts['manuscripts'].append(str(OUT));drafts['manuscript_record_subsets_pending'][str(OUT)]=[308,309]
    ledger['coverage_units'].append({'id':'Shared-fatigue-status2-source-prose','native_message_IDs':[308,309],'manuscript':str(OUT),
        'source_context':str(CONTEXT),'status':'source-context-prose-reviewed;native-release-actual-pending','completed_entries_added':0,'full_goal_complete':False})
    ledger['formatting_watchlist']['fatigue_status2']={'native_message_IDs':[308,309],'manuscript':str(OUT),'source_context':str(CONTEXT),
        'source_one_percent_s_and_full_width_ABF50_amounts_preserved':True,'native_font_release_and_original_increase_recovery_pending':True}
    summary='V1588 source/context/prose-reviews fatigue statuses308/309,both revised. Restore the actual fatigue increase/recovery messages in natural English,preserve one original %s and native full-width amount3/5/10/15,and avoid inventing units or confusing the requested change with the stored total. Native glyphs,complete leading F,trailing period,substitutions,bounds,release and original Search/expedition events remain pending. Counts1348 complete,1494 source/prose,146 reviewed-incomplete COMMON;broader editorial and separate graphics/all18 plaques remain open. V1578 experimental,V1492 promoted;goal active.'
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1588-fatigue-status2-source-prose','manuscript':str(OUT),'proof':str(ROOT/'source_review_receipt.json'),
        'source_prose_reviews_added':2,'completed_entries_added':0,'full_goal_complete':False})
    save(ledger_path,ledger)
    save(ROOT/'source_review_receipt.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'completed':1348,'source_prose':1494,
        'reviewed_incomplete_COMMON':146,'source_prose_reviews_added':2,'completed_entries_added':0,'full_goal_complete':False})
    Path('docs/fatigue_status_v1588_source_review.md').write_text('# V1588 fatigue status source review\n\n'+summary+'\n\n308: '+rows[0]['english']+'\n\n309: '+rows[1]['english']+'\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1588 fatigue status2 source review\n\n'+summary+'\n\nSee [source review](fatigue_status_v1588_source_review.md).\n')
    print('Fatigue statuses source/prose reviewed:1348 complete,1494 reviewed,146 pending;original full-width amount retained,formatting/events not yet approved.')
