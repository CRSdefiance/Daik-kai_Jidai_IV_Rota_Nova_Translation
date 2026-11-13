"""Approve51 native font planes;preserve relocation/revised-gameplay gates."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_stockholm_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_font_approval_v1859')
OLD=Path('translations/lil_Stockholm_encounter_editorial_manuscript_v1.json')
NEW=Path('translations/lil_Stockholm_encounter_editorial_manuscript_v2.json')
FONT=Path('work/analysis/lil_Stockholm_fonts_v1858/all51_native_macros_and_complete_font_planes.json')
CONTROL=Path('work/analysis/Gerhard_story_control_proof_v1857/original4000_prefix10_Gerhard_live_mapping.json')
CONTEXT=Path('work/analysis/lil_Stockholm_context_audit_v1855/original_Stockholm36_branch_and_three_fixture_audit.json')
BRANCH=Path('work/analysis/lil_Stockholm_branches_v1853/original_relative_skip_operand_proof.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()and not NEW.exists()
    doc=deepcopy(read(OLD));fonts=read(FONT);control=read(CONTROL);context=read(CONTEXT);branches=read(BRANCH)
    assert len(fonts['cases'])==51 and not fonts['failures']and fonts['native_macro_calls']==408
    assert sha(OLD.read_bytes())==fonts['manuscript_sha256']
    assert control['only_leading0x10_in_exact_B27_source_and_exact_runtime_may_be_added_to_private_profile']
    assert len(branches['operands_requiring_adjustment_when_resizing'])==24 and len(branches['cases'])==240
    assert len(context['original_speech_observations'])==36 and len(context['unvisited_original_speech_IDs'])==15
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[27]
    base=get_dialogue_profile(doc['dialogue_profile']);before=base.leading_speaker_bytes
    scoped=profile_for(arm,block);assert scoped.leading_speaker_bytes==before|{0x10} and base.leading_speaker_bytes==before and 0x10 not in before
    negative=[]
    for label,altered_arm,altered_block in [('wrong_runtime',bytes([arm[0]^1])+arm[1:],block),
        ('wrong_source_block',arm,block[:-1]+bytes([block[-1]^1]))]:
        try:profile_for(altered_arm,altered_block)
        except ValueError as error:negative.append({'case':label,'error':str(error)})
        else:raise AssertionError('Unbound profile accepted:'+label)
    gerhard=next(r for r in doc['records']if r['source_presentation_prefix_hex']=='10')
    for label,source,target,profile in [('global0x10_still_rejected',bytes.fromhex(gerhard['source_hex']),gerhard['english'].removesuffix('{PAD}'),base),
        ('unmapped0x11_still_rejected',b'\x11'+bytes.fromhex(gerhard['source_hex'])[1:],gerhard['english'].removesuffix('{PAD}').replace('{SPEAKER:10}','{SPEAKER:11}'),scoped)]:
        try:encode_relocatable_dialogue(source,target,profile)
        except ValueError as error:negative.append({'case':label,'error':str(error)})
        else:raise AssertionError('Unknown control accepted:'+label)
    cases={r['id']:r for r in fonts['cases']};waivers=[]
    for row in doc['records']:
        native=cases[row['id']]
        assert native['whole_native_independent_font_plane_exact']and native['all_glyphs_complete_in_order_unique_cells_within216x64']
        assert native['all_continuation_visible_origins_equal_first_row_zero']
        compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),scoped)
        assert compiled.encoded.hex()==native['encoded_hex']
        for d in native['diagnostics']:
            assert d['severity']=='warning'and d['code']=='line-break-count'
        if native['diagnostics']:
            row['qa_waivers']=['line-break-count']
            row['qa_waiver_reason']='The Japanese physical line count is not an authored English pause. This full paragraph preserves its source facts andexpressive punctuation;the exact native font plane was reviewed withall leading/trailing glyphs,zero row origins andat mostfour rows. '+native['diagnostics'][0]['message']+'. No weak-ending,overflow orcontrol warning iswaived.'
            waivers.append({'id':row['id'],'code':'line-break-count','reason':row['qa_waiver_reason']})
        row['review']['formatting']=True;row['compiled_hex']=native['encoded_hex']
        row['native_complete_font_plane_sha256']=native['native_font_plane_sha256']
        row['formatting_scope']='Size-independent one-paragraph native layout only;fixed PAD is anallocation probe,not approved relocated bytes orrevised gameplay.'
    assert len(waivers)==18 and len(negative)==4
    ROOT.mkdir(parents=True)
    visual={'all7_sheets_and51_complete_native_panels_actually_viewed':True,
        'source_gloss_prose_speakers_and_scene_neighbors_reviewed':True,
        'complete_first_last_letters_and_zero_continuation_origins_verified':True,
        'all51_native_independent_planes_and408_macro_alignment_cases_pass':True,
        'only18_source_vs_automatic_linebreak_count_warnings_narrowly_waived':waivers,
        'private_profile_only_Gerhard0x10_exact_B27_runtime_source_bound':True,
        'global_codec_profiles_native_code_and_current_ROM_unchanged':True,'negative_scope_cases':negative,
        'original36_speech_branch_not_revised_displays_or15_conditional_visits':True,
        'reference_map_registered_release_and_revised_gameplay_pending':True,
        'evidence':{str(p):sha(p.read_bytes())for p in(FONT,CONTROL,CONTEXT,BRANCH)},
        'review_sheets':fonts['review_sheets'],'full_goal_complete':False}
    visual_path=ROOT/'visual_and_scoped_profile_review.json';save(visual_path,visual)
    doc.update(status='51-source-prose-and-native-format-reviewed;reference-map-revised-gameplay-release-pending',
        formatting_review_pending=False,review_gates={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True},
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review=str(visual_path),visual_review_sha256=sha(visual_path.read_bytes()),
        scoped_profile_module='dk4tool/dialogue/lil_stockholm_profile.py',
        scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_stockholm_profile.py').read_bytes()),
        scoped_control_proof=str(CONTROL),scoped_control_proof_sha256=sha(CONTROL.read_bytes()),
        required_runtime_ARM9_sha256=sha(arm),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        fixed_encoder_is_allocation_probe_only_until_complete_reference_map=True)
    validate_natural_dialogue_batch(doc);save(NEW,doc)
    ledger_raw=LEDGER.read_bytes();ledger=read(LEDGER);prior=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1529,1696)
    (ROOT/'ledger_before.json').write_bytes(ledger_raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['active_source_prose_drafts']['manuscripts'].append(str(NEW))
    ledger['active_source_prose_drafts']['route_record_subsets_pending'][str(NEW)]=[r['id']for r in doc['records']]
    ledger['formatting_watchlist']['Lil_Stockholm_Hodram51'].update(status='all51-native-format-approved;reference-map-revised-actual-release-pending',
        manuscript=str(NEW),native_font_proof=str(FONT),control_mapping_proof=str(CONTROL),
        unmapped_control_hex=None,affected_IDs=[],formatting_warnings_waived='18 narrowly justified line-break-count only',
        original_context=str(CONTEXT),revised_displays_not_yet_verified=True)
    ledger['lil_Stockholm_editorial_v1852'].update(manuscript=str(NEW),status='all51-native-format-approved;still-incomplete',
        native_font_proof=str(FONT),original_control_contract=str(CONTROL),original_current_context=str(CONTEXT),
        original24_relative_sites240_cases_proof=str(BRANCH),
        all_original_context_jobs_terminal=True,unmapped_Gerhard_source_prefix_hex=None,
        actual_revised_displays_reference_map_and_registered_patch_pending=True)
    ledger['next_route_scene_editorial_packet'].update(manuscripts=[str(NEW)],actual_activation_pending=False,
        original_B27_absent_Gerhard_branch_activated_and_returned=True,revised_display_verification_pending=True,
        source_relocation_reference_map_pending=True,editorial_review_complete=False)
    summary=('V1859:all51 Stockholm B27 paragraphs pass full native/independent font planes and408 macro/alignment calls;all7 sheets viewed. '
        'Gerhard0x10 is mapped byfixture-free currentHodram SC1B42:portrait,fullname,fulltext,ordinarydismissal andsame originalselector16 onLil/Hodram snapshots. '
        'Only anexact-B27/runtime private profile extendsleading0x10;globalprofiles remainunchanged. Four invalidscope/control casesreject. '
        '18 physical source-vs-automatic linebreak warnings havenarrow per-record reasons;nootherwarning waived. '
        'OriginalStockholm absent-Gerhard branch completes36 speech visits72 holds75 commandpairs andone original2000 artpause at62850;'
        'three16-byte coordinatefixture footprints,input/capture hashes,originaldiscovery/docking/eventcompletion andreadonlyobserverrestoration pass. '
        '15 conditional speeches were notvisited here;Hodram control sample isnot a B27 visit. '
        'All24 originalrelative sites pass240 clean/current cases. Revisedactualdisplay,targetrelocation/reference map,registeredROM andexactpatch remainpending. '
        '1529 complete(1158 revised371 retained),1696 source/prose reviewed;116 reviewed-incompleteCOMMON plus51B27drafts andbroader all-routes/playerprose remain. '
        'RegisteredV1841 unchanged,V1492 promoted. Graphics/all18plaques andolder-recordre-audit remainseparate/open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1859-Stockholm51-native-format-and-control-proof',
        'proof':str(ROOT/'approval_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'current_integrated_candidate','unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==prior[key],key
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1859_pending.json');assert not pending.exists()and LEDGER.read_bytes()==ledger_raw
    save(pending,ledger);os.replace(pending,LEDGER)
    Path('docs/lil_Stockholm_v1859_native_checkpoint.md').write_text('# V1859 Stockholm native-format checkpoint\n\n'+summary+
        f'\n\nCurrent manuscript: {NEW.as_posix()}\n\nNative fonts: {FONT.as_posix()}\n\nControl: {CONTROL.as_posix()}\n\n'
        'Next: preserve all51 paragraphs,resize B27 withstring parity andall24 typed relative spans;proveinverse/sourcecommand preservation,wholeload/cache entry andallnative destinations. '
        'Research bytes needactualrevised36-speech path plusapprovedscope for15 conditional objects before registered cumulative integration. '
        'All51source/nativefonts andthe shared livecontrol contract exist;do notclaim15 individual visits. KeepallpreviousROMs.\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:f.write('\n\n## V1859 Stockholm51 native-format proof\n\n'+summary+'\n\nSee [checkpoint](lil_Stockholm_v1859_native_checkpoint.md).\n')
    handoff=HANDOFF.read_text().replace('# Current editorial handoff - V1852','# Current editorial handoff - V1859',1)
    start=handoff.index('## Current working unit:');end=handoff.index('## Latest completed scene:')
    section=f'''## Current working unit: Stockholm B27, native-format51 approved

{summary}

- Current manuscript: {NEW.as_posix()}. Encoder remainsfixed only asallocationprobe. All51 English/source paragraphs unchanged fromV1,38proposedrevisions13retentions;18 line-break-count waivers only. Nativeformat approved,butnot completed orintegrated.
- Fonts: {FONT.as_posix()};51fullnative/independent216x64 planes,408 logical/wrapped/fouralignment macro calls,completeglyphorder/unique cells/zero roworigins. All7sheetsviewed. Visual/privateprofile approval: {visual_path.as_posix()}.
- Private profile dk4tool/dialogue/lil_stockholm_profile.py binds exactARM9 SHA500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e andclean/current B27 hashes. It addsleading0x10 only;globalbase stillrejects0x10 andscopedprofilestillrejects0x11. Wrongruntime/block rejected. Do notmodifyglobalprofiles orcodec.
- Livecontrol proof {CONTROL.as_posix()}:currentV1841 fixture-freeHodram opening SC1B42 command304 sixbytes0040FFFF0010 selectsGerhard16;fullportrait/nameplate andtext6800/6830/native-independent-RGBexact,ordinaryA->Hodram338/7160. Same original2434C selector returns16 onLil2 andHodram1 withoutchanging4MiB. All9 exactB27 preamblesmatch,butthisisnot nine B27 visits.
- OriginalStockholm context {CONTEXT.as_posix()}:natural discovery49440,docking50040,36speeches72observedholds75commandpairs,one original2000 artpause,normalreturn62850. Exact3fixtures at30290/42580/48810 each16coordinatesonly;allinput/capture/4MiBhashes andobserverrestoration pass. Native0x3000FE10 saysGerhardabsent;15conditional speech IDs remainunvisited. OldEnglishcontext isnot revised-text display approval.
- Originalbranchproof {BRANCH.as_posix()}:24 typed0100/0200/0300 sites,240clean/current original2A510 calls,alltargets independentnativeboundaries. FreshB27 sourcepacket work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json covers102commands51speeches.
- All jobs **terminal**:Stockholm1851/session30500 ended62850;driver1854b/session9946 endednormally. Failed1854 stoppedafteronecapturedspeech onoriginal2000 artwait;explicit1854b continued SAMEemulator andhandledsourcewait. Gerhard1856/session19913 ended7160 normally;nativefont1858/session7251 ended0. Neverrestart becauseobservationtimeout.
- Next: resizeall51 paragraphs withbyteparity andtyped24spanfixups usingresearch_lil_lessons_relocation_v1760.py asa sourceboundtemplate. Fullinverse,all102commands/opaqueeffects,120 targetnative skipcases,wholeSC2load/cache/entrycensus needed beforecomplete referenceapproval. ThenresearchROMderivedfromV1841,actualrevised original36-speech Stockholm path viaexact1851 journal,normalreturn,registeredpost-layer/exactcleanpatch/eightstartup controls.15 conditional records needexplicit source/native/presentation sampling scope;no individualactualclaim. Keepall51 draftedmeaning,do notshortenforoldslots.
- Existing original1851 inputjournal work/analysis/lil_Stockholm_context_run_v1851/navigation.jsonl ends62850;researchtarget canreplayits fullnormalinputs afterindependent loaderapproval. SourceDLEproof/privateprofile alreadyfixed. Newtargetmodule needsstrictsource/runtime/configdependencies andnegativegates,aspreviousB24module. Do notcopyresearchbins asproductionbytes.
- Originaldestination proofs1846/1847 remainvalid:LondonB26 alsoofflineeligible(111speechobjects,unreviewed);B25depends128,not24. Originalevent80 predicate hasoneLCGwrite02168EB8 inofflinecopy;neverclaimallpredicatequeriespure oralterliveRNG.

'''
    handoff=handoff[:start]+section+handoff[end:]
    handoff=handoff.replace('The earlier B24 jobs are **terminal**;newStockholm1851 above islive.','All current recorded jobs are **terminal**;Stockholm andGerhard control probes areclosed asdescribed above.')
    handoff=handoff.replace('Stockholm1851 is live;poll originalsession30500 or inspectauthoritativeprocess before another thread starts testing.',
        'Allrecordedjobs areterminal;verifycurrentauthoritativestate beforeanotherthread starts testing.')
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'approval_receipt.json',{'manuscript':str(NEW),'manuscript_sha256':sha(NEW.read_bytes()),
        'complete_font_cases':51,'native_macro_alignment_calls':408,'negative_scope_cases':negative,
        'linebreak_count_waivers_only':18,'source_prose_reviewed':1696,'completed_unchanged':1529,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'all_jobs_terminal':True,'registered_ROM_unchanged':True,'full_goal_remains_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'native_approved_lines':51,'macro_calls':408,'narrow_linebreak_waivers':18,'negative_scope_controls':4,
        'complete_unchanged':1529,'source_prose_reviewed':1696,'registered_V1841_unchanged':True},flush=True)
