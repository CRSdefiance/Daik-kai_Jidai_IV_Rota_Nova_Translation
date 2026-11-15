"""Run stored parity/branch checks with exact market-successor dependency qualification."""
from pathlib import Path
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS,NEW_FORMAT,PAYLOAD
from scripts import check_editorial_stored_explicit_captain_v1 as previous
from scripts.check_editorial_stored_batch_v3 import compound_storage
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.check_editorial_compiled_pages_static_captain_v1 import SOURCE as PAGE_SOURCE
from scripts.qualify_maria270_market_parent_v1 import qualify
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def guard_market_independence(ctx,rebuilt):
    image,receipt=qualify(ctx.receipt())
    assert rebuilt['parent_sha256']==receipt['target_candidate_sha256']
    assert rebuilt['exact_registered_market_parent_reuse']==receipt
    original=ctx.machine
    protected=[(0x02000000+f,0x02000000+f+4) for f in FIELDS]+[(NEW_FORMAT,NEW_FORMAT+len(PAYLOAD))]
    def guarded(arm,common,raw,plan):
        cpu,get,provider=original(arm,common,raw,plan)
        def reject(u,access,address,size,value,unused):
            assert not any(address<end and start<address+size for start,end in protected),'Unexpected market-data dependency in stored speech/branch proof'
        def reject_code(u,address,size,unused):
            assert not any(address<end and start<address+size for start,end in protected),'Unexpected market literal/code execution in stored speech/branch proof'
        for start,end in protected:
            cpu.hook_add(UC_HOOK_MEM_READ,reject,begin=start,end=end-1)
            cpu.hook_add(UC_HOOK_CODE,reject_code,begin=start,end=end-1)
        return cpu,get,provider
    ctx.machine=guarded
    return receipt

def page_adapter(runtime,macros):
    # This is the exact adapter used by the completed initial page runner. Its
    # block receipts predate the later B50 abort, so restore its metadata from
    # the frozen common precedent rather than rerendering completed pages.
    assert runtime['ARM9_sha256']=='12e986d9625937d2d4141f7093e07fc16a474a129ee08a1043702952ac53f78d'
    precedent=load(PAGE_SOURCE)
    adapter=checked_text(precedent['source_owned_target_page_adapter'],{
        '12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b':runtime['ARM9_sha256']})
    return dict(source_owned_target_page_adapter=adapter,source_owned_progressive_macro_adapter=macros['source_owned_progressive_adapter'])

source=checked_text(previous.source,{
    "assert ctx.receipt()==runtime and rebuilt['parent_sha256']==runtime['candidate_sha256']":
        "assert ctx.receipt()==runtime\n    qualified_parent=guard_market_independence(ctx,rebuilt)",
    "assert image.read_file('/__arm9__.bin')==ctx.arm":
        "assert sha(image.read_file('/__arm9__.bin'))==qualified_parent['target_ARM9_sha256']",
    "    full_native=native;seen=set()\n    while 'source_owned_target_page_adapter' not in full_native:\n        prior=Path(full_native['previous_native']);assert str(prior) not in seen;seen.add(str(prior))\n        assert sha(prior.read_bytes())==full_native['previous_native_sha256']\n        full_native=load(prior)\n        assert full_native['runtime']==native['runtime'] and full_native['font_sha256']==native['font_sha256']":
        "    full_native=page_adapter(runtime,macros)",
    "{**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)}":
        "{**old_font.make_painter.__globals__,'CURRENT_ARM9':qualified_parent['target_ARM9_sha256']}",
    "{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory}":
        "{**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':qualified_parent['target_ARM9_sha256'],'ASCII_painter':ascii_factory}",
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
    "native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=ctx.receipt(),":
        "native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=ctx.receipt(), exact_registered_market_parent_reuse=qualified_parent, market_pointer_read_andexecution_dependency_guards_pass=True,",
})
exec(compile(source,__file__+'::same-stored-native-guards-narrow-registered-market-data-delta','exec'),globals())
