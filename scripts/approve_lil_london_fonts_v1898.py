"""Approve all111 native paragraphs; keep relocation/revised gameplay separate."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_london_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_font_approval_v1898')
OLD=Path('translations/lil_london_editorial_manuscript_v3.json')
OUT=Path('translations/lil_london_editorial_manuscript_v4.json')
PROOFS=[
    Path('work/analysis/lil_London_known_fonts_v1886/all68_native_macros_and_complete_font_planes.json'),
    Path('work/analysis/lil_London_rumor_font_v1889/one_changed_native_macro_and_complete_font_plane.json'),
    Path('work/analysis/lil_London_scoped_fonts_v1895/all40_native_macros_and_complete_font_planes.json'),
    Path('work/analysis/lil_London_FE_v1896/all3_FE_native_planes_and_actual_mode_reconciliation.json')]
MACROS=Path('work/analysis/lil_London_FE_macros_v1897/all3_FE24_native_macro_alignment_cases.json')
CONTROL=Path('work/analysis/lil_London_controls_v1893b/source_bound_B26_presenter_and_control_contract.json')
ACTUAL=Path('work/analysis/lil_London_context_audit_v1892/original_London105_branch_and_three_fixture_audit.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=read(OLD)
    before=deepcopy(doc)
    image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[26]
    progressive=profile_for(arm,block)
    modal=profile_for(arm,block,'FE-paper')
    cases={}
    sheets=[]
    dependencies={str(p):sha(p.read_bytes()) for p in (*PROOFS,MACROS,CONTROL,ACTUAL,OLD,
        Path('dk4tool/dialogue/lil_london_profile.py'))}
    for path in PROOFS:
        proof=read(path)
        assert sha(Path(proof['manuscript']).read_bytes())==proof['manuscript_sha256']
        old_rows={r['id']:r for r in read(proof['manuscript'])['records']}
        for case in proof['cases']:
            ident=case['id']
            current=next(r for r in doc['records'] if r['id']==ident)
            if ident=='DK4_MES_B26_R0087' and len(proof['cases'])==68:
                continue
            assert current['source_hex']==old_rows[ident]['source_hex']
            assert current['english']==old_rows[ident]['english']
            assert ident not in cases
            cases[ident]=deepcopy(case)
            cases[ident]['source_proof']=str(path)
            assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
            dependencies[case['preview']]=case['preview_sha256']
        refs=proof.get('review_sheets',[])
        if 'review_sheet' in proof:
            refs=[dict(path=proof['review_sheet'],sha256=proof['review_sheet_sha256'])]
        for sheet in refs:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
            dependencies[sheet['path']]=sheet['sha256']
            sheets.append(sheet)
    assert len(cases)==111
    fe_macros={r['id']:r['macro_cases'] for r in read(MACROS)['cases']}
    for ident,checks in fe_macros.items():
        cases[ident]['macro_cases']=checks
    assert sum(len(r['macro_cases']) for r in cases.values())==888
    negatives=[]
    def reject(label,fn):
        try:fn()
        except ValueError as error:negatives.append(dict(case=label,error=str(error)))
        else:raise AssertionError('Invalid London native scope accepted: '+label)
    reject('wrong_runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block))
    reject('wrong_source_block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1])))
    reject('wrong_consumer',lambda:profile_for(arm,block,'unmapped'))
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    for prefix in ('10','1c','97','fe'):
        row=next(r for r in doc['records'] if r['source_presentation_prefix_hex']==prefix)
        reject('global_'+prefix+'_still_rejected',lambda r=row:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].removesuffix('{PAD}'),base))
    fe=next(r for r in doc['records'] if r['source_presentation_prefix_hex']=='fe')
    named=next(r for r in doc['records'] if r['source_presentation_prefix_hex']=='1c')
    reject('FE_not_progressive',lambda:encode_relocatable_dialogue(bytes.fromhex(fe['source_hex']),fe['english'].removesuffix('{PAD}'),progressive))
    reject('progressive_not_FE',lambda:encode_relocatable_dialogue(bytes.fromhex(named['source_hex']),named['english'].removesuffix('{PAD}'),modal))
    first=doc['records'][0]
    reject('unmapped11_still_rejected',lambda:encode_relocatable_dialogue(b'\x11'+bytes.fromhex(first['source_hex'])[1:],first['english'].replace('SPEAKER:02','SPEAKER:11').removesuffix('{PAD}'),progressive))
    waived=[]
    for row in doc['records']:
        case=cases[row['id']]
        compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),
            modal if row['source_presentation_prefix_hex']=='fe' else progressive)
        assert compiled.encoded.hex()==case['encoded_hex']
        row['compiled_hex']=case['encoded_hex']
        diagnostics=[d for d in compiled.diagnostics if d.severity in ('error','warning')]
        assert all(d.severity=='warning' and d.code=='line-break-count' for d in diagnostics)
        if diagnostics:
            assert len(diagnostics)==1
            reason=('The Japanese physical line count isnot anEnglish dramatic pause. Full sourcefacts andspeaker intent arepreserved inone logical paragraph;the complete native/independent plane hasallfirst/last glyphs insideits original progressive orFE bounds andonepage. '+diagnostics[0].message+'. Noother warning iswaived.')
            row['qa_waivers']=['line-break-count']
            row['qa_waiver_reason']=reason
            waived.append(dict(id=row['id'],code='line-break-count',reason=reason))
        row['review']['formatting']=True
        row['native_display_consumer']='original_FE_modal_5473C_mode1' if row['source_presentation_prefix_hex']=='fe' else 'original_progressive_54020'
        row['context']=row['context'].replace('newscene control mapping,native format andrepresentative gameplay remainpending.',
            'Original105-speech representative gameplay andsource-bound control/native/font proofs pass;revised gameplay,typed relocation andregistered integration remainpending.')
        if row['source_presentation_prefix_hex']=='97':
            row['speaker']='Unnamed voice;native actor151 catalog label Retainer'
            row['speaker_context_basis']='Original selector97 maps toactor151 andthe shared progressive presenter. Catalog name iscurrent technical evidence,not anewrank or anindividual live visit.'
        row['display_mapping_pending']=False
        row['individually_observed_original_context']=row['id'] not in read(ACTUAL)['unvisited_original_speech_IDs']
    assert len(waived)==24
    ROOT.mkdir(parents=True)
    font_path=ROOT/'all111_complete_native_font_and_macro_reconciliation.json'
    save(font_path,dict(manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),cases=list(cases.values()),
        all111_complete_native_independent_planes=True,current_record_macro_alignment_cases=888,
        old67_progressive_planes_inherited_exact_one_changed_rumor_plane_retested=True,
        three_FE_separate_native_mode1_planes_and6_old_actual_holds=True,review_sheets=sheets,
        all16_sheet_contents_actually_viewed=True,evidence=dependencies,
        revised_actual_scene_andrelocation_release_pending=True,full_goal_complete=False))
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=False,
        status='all111-source-prose-native-font-approved;relocation-revised-gameplay-andrelease-pending',
        native_font_proof=str(font_path),native_font_proof_sha256=sha(font_path.read_bytes()),
        visual_review=str(ROOT/'native_visual_and_scope_approval.json'),scoped_profile_module='dk4tool/dialogue/lil_london_profile.py',
        scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_london_profile.py').read_bytes()),
        scoped_control_proof=str(CONTROL),scoped_control_proof_sha256=sha(CONTROL.read_bytes()),
        required_runtime_ARM9_sha256=sha(arm),original_actual_context=str(ACTUAL),
        fixed_encoder_is_allocation_probe_only_until_complete_reference_map=True)
    validate_natural_dialogue_batch(doc)
    bad=deepcopy(doc)
    bad['records'][0]['review']['formatting']=False
    reject('unreviewed_record_formatting',lambda:validate_natural_dialogue_batch(bad))
    assert len(negatives)==11
    save(ROOT/'native_visual_and_scope_approval.json',dict(all111_source_context_naturalness_and_native_planes_reviewed=True,
        all16_sheets_and_all111_panel_contents_actually_viewed=True,
        complete_first_last_glyphs_bounds_original_progressive_and_FE_pages_verified=True,
        only24_physical_linebreak_count_warnings_narrowly_waived=waived,
        exact_runtime_B26_private_profiles_global_profiles_unchanged=True,
        original105_actual_visits_six_conditional_offline_only=True,
        no_revised_glyph_gameplay_orregistered_release_approval=True,negative_cases=negatives,
        evidence={**dependencies,str(font_path):sha(font_path.read_bytes())},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    save(OUT,doc)
    assert all(a['english']==b['english'] for a,b in zip(before['records'],doc['records'],strict=True))
    print(dict(native_records=111,macro_alignment_cases=888,narrow_linebreak_waivers=24,negative_scope_cases=11,
        manuscript=str(OUT),relocation_revised_gameplay_registered_release_pending=True))
