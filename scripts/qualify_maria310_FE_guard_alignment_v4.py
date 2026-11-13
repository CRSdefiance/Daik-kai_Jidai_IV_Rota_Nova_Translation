"""Qualify removal of one compiler-owned edge guard, retaining all native checks and prose."""
from pathlib import Path
import traceback
from PIL import Image
from scripts.qualify_maria310_FE_parity_space_v1 import *

def main():
    out=ROOT/'FE_guard_alignment_qualification_v4.json';assert not out.exists()
    prior_path=ROOT/'final_native_v1.json';doc_path=ROOT/'formatting_v1/formatting_input.json'
    old,doc=map(load,[prior_path,doc_path]);ctx=RegisteredRuntime(doc['runtime']['release_proof'],doc['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==doc['runtime']
    ident='DK4_MES_B54_R0507';row=next(r for r in old['records'] if r['id']==ident)
    source=next(r for r in doc['records'] if r['id']==ident)
    raw=bytes.fromhex(row['compiled_hex']);body=raw[1:];prior=Path(row['complete_native_English_display']['native_plane']).read_bytes()
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    factory=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af},argdefs=native.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);cases=[];passed={}
    for at in [i for i,c in enumerate(body) if c==32 and (i==0 or body[i-1]==10 or i+1==len(body) or body[i+1]==10)]:
        text=body[:at]+body[at+1:];case=dict(removed_guard_offset=at,compiled_hex=(raw[:1]+text).hex())
        assert ' '.join(text.decode().split())==source['editorial_logical_English']
        try:
            rendered=paint(text);rows=check_FE_rows(text,rendered)
        except AssertionError:case.update(pass_all=False,failure=traceback.format_exc(limit=2))
        else:
            passed[at]=rendered['physical'];case.update(pass_all=True,native_plane_sha256=sha(rendered['physical']),rows=rows,
                complete_consumed_bytes=rendered['complete_consumed_bytes'],events=rendered['events'],
                changed_pixels_from_prior=sum(a!=b for a,b in zip(prior,rendered['physical'],strict=True)))
        cases.append(case)
    good=[c for c in cases if c['pass_all']]
    proof=dict(id=ident,cases=cases,runtime=doc['runtime'],all_original_native_assertions_retained=True,
        logical_prose_source_controls_existing_LF_font_viewport_engine_unchanged=True,
        original_compiled_hex=raw.hex(),source_reference=source['source_reference'],current_reference=source['current_reference'],new_credit=0)
    if good:
        selected=min(good,key=lambda c:c['changed_pixels_from_prior']);pixels=passed[selected['removed_guard_offset']]
        binary=ROOT/'FE_guard_alignment_candidate_v4.bin';binary.write_bytes(pixels)
        png=binary.with_suffix('.png');pic=Image.new('RGB',(228,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);pic.resize((912,256)).save(png)
        proof.update(target_compiled_hex=selected['compiled_hex'],selected=selected,native_plane=str(binary),preview=str(png),
            preview_sha256=sha(png.read_bytes()),fresh_visual_four_alignment_andstored_checks_pending=True)
    save(out,proof)
    print('Edge guard candidates:',len(cases),'strict passes:',[c['removed_guard_offset'] for c in good])
    assert good,'No qualified removable guard'

if __name__=='__main__':main()
