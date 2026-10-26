"""Rebind unchanged complete FE proofs to exact successor compiled outputs."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_shrines_temples_profile import profile_for
from dk4tool.dialogue.lil_shrines_temples_layout_v2 import encode_relocatable_dialogue, audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Shrines_Temples_FE_v3184')
DOC=Path('translations/lil_shrines_temples_editorial_manuscript_v5.json')
PRIOR=Path('work/analysis/lil_Shrines_Temples_FE_v3180/current_FE_macro_font_and_typed_paper_proof.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,prior=read(DOC),read(PRIOR)
    assert sha(Path(prior['manuscript']).read_bytes())==prior['manuscript_sha256']
    assert sha(Path(prior['native_formatter_module']).read_bytes())==prior['native_formatter_module_sha256']
    old={r['id']:r for r in read(prior['manuscript'])['records']}
    oldcases={r['id']:r for r in prior['cases']}
    image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    assert sha(Path(doc['current_ROM']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==prior['ARM9_sha256'] and sha(common)==prior['COMMON_sha256']
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    cases=[]
    for row in doc['records']:
        if row['kind']!='system-FE':continue
        previous,case=old[row['id']],oldcases[row['id']]
        for key in ['english','source_hex','current_hex','source_reference','current_reference','kind','block']:
            assert row[key]==previous[key],(row['id'],key)
        raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],'FE-paper')
        encoded=encode_relocatable_dialogue(raw,row['english'],profile)
        assert encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex']
        assert row['english'].split('}',1)[1].encode('ascii').replace(b'{MACRO:FI}',b'FI')==previous['english'].split('}',1)[1].encode('ascii').replace(b'{MACRO:FI}',b'FI')
        qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in row.get('qa_waivers',[])]
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert sha(Path(case['native_plane']).read_bytes())==case['native_plane_sha256']
        cases.append({**case,'reused_current_native_case':True,'successor_QA':qa})
    assert len(cases)==30
    for sheet in prior['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True)
    formatter=Path('dk4tool/dialogue/lil_shrines_temples_layout_v2.py')
    save(ROOT/'current_FE_macro_font_and_typed_paper_proof.json',{
        **prior,'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'native_formatter_module':str(formatter),'native_formatter_module_sha256':sha(formatter.read_bytes()),
        'cases':cases,'prior_proof':str(PRIOR),'prior_proof_sha256':sha(PRIOR.read_bytes()),
        'all30_successor_source_prose_runtime_and_encoded_outputs_exact':True,
        'newly_executed_font_cases':0,'reused_unchanged_font_cases':30,
        'newly_executed_current_macro_alignment_cases':0,'reused_current_macro_alignment_cases':240,
        'all4_FE_sheets_viewed_and_hash_unchanged':True,'visual_review_pending':False,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completion_credit_added':0,'full_goal_complete':False})
    print('Thirty complete FE planes/240macro cases reused by exact source, prose, runtime and successor output;four viewed sheets hash-exact.')
