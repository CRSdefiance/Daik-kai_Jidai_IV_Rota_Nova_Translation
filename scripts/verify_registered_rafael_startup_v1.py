"""Reuse exact reviewed Rafael startup RGB while checking the successor's own RAM."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_registered_startup_v8 import source as previous

source=checked_text(previous,{
    'from dk4tool.rom.nds import NdsImage':
        'from dk4tool.rom.nds import NdsImage\nfrom dk4tool.patch.reviewed_name_catalog import ROUTE',
    "    previous_capture_path=Path(parent['capture_report'])":
        """    approval_path=Path(args.parent_startup).parent/'direct_visual_andcontext_approval_v1.json'
    approval=load(approval_path)
    assert approval['context_sha256']==sha(args.parent_startup.read_bytes())
    assert Path(approval['context'])==args.parent_startup
    assert approval['all_six_key_frames_directly_viewed'] and len(parent['captures'])==6
    assert approval['ordinary_title_NewGame_Rafael_selection_andfirst_opening_scene_observed']
    assert approval['review_sheet_sha256']==parent['review_sheet_sha256']
    assert parent['actual_captain_getter']==parent['actual_route_word']==0
    assert not any('RIGHT' in r['buttons'] for r in capture['scripted_input_schedule'])
    previous_capture_path=Path(parent['capture_report'])""",
    'assert captain==1 and bytes(cpu.mem_read(BASE,0x400000))==before':
        "assert captain==0 and int.from_bytes(cpu.mem_read(ROUTE,4),'little')==0 and bytes(cpu.mem_read(BASE,0x400000))==before",
    "six_key_frames_directly_viewed=parent['six_key_frames_directly_viewed'],":
        "six_key_frames_directly_viewed=approval['all_six_key_frames_directly_viewed'],",
    'ordinary_title_NewGame_Hodram_Joakim_Bergstrom_andopening_observed=True,':
        'ordinary_title_NewGame_Rafael_Castor_andopening_observed=True,actual_route_word=0,',
    "        parent_startup=str(args.parent_startup),parent_startup_sha256=sha(args.parent_startup.read_bytes()),":
        "        parent_startup=str(args.parent_startup),parent_startup_sha256=sha(args.parent_startup.read_bytes()),\n        parent_visual_approval=str(approval_path),parent_visual_approval_sha256=sha(approval_path.read_bytes()),",
    'Own4001-frame registered cold boot,all10 exact RGB pairs,current captain1,payload andprotected names pass;no old RAM overlay.':
        'Own4001-frame Rafael coldboot,all exact RGB pairs,current captain0/route0,payload andprotected names pass;no old RAM overlay.',
})
exec(compile(source,__file__+'::same-own-ROM-snapshot-explicit-Rafael-andprior-exact-RGB','exec'),globals())
