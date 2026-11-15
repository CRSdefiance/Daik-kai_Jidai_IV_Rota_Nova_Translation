"""Preserve failed full-screen ownership inference;bind captions to directly observed glyph backing."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/audit_lil_B166_actual_menu_v4079.py');t=draft.read_text(encoding='utf-8').replace('native_menu_backing_surface_v4079','native_menu_backing_surface_v4080')
    start=t.index('            # The captured native full-bottom-screen view');end=t.index('cases=[]',start)+len('cases=[]')
    t=t[:start]+"            owner=read('work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json');assert not owner['errors'] and not owner['mismatches'];observed=owner['rows'][-1];view=observed['view_address'];words=observed['view_words'];header=observed['bitmap_header_address'];h=struct.unpack_from('<5I',raw,header-0x02000000);assert h[:3]==(4,64,36);pointer=(header+h[4])&0xFFFFFFFF;assert pointer==observed['backing_pointer'] and 0x02000000<=pointer and pointer+4608<=0x02400000;stored=raw[pointer-0x02000000:pointer-0x02000000+4608];pixels=bytes(n for b in stored for n in (b&15,b>>4));cases=[]\n"+t[end:]
    changes={
        "oy=rect[1]+12+option*20;native,proof=paint(arm,label.encode('ascii'),1,width,(origin_x,oy));expected=bytes(int(x==1) for x in native)":"oy=rect[1]+16+option*20;native,proof=paint(arm,label.encode('ascii'),8,width,(0,option*12));expected=bytes(int(x==8) for x in native)",
        'origin_x+width,192+oy+20':'origin_x+width,192+oy+12',
        "pixels[(oy+y)*256+origin_x+x]==1) for y in range(20)":"pixels[(option*12+y)*256+x]==8) for y in range(12)",
        '(206,199,181)':'(205,198,180)',
        'whole_bottom_screen_view=view':'observed_caption_view=view',
        'backing_bytes=24576':'backing_bytes=4608',
        'captured_native_bitmap_256x192_full_bottom_backing_bound=True':'captured_actual_native_caption_bitmap_256x36_backing_and54x12_views_bound=True',
        '256x192 backing bound':'256x36 glyph backing bound',
        "[FIXTURE,Path('scripts/native_menu_backing_surface_v4080.py')":"[DRAFT,Path('work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json'),FIXTURE,Path('scripts/native_menu_backing_surface_v4080.py')"
    }
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    anchor='    ROOT.mkdir(parents=True);sheet=';assert t.count(anchor)==1;t=t.replace(anchor,"    traced=read('work/analysis/lil_B166_menu_owner_trace_v4086/terminal.json');assert traced['terminal'] and traced['all_host_slots_restored'];tr=read(traced['report']);baseline=read(read(RUN/'reviewed_terminal.json')['report']);assert all(Image.open(next(x['path'] for x in tr['frames_captured'] if x['frame']==f)).convert('RGB').tobytes()==Image.open(next(x['path'] for x in baseline['frames_captured'] if x['frame']==f)).convert('RGB').tobytes() for f in [3000,3500])\n"+anchor)
    exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft))
