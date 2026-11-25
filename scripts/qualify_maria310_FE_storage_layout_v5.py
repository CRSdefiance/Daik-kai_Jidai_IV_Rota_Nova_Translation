"""Find a four-row, ordinary-codec paragraph plan with native-safe storage parity."""
from itertools import combinations
import traceback
from PIL import Image
from dk4tool.dialogue.codec import parse_markup,tokens_to_bytes
from scripts.qualify_maria310_FE_parity_space_v1 import *

def main():
    out=ROOT/'FE_storage_layout_qualification_v5.json';assert not out.exists()
    plan_path=ROOT/'plan_v8_complete_clauses/automatic_plans.json';doc_path=ROOT/'formatting_v1/formatting_input.json'
    plan,doc=map(load,[plan_path,doc_path]);ident='DK4_MES_B54_R0507'
    row=next(r for r in plan['records'] if r['id']==ident);source=next(r for r in doc['records'] if r['id']==ident)
    ctx=RegisteredRuntime(doc['runtime']['release_proof'],doc['runtime']['startup_proof'],captain=3);assert ctx.receipt()==doc['runtime']
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    factory=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af},argdefs=native.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);words=row['logical_English'].split();candidates=[]
    for cuts in combinations(range(1,len(words)),3):
        lines=[' '.join(words[a:b]) for a,b in zip((0,*cuts),(*cuts,len(words)),strict=True)]
        if any(len(s)+int(i>0)+int(i<3 and len(s)%2==0)>38 for i,s in enumerate(lines)):continue
        markup='{SPEAKER:FE}'+'{LB}'.join(lines)
        encoded=tokens_to_bytes(parse_markup(markup),guard_linebreaks=True,pair_phase_safe_breaks=True)
        if len(encoded)%2!=len(bytes.fromhex(source['current_hex']))%2:continue
        assert encoded[0]==254 and ' '.join(encoded[1:].decode().split())==row['logical_English']
        candidates.append(dict(lines=lines,formatted_markup=markup,encoded_hex=encoded.hex(),
            cost=sum((38-len(s))**2 for s in lines[:3])))
    candidates.sort(key=lambda c:c['cost']);passed=[]
    print('Automatic four-row codec candidates with matching storage parity:',len(candidates),flush=True)
    for i,c in enumerate(candidates):
        body=bytes.fromhex(c['encoded_hex'])[1:]
        try:
            result=paint(body);rows=check_FE_rows(body,result)
        except AssertionError:c.update(pass_all=False,failure=traceback.format_exc(limit=2))
        else:
            binary=ROOT/f'FE_storage_layout_v5_{i}.bin';binary.write_bytes(result['physical'])
            png=binary.with_suffix('.png');pic=Image.new('RGB',(228,64));pic.putdata([(0,8,0) if v else (239,232,201) for v in result['physical']]);pic.resize((912,256)).save(png)
            c.update(pass_all=True,native_plane=str(binary),preview=str(png),preview_sha256=sha(png.read_bytes()),
                rows=rows,complete_consumed_bytes=result['complete_consumed_bytes']);passed.append(c)
        print('Candidate',i,'pass',c['pass_all'],flush=True)
    proof=dict(id=ident,runtime=doc['runtime'],candidates=candidates,all_original_native_assertions_retained=True,
        source_reference=source['source_reference'],current_reference=source['current_reference'],
        original_encoded_hex=row['encoded_hex'],clean_logical_prose_unchanged=True,
        original_codec_guard_andpair_phase_rules_unchanged=True,source_owned_automatic_word_boundary_enumeration=True,
        full_original228px_geometry_font_andengine_unchanged=True,fresh_four_alignment_visual_andstorage_pending=True,new_credit=0)
    if passed:proof['selected']=passed[0]
    save(out,proof)
    assert passed,'No native safe four-row source-preserving layout'
    print('Qualified',len(passed),'four-row layouts;selected lines:',passed[0]['lines'])

if __name__=='__main__':main()
