"""Recheck only final FE parity padding through the frozen native replay."""
import ast
import struct
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_lil_london_FE_v1896 as original
from scripts.verify_lil_FE_display_v1737 import snapshots,OBS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_FE_parity_v1900')
RELOC=Path('work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json')
PRIOR=Path('work/analysis/lil_London_FE_v1896/all3_FE_native_planes_and_actual_mode_reconciliation.json')

if __name__=='__main__':
    assert not ROOT.exists()
    relocation,prior=map(read,(RELOC,PRIOR))
    arm=NdsImage.open(relocation['candidate']).read_file('/__arm9__.bin')
    captured=next(r for r in read(OBS)['rows'] if r.get('complete_readonly_snapshots'))
    data=snapshots(captured)
    bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    descriptor=bitmap[4]
    header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    assert header[1:3]==(72,48)
    env={**original.__dict__, 'arm':arm,'data':data,'captured':captured,'ctx':captured['context'],
        'pixels_address':(descriptor+header[4])&0xffffffff,'header':header,'width':288,'font':GameAsciiFont.from_arm9(arm)}
    # Reuse the exact frozen render function,including its native input guards,
    # independent pixels,complete glyph order andone-page return-pointer checks.
    source=Path(original.__file__).read_bytes()
    functions=[n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.FunctionDef) and n.name=='render']
    assert len(functions)==1
    exec(compile(ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])),str(original.__file__),'exec'),env)
    cases=[]
    for r in relocation['text_records']:
        if r['consumer']!='original_FE_modal_5473C_mode1':continue
        target=bytes.fromhex(r['target_hex'])
        assert target[:1]==b'\xfe'
        old=next(v for v in prior['cases'] if v['id']==r['id'])
        assert target==bytes.fromhex(old['encoded_hex'])+(b' ' if r['parity_space_added'] else b'')
        logical,physical,events=env['render'](target[1:])
        assert sha(logical)==old['native_plane_sha256']
        preview=Image.new('RGB',(228,64))
        preview.putdata([(0,8,0) if v else (239,232,201) for v in physical])
        assert preview.tobytes()==Image.open(old['preview']).convert('RGB').tobytes()
        cases.append(dict(id=r['id'],target_hex=r['target_hex'],parity_space_added=r['parity_space_added'],
            complete_native_independent_plane_byte_exact_to_reviewed=True,
            exact_target_consumed_on_one_page=True,original_preview=old['preview'],logical_plane_sha256=sha(logical)))
    assert len(cases)==3
    ROOT.mkdir(parents=True)
    save(ROOT/'all3_final_FE_parity_native_planes.json',dict(relocation=str(RELOC),relocation_sha256=sha(RELOC.read_bytes()),
        prior_proof=str(PRIOR),prior_proof_sha256=sha(PRIOR.read_bytes()),cases=cases,
        frozen_renderer=str(original.__file__),frozen_renderer_sha256=sha(source),
        only_final_parity_targets_reexecuted_old_actual_checks_inherited=True,
        all3_complete_padded_targets_one_native_page_and_pixel_exact=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(final_FE_native_cases=3,parity_spaces=sum(r['parity_space_added'] for r in cases),all_reviewed_planes_exact=True))
