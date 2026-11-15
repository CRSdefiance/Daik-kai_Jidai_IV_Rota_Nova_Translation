"""Recompile byte-identical style rows under a successor plan; reuse native slot proofs."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['proof','manuscript','plan','out']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    proof,doc,after=map(load,[a.proof,a.manuscript,a.plan]);beforepath=Path(proof['plan']);before=load(beforepath)
    assert proof['plan_sha256']==digest(beforepath) and proof['manuscript_sha256']==digest(a.manuscript)
    assert before['manuscript_sha256']==after['manuscript_sha256']==digest(a.manuscript)
    assert proof['runtime']==doc['runtime'] and not after['failures']
    for name,h in proof['evidence'].items():assert digest(name)==h
    old={r['id']:r for r in before['records']};new={r['id']:r for r in after['records']}
    style=[r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative']
    assert len(style)==proof['physical_alternatives'] and all(old[r['id']]==new[r['id']] for r in style)
    compiled=[]
    for obj in proof['objects']:
        rows=[r for r in style if r['block']==obj['block'] and r['source_command_offset']==obj['source_command_offset']]
        rows.sort(key=lambda r:r['source_reference']['offset'])
        target=compile_styles(bytes.fromhex(obj['source_object_hex']),bytes.fromhex(obj['current_object_hex']),rows,new,require_formatting=False)
        assert target.hex()==obj['target_object_hex'] and digest(obj['target_path'])==obj['target_sha256']
        assert [r['id'] for r in rows]==obj['physical_record_IDs']
        compiled.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=target.hex()))
    result=deepcopy(proof)
    result.update(plan=str(a.plan),plan_sha256=digest(a.plan),original_native_style_proof=str(a.proof),original_native_style_proof_sha256=digest(a.proof),
        complete_source_current_alias_target_body_andfinal_plan_recompiled_exact=True,
        final_plan_style_rows_byte_identical_to_native_checked_rows=True,
        native_slot_andnegative_cases_reused_not_reexecuted=True,pure_final_plan_recompilations=compiled)
    result['evidence'].update({str(v):digest(v) for v in [a.proof,a.plan,a.manuscript,Path(__file__)]})
    a.out.parent.mkdir(parents=True,exist_ok=True);save(a.out,result)
    print('Recompiled',len(compiled),'exact style objects; reused',proof['native_target_slot_cases'],'native slot proofs without replay.')

if __name__=='__main__':main()
