"""Source-exact current COMMON parser and both actual autoloaded ITCM sections."""
import inspect
from dk4tool.patch.modal_cursor_guard import OFFSET,POOL,buffered_helper
from ndspy.code import MainCodeFile
from scripts.execute_scene_caption_raster import execute as original
from scripts.source_locked_derivation_v5118 import checked_text
EXTRA='''        extra_sections=[s for s in MainCodeFile(bytes(source),BASE).sections if s.ramAddress<BASE and s.ramAddress!=section.ramAddress]
        assert len(extra_sections)==1 and len(extra_sections[0].data)==4096
        extra=extra_sections[0]
        assert extra.ramAddress==CURRENT_EXTRA_ITCM_ADDRESS and bytes(extra.data)==CURRENT_EXTRA_ITCM_BYTES
        machine.mem_write(extra.ramAddress,bytes(extra.data))
        itcm_ranges.append((extra.ramAddress,extra.ramAddress+len(extra.data)))'''
CURSOR_APPEND='                assert bytes(staged.data[CURRENT_CURSOR_ENTRY-pool:CURRENT_CURSOR_ENTRY-pool+len(CURRENT_CURSOR_BYTES)])==CURRENT_CURSOR_BYTES\n                item_helper_ranges.append((CURRENT_CURSOR_ENTRY,CURRENT_CURSOR_ENTRY+len(CURRENT_CURSOR_BYTES)))'
SOURCE=checked_text(inspect.getsource(original),{
    'from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries':'from dk4tool.script.common_message_table import DIRECTORY_OFFSET\n            from dk4tool.patch.duel_editorial import owned_entries as current_owned_entries',
    'entries = common_message_entries(item_common, source, clean=False)':'entries = current_owned_entries(item_common, source, CURRENT_DIRECTORY_SHA256)',
    '                item_helper_ranges.append((paragraph, paragraph + 76))':'                item_helper_ranges.append((paragraph, paragraph + 76))\n'+CURSOR_APPEND,
    '        itcm_ranges.append((section.ramAddress, section.ramAddress + len(section.data)))':'        itcm_ranges.append((section.ramAddress, section.ramAddress + len(section.data)))\n'+EXTRA,
})
def make_execute(directory,arm):
    sections=MainCodeFile(arm,original.__globals__['BASE']).sections;assert len(sections)==5
    assert arm[OFFSET+3]==0xEA
    cursor=original.__globals__['BASE']+OFFSET+8+int.from_bytes(arm[OFFSET:OFFSET+3],'little',signed=True)*4
    cursor_bytes=buffered_helper(cursor);payload=bytes(sections[3].data[:-48]);assert payload[cursor-POOL:cursor-POOL+len(cursor_bytes)]==cursor_bytes
    extra=sections[-1];assert extra.ramAddress<original.__globals__['BASE'] and len(extra.data)==4096
    env={**original.__globals__,'CURRENT_DIRECTORY_SHA256':directory,'CURRENT_EXTRA_ITCM_ADDRESS':extra.ramAddress,'CURRENT_EXTRA_ITCM_BYTES':bytes(extra.data),'CURRENT_CURSOR_ENTRY':cursor,'CURRENT_CURSOR_BYTES':cursor_bytes}
    exec(compile(SOURCE,__file__+'::current-source-exact-sections','exec'),env)
    def run(source,*args,**kwargs):
        assert source==arm
        return env['execute'](source,*args,**kwargs)
    return run
