"""Measure the exact native menu painter at54/56/58/60 pixels;do not approve mismatches."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_menu_pixels_v4071')
if __name__=='__main__':
    assert not ROOT.exists();source=read('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json');arm=NdsImage.open(source['current_ROM']).read_file('/__arm9__.bin');text=inspect.getsource(prior.paint)
    changes={
        '    width, height = 48, 20':'    width, height = LABEL_WIDTH, 20',
        '    size = width * height // 2':'    stride=(width+3)//4*4;size=stride*height//2',
        "struct.pack('<5I', 4, width // 4, height,":"struct.pack('<5I', 4, stride // 4, height,",
        '    expected = bytearray(width * height)':'    expected = bytearray(stride * height)',
        'expected[(y + yy) * width + x + index * 6 + xx]':'expected[(y + yy) * stride + x + index * 6 + xx]',
        '    assert pixels == bytes(expected)':"    equal=pixels==bytes(expected)",
        "'independent_complete_native_pixels_match': True, 'style': style}":"'independent_complete_native_pixels_match':equal,'style':style,'logical_width':width,'storage_stride':stride,'actual_nonzero_bbox':[min((i%stride for i,p in enumerate(pixels) if p),default=None),min((i//stride for i,p in enumerate(pixels) if p),default=None),max((i%stride for i,p in enumerate(pixels) if p),default=None),max((i//stride for i,p in enumerate(pixels) if p),default=None)],'mismatches':[(i%stride,i//stride,a,b) for i,(a,b) in enumerate(zip(pixels,expected)) if a!=b][:20],'view64_hex':bytes(cpu.mem_read(view,64)).hex(),'context64_hex':bytes(cpu.mem_read(context,64)).hex(),'expected_hex':expected.hex()}"
    }
    for a,b in changes.items():assert text.count(a)==1,a;text=text.replace(a,b)
    ROOT.mkdir(parents=True);cases=[];pictures=[]
    for width in [54,56,58,60]:
        env={**prior.__dict__,'LABEL_WIDTH':width};exec(compile(text,__file__+'::source-painter-width-diagnostic','exec'),env)
        pixels,proof=env['paint'](arm,b'Please do',1);stride=proof['storage_stride'];expected=bytes.fromhex(proof.pop('expected_hex'))
        proof.update(actual_plane_sha256=sha(pixels),expected_plane_sha256=sha(expected));cases.append(proof)
        for label,data in [('actual',pixels),('expected',expected)]:
            im=Image.new('RGB',(stride,20));im.putdata([(8,8,8) if p else (239,232,201) for p in data]);pictures.append((f'width{width} stride{stride} {label}',im))
    sheet=Image.new('RGB',(700,480),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate(pictures):x,y=(i%2)*350,(i//2)*120;draw.text((x+5,y+5),label,fill='white');sheet.paste(im.resize((im.width*4,80),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'actual_and_expected_width_cases.png';sheet.save(path)
    save(ROOT/'width_cases_no_mismatch_approval.json',dict(source_ROM=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],cases=cases,source_owned_painter_diagnostic_adapter=text,comparison_assertion_replaced_only_to_record_failures_not_approve=True,no_menu_approval_or_credit=True,sheet=str(path),sheet_sha256=sha(path.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print([{k:r[k] for k in ['logical_width','storage_stride','native_origin','actual_nonzero_bbox','independent_complete_native_pixels_match','mismatches']} for r in cases])
