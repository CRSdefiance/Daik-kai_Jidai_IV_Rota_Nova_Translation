"""Observe strict native failures for nonterminal alignment-space candidates; no approvals."""
from pathlib import Path
import traceback
from scripts.qualify_maria310_FE_parity_space_v1 import *

def main():
    out=ROOT/'FE_parity_positions_diagnostic_v3.json';assert not out.exists()
    old=load(ROOT/'final_native_v1.json');doc=load(ROOT/'formatting_v1/formatting_input.json')
    ctx=RegisteredRuntime(doc['runtime']['release_proof'],doc['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==doc['runtime']
    row=next(r for r in old['records'] if r['id']=='DK4_MES_B54_R0507')
    raw=bytes.fromhex(row['compiled_hex']);body=raw[1:]
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    factory=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af},argdefs=native.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);cases=[]
    positions=sorted({i for i,c in enumerate(body) if c in [10,32]}|{i+1 for i,c in enumerate(body) if c==10})
    for at in positions:
        text=body[:at]+b' '+body[at:];case=dict(at=at,body_hex=text.hex())
        assert ' '.join(text.decode().split())==' '.join(body.decode().split())
        try:
            rendered=paint(text);rows=check_FE_rows(text,rendered)
        except AssertionError:
            case.update(pass_all=False,failure=traceback.format_exc(limit=2))
        else:
            path=ROOT/f'FE_parity_position_v3_{at}.bin';path.write_bytes(rendered['physical'])
            case.update(pass_all=True,native_plane=str(path),native_plane_sha256=sha(rendered['physical']),rows=rows)
        cases.append(case)
    save(out,dict(runtime=doc['runtime'],cases=cases,all_original_assertions_retained=True,not_approval=True))
    print('Strict positions tested:',len(cases),'passes:',[c['at'] for c in cases if c['pass_all']])
    failures={c['failure'] for c in cases if not c['pass_all']}
    for f in failures:print(f)

if __name__=='__main__':main()
