"""Source/prose review of the original optional Experience notice310."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_review_v1631')
SOURCE=Path('work/analysis/hot_spring_notice_source_v1627/optional_hot_spring_Experience_notice310_source.json')
OUT=Path('translations/hot_spring_notice_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    context=read(SOURCE);row=deepcopy(next(r for r in context['records_and_neighbors'] if r['message_id']==310))
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(context['candidate'])
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    original=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    assert original[310].text.hex()==row['source_hex'] and sha(Path(context['candidate']).read_bytes())==context['candidate_sha256']
    row.update(id='COMMON_MESSAGE_310',source_family='hot-spring-optional-Experience-system-notice',
        speaker='Speakerless original546B8 system notice',context=context['context'],consumer='original-no-argument-546B8-literal-modal',
        english='The hot spring boosted Experience.',source_meaning='The benefits of the hot spring increased the stat identified as Experience.',
        localization_note='Use a complete natural system message and preserve the hot spring as the cause. Experience is the quoted source stat name. Do not invent a recipient,party-wide effect,numeric amount or full-fatigue reset. Remove legacy authored indent and line break;native formatting is still a separate gate.',
        editorial_decision='revise',canonical_source_hex=base[310].text.hex(),native_argument_count=0,source_native_macros=[],
        authored_as_one_unwrapped_paragraph=True,review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
        status='source-context-prose-reviewed;native-release-original-optional-notice-pending')
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'hot-spring-experience-original-single-line-v1','file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':context['candidate'],'current_ROM_sha256':context['candidate_sha256'],
        'current_COMMON_sha256':sha(current.read_file('/COMMON/MESFILE.DK4')),'current_ARM9_sha256':sha(current.read_file('/__arm9__.bin')),
        'source_context':str(SOURCE),'source_context_sha256':sha(SOURCE.read_bytes()),'records':[row],'revised':1,'retained':0,
        'no_authored_line_breaks_or_alignment':True,'no_runtime_argument_or_source_macro_added':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1507,157)
    assert 310 not in ledger['reviewed_but_incomplete_COMMON_IDs'] and not any(310 in f.get('native_message_IDs',[]) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_review.json',before);save(OUT,doc)
    ledger['records_with_source_and_prose_pass']+=1;ledger['records_with_source_prose_drafts']+=1;ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=1
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(ledger['reviewed_but_incomplete_COMMON_IDs']+[310])
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted(drafts['native_message_IDs']+[310]);drafts['manuscripts'].append(str(OUT));drafts['manuscript_record_subsets_pending'][str(OUT)]=[310]
    ledger['coverage_units'].append({'id':'Shared-hot-spring-Experience-notice1-source-prose','native_message_IDs':[310],'status':row['status'],'manuscript':str(OUT),'completed_entries_added':0})
    ledger['formatting_watchlist']['hot_spring_Experience_notice310'].update(status=row['status'],manuscript=str(OUT),not_in_completed_or_reviewed_counts_yet=False,
        reviewed_source_prose_but_not_completed=True,native_font_release_and_original_optional_notice_pending=True)
    ledger['research_checkpoints'].append({'id':'V1631-hot-spring-notice-source-prose','proof':str(ROOT/'source_review_receipt.json'),'source_prose_reviews_added':1,'completed_entries_added':0,'full_goal_complete':False})
    assert ledger['records_editorially_completed']==before['records_editorially_completed'] and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==158
    save(lp,ledger);save(ROOT/'source_review_receipt.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'source_context':str(SOURCE),'source_context_sha256':sha(SOURCE.read_bytes()),
        'completed':1350,'source_prose':1508,'reviewed_incomplete_COMMON':158,'completed_entries_added':0,'native_release_and_actual_optional_notice_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Notice310 source/prose reviewed:1350 complete,1508 reviewed,158 pending. No native/release/actual approval yet.')
