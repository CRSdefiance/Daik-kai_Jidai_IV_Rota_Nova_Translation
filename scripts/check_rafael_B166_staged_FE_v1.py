"""Compile the 22 source-staged FE panels and prove all row origins on the original painter."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import re

from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_compiled_pages_v2 as native
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B166_B167_ordinary_v1 import ROOT, STAGED
from scripts.probe_rafael_B166_FE_source_staging_v1 import build_painter
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE_ANCHORS = ROOT/'native_FE_source_staging_v1/native_FE_rows.json'
OUT = ROOT/'staged_FE_native_v1'
HEADINGS = {183,190,196,205,208,215,222,237}
RIGHT = {249:96,257:108}
SILENCES = {265,273}
LEFT = {253,261,269,908,912}
PARTICLES = {'a','an','the','and','or','to','of','for','in','my','your','at','some','any','with'}


def wrap_options(body, count):
    words=body.split()
    options=[]
    def visit(at, lines):
        if at==len(words):
            ends=[line.split()[-1].lower().strip('.,!?') for line in lines[:-1]]
            last=len(lines[-1])
            score=(sum(w in PARTICLES for w in ends)+int(last<8 and len(lines)>1),len(lines),
                sum((36-len(line))**2 for line in lines[:-1]))
            options.append((score,lines))
            return
        if len(lines)==count:
            return
        for stop in range(at+1,len(words)+1):
            line=' '.join(words[at:stop])
            if len(line)>36:
                break
            visit(stop,(*lines,line))
    visit(0,())
    return [lines for _,lines in sorted(options)]


def source_shapes(idx, logical):
    if idx==183:
        return [[(0,'Eirene:'),(0,'...'),(0,'Claudio?')]]
    if idx in HEADINGS:
        assert logical.startswith('Eirene: ')
        return [[(0,'Eirene:'),*((0,t) for t in rows)] for rows in wrap_options(logical[8:],3)]
    if idx==245:
        return [[(0,''),(0,'Claudio...'),(0,logical.split(' ',1)[1])]]
    if idx in RIGHT:
        x=min(RIGHT[idx],222-len(logical)*6)
        assert x>=60 and x%6==0
        return [[(0,''),(0,''),(x,logical)]]
    if idx in LEFT:
        return [[(0,''),(0,''),(0,logical)]]
    if idx==787:
        return [[(0,'{MACRO:FI}')]]
    if idx==791:
        return [[(0,'Muint obrigada'),(0,'por tudo.'),(0,'(MWEEN-too oh-bree-GAH-dah'),(12,'por TOO-doo.)')]]
    if idx==794:
        return [[(0,'Muint bem'),(0,'obrigada.'),(0,'(MWEEN-too beng oh-bree-GAH-dah.)'),(24,'Charlotte Miller')]]
    if idx==797:
        return [[(0,'{MACRO:FI},'),(0,'thank you so much for everything.'),(0,"I'm doing very well, thank you."),(84,'Charlotte Miller')]]
    assert idx in SILENCES
    return [[(0,''),(0,''),(204,'…')]]


def actual_rows(events):
    groups=defaultdict(list)
    for e in events:
        code=e['code']
        text=bytes([code]).decode('ascii') if e['kind']=='ascii' else code.to_bytes(2,'big').decode('cp932')
        groups[e['y']].append((e['x'],text))
    out=[]
    for y,g in sorted(groups.items()):
        nonblank=[x for x,c in g if not c.isspace()]
        if nonblank:
            out.append((y,nonblank[0],''.join(c for _,c in g).strip()))
    return out


def expand(body):
    return body.replace(b'FI',b'Rafael')


def candidates(row,idx,shape):
    if idx in SILENCES:
        raw=bytes.fromhex(row['current_hex'])
        assert raw==bytes.fromhex(row['source_hex'])
        yield raw[1:]
        return
    lines=[b' '*(x//6)+t.replace('{MACRO:FI}','FI').encode('cp932') for x,t in shape]
    for guards in product((0,1),repeat=len(lines)-1):
        for blanks in ('ascii','native'):
            result=[]
            for i,line in enumerate(lines):
                x=shape[i][0]
                if blanks=='native' and x%12==0 and x:
                    line=b'\x81\x40'*(x//12)+line[x//6:]
                trailing=b' ' if i<len(guards) and guards[i] and line else b''
                result.append(line+trailing)
            yield b'\n'.join(result)


def main():
    assert not OUT.exists()
    staged,prior = map(load,(STAGED,SOURCE_ANCHORS))
    assert staged['runtime']==prior['runtime']
    ctx=RegisteredRuntime(staged['runtime']['release_proof'],staged['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==staged['runtime']
    painter,calibration=build_painter(staged['runtime'])
    adapter=checked_text(load(native.MACROS)['source_owned_FE_adapter'],{
        "b'Hodram'":"b'Rafael'","b'Bergstrom'":"b'Castor'","b'Bergstrom Fleet'":"b'Castor Co.'"})
    macro_env=dict(native.FE_expand.__globals__)
    exec(compile(adapter,__file__+'::original-FE-expansion','exec'),macro_env)
    OUT.mkdir()
    proofs=[]
    pictures=[]
    failures=[]
    for row,anchor in zip(staged['records'],prior['staged'],strict=True):
        idx=row['source_record_index']
        ident=row['id']
        logical=row['english']
        assert anchor['id']==ident and row['source_complete_preamble_hex']=='0040ffff00fe'
        shapes=source_shapes(idx,logical)
        prior_rows=anchor['observations']['source']['rows']
        match=None
        trials=0
        for shape in shapes:
            joined=' '.join(t for _,t in shape if t)
            if idx==183:
                joined=joined.replace('... Claudio?','...Claudio?')
            assert joined==logical,(ident,joined,logical)
            expected=[(i*12,x,t.replace('{MACRO:FI}','Rafael')) for i,(x,t) in enumerate(shape) if t]
            assert [y for y,_,_ in expected][:1]==[r['y'] for r in prior_rows][:1]
            assert len(shape)<=4 and all(x+6*len(t)<=228 for _,x,t in expected if t.isascii())
            for body in candidates(row,idx,shape):
                trials+=1
                try:
                    display=painter(expand(body))
                    actual=actual_rows(display['events'])
                except AssertionError:
                    continue
                if actual==expected:
                    match=(shape,body,expected,display)
                    break
            if match:
                break
        if not match:
            failures.append(dict(id=ident,candidate_shapes=len(shapes),guard_candidates=trials))
            continue
        shape,body,expected,display=match
        assert b'\0' not in body and re.findall(rb'F[AIOU]',body)==[t.encode() for t in row['native_literal_tokens']]
        expanded=expand(body)
        aligned=ctx.execute(macro_env['expand'],body)
        assert len(aligned['cases'])==4 and all(c['output_hex']==expanded.hex() for c in aligned['cases'])
        assert display['complete_consumed_bytes']==len(expanded)
        physical,logical_plane=display.pop('physical'),display.pop('logical')
        binary=OUT/(ident+'.bin')
        binary.write_bytes(physical)
        logical_file=binary.with_name(ident+'_logical.bin')
        logical_file.write_bytes(logical_plane)
        pic=Image.new('RGB',(228,64))
        pic.putdata([(0,8,0) if v else (239,232,201) for v in physical])
        pic.save(binary.with_suffix('.png'))
        pictures.append((ident,pic))
        proofs.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],
            logical_English=logical,source_complete_preamble_hex=row['source_complete_preamble_hex'],
            source_staging_reason=row['FE_layout_finding'],encoded_hex=(b'\xfe'+body).hex(),expanded_hex=expanded.hex(),
            native_macro_alignments=aligned,planned_visible_rows=expected,complete_native_English_display=display,
            all_visible_row_origins_and_full_glyphs_exact=True,guard_candidates=trials,plane=str(binary),
            plane_sha256=sha(physical),logical_plane=str(logical_file),logical_plane_sha256=sha(logical_plane)))
    sheets=[]
    for start in range(0,len(pictures),8):
        part=pictures[start:start+8]
        sheet=Image.new('RGB',(920,152*((len(part)+1)//2)),'#263238')
        draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(part):
            x,y=(i%2)*460,(i//2)*152
            draw.text((x+4,y+3),label,fill='white')
            sheet.paste(pic.resize((456,128),Image.Resampling.NEAREST),(x,y+20))
        path=OUT/f'FE_stage_sheet_{start//8+1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),records=[k for k,_ in part]))
    save(OUT/'staged_display.json',dict(runtime=staged['runtime'],records=proofs,failed=failures,review_sheets=sheets,
        calibration=calibration,source_anchor_proof=str(SOURCE_ANCHORS),source_anchor_sha256=sha(SOURCE_ANCHORS.read_bytes()),
        fresh_native_FE_ABI_alignments=4*len(proofs),new_credit=0,stored_actual_and_direct_visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in (STAGED,SOURCE_ANCHORS,Path(__file__))}))
    print(f'{len(proofs)} original FE panels passed exact row, glyph, bounds and four-alignment checks. Failures: {failures}')
    assert len(proofs)==22 and not failures


if __name__=='__main__':
    main()
