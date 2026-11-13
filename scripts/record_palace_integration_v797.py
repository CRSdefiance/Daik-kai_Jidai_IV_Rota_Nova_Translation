"""Record the integrated Palace candidate and precisely scoped actual tests."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.palace_editorial import ROOT
from scripts.verify_village_wrap_v608 import read,save

DOC=Path('docs/palace_integration_v797_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V797 Palace prose integration and contract verification')
GUIDE=Path('E:/Rota Nova translations/Strategy Guide/Screenshots/V797 Palace contract')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    registered=read(ROOT/'registered_verification.json');actual=read(ROOT/'contract_gameplay_verification.json')
    assert registered['candidate_sha256']==actual['candidate_sha256']
    assert sha(Path(registered['candidate']).read_bytes())==registered['candidate_sha256']
    assert actual['quote_extra_blank_page_removed_one_A_reaches1157']
    assert actual['cash_models_actors_towns_items_goods_couriers_exact_initial_to_return']
    assert all(r['whole_outside_dialogue_plane_exact'] for r in actual['outside_body_comparisons'])
    assert all(r['whole_screen_exact'] for r in actual['control_frames'])
    assert len(read(ROOT/'newgame_regression.json')['whole_screen_frame_pairs'])==7
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed']==496 and ledger['records_with_source_and_prose_pass']==530
    assert len(ledger['active_source_prose_drafts']['native_message_IDs'])==34
    save(ROOT/'editorial_ledger_before_v797.json',ledger)
    ledger['previous_whole_batch_verified_candidate_V792']=ledger['current_integrated_candidate']
    current={'path':registered['candidate'],'sha256':registered['candidate_sha256'],'profile':registered['profile'],
        'MESFILE_sha256':registered['COMMON_sha256'],'ARM9_sha256':registered['ARM9_sha256'],
        'patch_sha256':registered['patch_sha256'],'manifest':str(Path(registered['candidate']).with_suffix('.manifest.json')),
        'status':'experimental-Palace-family-partially-gameplay-verified','details':str(DOC),
        'supplemental_verification':str(ROOT/'contract_gameplay_verification.json'),
        'remaining_in_this_registered_batch':'Palace Market-letter permissions,defense,treasure loan/return,successful contract and refusal outcomes require additional actual family samples;no31-entry completion credit yet.',
        'full_goal_complete':False}
    ledger['current_integrated_candidate']=current
    ledger['active_source_prose_drafts']['manuscripts'].append('translations/palace_editorial_manuscript_v3.json')
    ledger['active_source_prose_drafts']['status']='750-752-context-unmapped;Palace31-integrated-native-reviewed-additional-gameplay-pending'
    ledger['active_source_prose_drafts']['note']='Palace31 integrated in V797 with production formatting/native copies;actual contract quote/share/cancellation and return verified. Additional Palace families remain pending;none of31 counted complete yet. Three older contexts750-752 remain unmapped.'
    ledger['palace_next_source_packet']['next']='Verify actual Market-letter permissions,defense contributions,treasure loan/return and successful/refused contracts using original conditions or disclosed isolated fixtures. Keep31-entry completion gate open.'
    ledger['palace_next_source_packet']['production_manuscript']='translations/palace_editorial_manuscript_v3.json'
    ledger['palace_next_source_packet']['integration']=str(ROOT/'registered_verification.json')
    ledger['palace_next_source_packet']['actual_contract_sample']=str(ROOT/'contract_gameplay_verification.json')
    for finding in ledger['findings']:
        if finding['id']=='Palace1156-extra-blank-page-original-display':
            finding.update({'status':'corrected-integrated-actual-display-verified-V797',
                'repair_proof':str(ROOT/'contract_gameplay_verification.json'),
                'detail':'Exact full native font includes all four2842 digits;one A now reaches1157 without an empty page. Original outside-body pixels and later amount picker/menu/town controls match. Other Palace branches remain pending.'})
        elif finding['id']=='Palace1162-insufficient-funds-meaning':
            finding['status']='source-context-corrected-integrated-native-reviewed;actual-refusal-pending'
    ledger['formatting_watchlist']['latest_reference_proof']=str(ROOT/'registered_verification.json')
    ledger['formatting_watchlist']['reference_case']+=' V797 preserves repaired676/677 and arrival346-348 text exactly;Palace1156 full four-digit amount and removed blank page verified in actual playback. No fresh shop676/677 activation claimed.'
    summary=('V797 integrates31 source-reviewed Palace paragraphs after the complete V792 stack,with470 batches/114 accepted layers preserved. '
        '35,320 exact selector/ABI cases,140 whole8MiB status cases,323 production layouts,40 complete font planes and5,076 full warm/cold native copies pass. '
        'The original168-byte private data bank is reordered as13-byte luxury-goods string plus alignment,130-byte table and24-byte phrase indices;only two pointer literals move. '
        'Gate instructions,exact caller restrictions,sections/BSS/cache and123040-byte staged payload stay unchanged. '
        'Actual contract1156 displays all2842 digits,one A reaches1157 without the old blank page,and1158 cancellation returns to town with8371 coins and persistent objects unchanged. '
        'Three dialogue holds preserve every outside-body pixel;seven other scene controls and seven New Game/startup frames are exact. '
        'Clean-input patch reconstructs exactly.496 complete/530 source-prose reviewed/34 reviewed pending remain unchanged;additional Palace families need actual samples. Full editorial goal and separate graphics audit remain unfinished.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V796-V797-Palace-bounded-integration-contract-gameplay',
        'documentation':str(DOC),'new_editorially_completed':0,'new_ROM':True,'full_goal_complete':False})
    save(LEDGER,ledger);save('out/editorial_review_latest.json',current)
    DOC.write_text('# V797: Palace integration and actual contract verification\n\n'+summary+'\n\n'
        '## Candidate\n\n'
        f"Experimental ROM: `{registered['candidate']}`\n\nSHA-256: `{registered['candidate_sha256']}`\n\n"
        f"Exact clean-input patch SHA-256: `{registered['patch_sha256']}`\n\n"
        'Profile: `all-routes-unified-v797`. Canonical parent remains '
        '`out/raphael_natural_v2_accepted_base.nds`, SHA-256 '
        '`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. '
        'Only `/COMMON/MESFILE.DK4` and ARM9 change from V792. All3637 other logical COMMON strings remain exact; '
        'the existing41-block allocation is repacked across blocks15-40, with complete opaque tails preserved. '
        'All preceding accepted/experimental dependencies are retained. No canonical promotion.\n\n'
        '## Evidence and limits\n\n'
        'The native tests use explicit original parent/ID/argument contracts; names and amounts include '
        'declared size stress values, not claims of naturally earned eligibility. All changes remain inside '
        'previously proven private allocations and COMMON metadata. The complete `luxury goods` string '
        'includes its NUL; a rejected prototype omitted that byte in its capacity calculation. Final packing '
        'keeps the string word aligned and selector table halfword aligned, matching ARM946 loads. '
        'All140 status-output/ABI/8MiB guards pass after relocation.\n\n'
        'Actual DeSmuME playback cold-boots an isolated byte-exact Istanbul save, without savestates '
        'or condition/location/inventory fixtures. The donor remains unchanged. The old full schedule '
        'contains one extra blank-page A at5201;the repaired schedule removes precisely that event and '
        'moves later identical actions400 frames earlier. The journal and terminal6800-frame report '
        'confirm normal cancellation and town return. Full native font/blank-paper ink is checked for '
        '1156,1157,1158, including complete leading/trailing letters and2842. The source actual extra '
        'blank page is repaired;this does not certify the whole game.\n\n'
        'Automatic approval initially rejected the saved-game launch due to possible donor writes. '
        'Inspection established that the unchanged harness reads/copies the donor and exposes only '
        'the fresh output save directory to the core;the evidence-supported retry was approved. '
        'The donor hash is checked again after playback.\n\n'
        '## Remaining work\n\n'
        'Actual Market-letter permission,defense,treasure loan/return,successful-contract and refusal '
        'family samples remain required. All31 Palace entries retain their completion gate. The older '
        '750-752 contexts,wider shared prose,all route scenes and help/other prose remain unfinished. '
        'The separate graphics audit/18 plaques stay open;Online-body exclusions,brown marks and '
        'approved names remain unchanged. Revisit older record checks at full editorial completion.\n',encoding='utf-8')
    for name in ('known_issues','todo','translation_progress','editorial_review_goal'):
        p=Path('docs')/(name+'.md');p.write_text(p.read_text(encoding='utf-8')+
            '\n\n## V797: Palace integration and contract verification\n\n'+summary+
            ' See [V797 checkpoint](palace_integration_v797_checkpoint.md).\n',encoding='utf-8')
    GUIDE.mkdir(parents=True,exist_ok=True)
    guide=[]
    for row in actual['actual_repaired_holds']:
        source=Path(row['capture']['path']);dest=GUIDE/f"COMMON{row['message_id']}_verified.png"
        assert not dest.exists();shutil.copy2(source,dest);assert sha(dest.read_bytes())==sha(source.read_bytes())
        guide.append({'message_id':row['message_id'],'path':str(dest),'sha256':sha(dest.read_bytes()),
            'candidate_sha256':current['sha256'],'source_capture':str(source),'actual_contract_sample_only':True})
    save(GUIDE/'provenance.json',{'screenshots':guide,'candidate_experimental':True,'full_goal_complete':False})
    files=[DOC,LEDGER,Path('translations/release_stack.json'),Path('translations/palace_editorial_release_v1.json')]
    files += [Path('translations')/f'palace_editorial_manuscript_v{n}.json' for n in (1,2,3)]
    files += [Path('dk4tool/patch/palace_editorial.py'),Path('dk4tool/patch/palace_editorial_runtime.py'),
              Path('scripts/build_integrated_release.py')]
    files += list(ROOT.glob('*.json'))+list((ROOT/'native_copies').glob('*.json'))
    files += list(Path('work/analysis/palace_runtime_v796').glob('*.json'))
    files += list(Path('work/analysis/palace_editorial_v795').glob('*.json'))
    files += list(Path('work/analysis/palace_editorial_v795/prototype_layout').glob('*.json'))
    files += list(Path('work/analysis/palace_editorial_v795/prototype_layout').glob('*.png'))
    files += [Path('scripts')/n for n in ('context_palace_v795.py','review_palace_v795.py','probe_palace_layout_v795.py',
        'record_palace_review_v795.py','verify_palace_runtime_v796.py','prepare_palace_v797.py','verify_palace_copies_v797.py',
        'register_palace_release_v797.py','verify_palace_release_v797.py','verify_palace_gameplay_v797.py','record_palace_integration_v797.py')]
    copies=[]
    for source in sorted(set(files)):
        assert not source.is_absolute();dest=ARCHIVE/source;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,dest);assert sha(source.read_bytes())==sha(dest.read_bytes())
        copies.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes())})
    receipt={'copies':copies,'all_copies_SHA256_exact':True,'guide_candidates':guide,'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'V797 checkpoint/ledger/progress saved;{len(copies)} exact archive copies and3 guide candidates.496 complete unchanged;goal active.',flush=True)


if __name__=='__main__':main()
