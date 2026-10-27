"""Derive independent B177 pending/history/reference audit with exact logical-tail bounds."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_relocation_audit_tools_v4628')
assert not root.exists()
tool=derive('scripts/verify_editorial_handoff_v4578.py','scripts/verify_editorial_handoff_v4628.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'editorial_handoff_verification_v4578':'editorial_handoff_verification_v4628',
    'relocation_checkpoint_v4577':'relocation_checkpoint_v4627',
    'editorial_manuscript_v3':'editorial_manuscript_v5','relocation_v4575':'relocation_v4625','stored_v4576':'stored_v4626',
    'lil_B176_reversible_relocation_v4577':'lil_B177_reversible_relocation_v4627',
    '==(5865,5878,3728,2137)':'==(5875,5888,3733,2142)',
    '==(5875,5865,10)':'==(5885,5875,10)',
    "len({historical_key(r) for r in fresh['record_keys']})==5875":"len({historical_key(r) for r in fresh['record_keys']})==5885",
    "['/data/SC2.DK4']==4022":"['/data/SC2.DK4']==4032",
    'unfinished_editorial_scope_v4573':'unfinished_editorial_scope_v4623',
    "scope['remaining_B177_B180_physical_speeches']==48":"scope['remaining_B178_B180_physical_speeches']==38",
    '==(40,16,24)':'==(40,24,16)','blocks[176]':'blocks[177]',"b['block']==176":"b['block']==177",
    '==(392,404,390,404)':'==(488,472,486,470)',
    '[(0xA000,8,8),(0xC200,384,398),(0,386,400)]':'[(0xA000,8,8),(0xC200,480,464),(0,482,466)]',
    '00a0ffff010a0da1':'00a0ffff01090fa1',
    'source[384:390]==target[398:404]':'source[480:486]==target[464:470]',
    'restored=bytearray(target)':'restored=bytearray(target[:b[\'research_logical_end\']])',
    "struct.pack_into('<H',restored,4,382)":"struct.pack_into('<H',restored,4,478)",
    'bytes(restored)==source[:390]':'bytes(restored)==source[:486]',
    "main['rom_sha256']==sha(Path(main['rom']).read_bytes())==doc['current_ROM_sha256']":
        "main['rom_sha256']==sha(Path(main['rom']).read_bytes())\n    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']\n    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4595'",
    'V4577 independently verified:5875 reread/5865 completed/10 pending':
        'V4627 independently verified:5885 reread/5875 completed/10 pending',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,complete_logical470_bytes_exclude_two_stored_padding_bytes=True,
    main_V4541_and_latest_V4595_bound_separately=True,no_new_review_orcompletion_credit=True,full_goal_complete=False))
