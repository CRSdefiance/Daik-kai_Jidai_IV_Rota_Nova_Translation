"""Admit only the exact compiled registered cursor helper reached by the current painter."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    addition="""                assert bytes(staged.data[CURRENT_CURSOR_ENTRY-pool:CURRENT_CURSOR_ENTRY-pool+len(CURRENT_CURSOR_BYTES)])==CURRENT_CURSOR_BYTES
                item_helper_ranges.append((CURRENT_CURSOR_ENTRY,CURRENT_CURSOR_ENTRY+len(CURRENT_CURSOR_BYTES)))"""
    print(derive('scripts/current_item_detail_machine_v6102.py','scripts/current_item_detail_machine_v6102b.py',{
        'import inspect':'import inspect\nfrom dk4tool.patch.modal_cursor_guard import OFFSET,POOL,buffered_helper',
        'SOURCE=checked_text': 'CURSOR_APPEND='+repr(addition)+'\nSOURCE=checked_text',
        "    '        itcm_ranges.append((section.ramAddress, section.ramAddress + len(section.data)))':":"    '                item_helper_ranges.append((paragraph, paragraph + 76))':'                item_helper_ranges.append((paragraph, paragraph + 76))\\n'+CURSOR_APPEND,\n    '        itcm_ranges.append((section.ramAddress, section.ramAddress + len(section.data)))':",
        '    extra=sections[-1];assert extra.ramAddress':"    assert arm[OFFSET+3]==0xEA\n    cursor=original.__globals__['BASE']+OFFSET+8+int.from_bytes(arm[OFFSET:OFFSET+3],'little',signed=True)*4\n    cursor_bytes=buffered_helper(cursor);payload=bytes(sections[3].data[:-48]);assert payload[cursor-POOL:cursor-POOL+len(cursor_bytes)]==cursor_bytes\n    extra=sections[-1];assert extra.ramAddress",
        "'CURRENT_EXTRA_ITCM_BYTES':bytes(extra.data)":"'CURRENT_EXTRA_ITCM_BYTES':bytes(extra.data),'CURRENT_CURSOR_ENTRY':cursor,'CURRENT_CURSOR_BYTES':cursor_bytes",
    }))
    print(derive('scripts/prove_shachihoko_detail_fonts_v6101b.py','scripts/prove_shachihoko_detail_fonts_v6101c.py',{
        'scripts.current_item_detail_machine_v6102 import':'scripts.current_item_detail_machine_v6102b import',
        "Path('scripts/current_item_detail_machine_v6102.py')":"Path('scripts/current_item_detail_machine_v6102b.py')",
    }))
