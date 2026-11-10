"""Bind five directly seen phrase splits and one measured FE extra-row defect."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
FINDINGS={
'DK4_MES_B64_R0091':dict(line_phrases=["If you'd like",'help you out'],sheet=6,
    reason='Keep the short conditional and the condescending-offer echo together rather than splitting If you would/like across rows.'),
'DK4_MES_B64_R0126':dict(line_phrases=['I could help you out'],sheet=6,
    reason='Keep the complete quoted offer together; the viewed page split help from you out at the key self-reflection echo.'),
'DK4_MES_B64_R0144':dict(line_phrases=['gone about it'],sheet=7,
    reason='The viewed page split gone about/it; preserve the phrasal expression as a unit in the reassurance.'),
'DK4_MES_B64_R0256':dict(line_phrases=['whole lot!'],sheet=8,
    reason='The viewed page stranded lot before the final Yeah question; keep whole lot together.'),
'DK4_MES_B64_R0319':dict(line_phrases=['All we had','as far as the eye could see.'],sheet=9,
    reason='The viewed page stranded All before we had and split the short as-far-as-the-eye-could-see expression; preserve both coherent phrases.'),
}

if __name__=='__main__':
    prior=ROOT/'planned_boundary_preferences_v4.json';target=ROOT/'visual_preferences_v5.json';assert not target.exists()
    doc=load(ROOT/'formatting_input_v3.json');byid={r['id']:r for r in doc['records']}
    preferences=deepcopy(load(prior))
    for key,values in FINDINGS.items():
        values=deepcopy(values);number=values.pop('sheet');sheet=ROOT/f'contact_B61_B66_v1/sheets/sheet_{number}.png'
        preferences['records'][key]=dict(**values,
            bindings={k:sha(byid[key][k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
            directly_viewed_sheet=str(sheet),directly_viewed_sheet_sha256=sha(sheet.read_bytes()),
            no_prose_change_no_authored_breaks=True)
    proof=ROOT/'Charlotte_FE_R87_row_finding_v1.json';finding=load(proof)
    assert finding['actual_rows']==[{'y':0,'text':'Hee hee, thank you. Come along. Ther'},
        {'y':12,'text':'e '},{'y':24,'text':'is plenty of food!'}]
    key='DK4_MES_B69_R0087'
    preferences['records'][key]=dict(FE_planning_cells=36,
        bindings={k:sha(byid[key][k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
        reason='The concrete37-character first FE row automatically wrapped the final e, then LF made an extra third row. Reuse the existing source-qualified guard-reserve policy only for this record. Native228px geometry/font/control code remain unchanged.',
        native_finding=str(proof),native_finding_sha256=sha(proof.read_bytes()),
        fresh_native_FE_row_membership_required=True)
    preferences.update(previous_preferences=str(prior),previous_preferences_sha256=sha(prior.read_bytes()),
        five_directly_seen_phrase_findings_andone_concrete_FE_row_failure=True,
        all539_English_andall_native_runtime_geometry_unchanged=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(target,preferences)
    print('Five visual phrase findings/one exact FE extra-row defect scoped;wording and native geometry preserved. Fresh plans/native pages required.',flush=True)
