"""Native menu caption model:logical view inside observed256x36 backing,with room for the original pair flush."""
import inspect
from scripts import verify_ship_advice_choice_centering_20261022 as original
from dk4tool.patch.grand_race_menu_release import sha
SOURCE=inspect.getsource(original.paint)
def paint(arm,text,style,width,origin):
    assert 0<width<=228 and len(text)*6<=width and 0<=origin[0] and origin[0]+width+6<=256 and 0<=origin[1] and origin[1]+12<=36
    source=SOURCE
    changes={
        '    width, height = 48, 20':'    width,height=LOGICAL_WIDTH,12;backing_width,backing_height=256,36;origin_x,origin_y=VIEW_ORIGIN',
        'header, view, context, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000':'header,view,context,string=0x02450000,0x02460000,0x02461000,0x02462000',
        '    size = width * height // 2':'    size=backing_width*backing_height//2',
        "raw_header = struct.pack('<5I', 4, width // 4, height, 0x02452000 - header, 20)":"raw_header=struct.pack('<5I',4,backing_width//4,backing_height,0x02459000-header,20)",
        'call(cpu, 0xD3AFC, (view, header, 0, 0))':'call(cpu,0xD3AFC,(view,header,origin_x,origin_y))',
        '    x, y = (width - len(text) * 6) // 2, 4':'    x,y=origin_x+(width-len(text)*6)//2,origin_y',
        '    expected = bytearray(width * height)':'    expected=bytearray(backing_width*backing_height)',
        'expected[(y + yy) * width + x + index * 6 + xx]':'expected[(y+yy)*backing_width+x+index*6+xx]',
        'visible_center_twice = 2 * x + len(visible) * 6':'visible_center_twice=2*(x-origin_x)+len(visible)*6',
        "    return pixels, {'text': text.decode(), 'native_origin': [x, y],":"    whole=pixels;pixels=bytes(whole[(origin_y+yy)*backing_width+origin_x+xx] for yy in range(height) for xx in range(width))\n    return pixels, {'backing_width':backing_width,'backing_height':backing_height,'backing_plane_sha256':sha(whole),'logical_width_px':width,'logical_height_px':height,'source_view_origin':list(VIEW_ORIGIN),'extra_flush_stays_within_physical_backing':True,'storage_padding_all_blank':all(not p for i,p in enumerate(whole) if not(origin_x<=i%backing_width<origin_x+width and origin_y<=i//backing_width<origin_y+height)),'text':text.decode(),'native_origin':[x-origin_x,y-origin_y],'physical_native_origin':[x,y],"
    }
    for a,b in changes.items():assert source.count(a)==1,a;source=source.replace(a,b)
    env={**original.__dict__,'LOGICAL_WIDTH':width,'VIEW_ORIGIN':origin,'sha':sha};exec(compile(source,__file__+'::native-full-backing-logical-menu-view','exec'),env);pixels,proof=env['paint'](arm,text,style);proof['source_owned_adapter_sha256']=sha(source.encode());return pixels,proof
