"""Execute native context/glyph rendering with bounded pixels.

The initialized font metrics and bitmap origin are explicit runtime contracts.
The optional Kanji asset enables the actual auto-loaded ITCM CP932 painter.
Existing bitmap/UI/physical routing and glyph-copy contracts remain explicit.
"""

import struct

from ndspy.code import MainCodeFile
from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

BASE = 0x02000000
CONTEXT, BITMAP, IMAGE, TEXT = 0x02400000, 0x02400100, 0x02400200, 0x02400300
BUFFER, STACK, STOP, GET_ORIGIN = 0x02500000, 0x027F0000, 0x027FFF00, 0x01FFF000


def execute(source, text, *, tracking=-1, x=18, y=70, mode=16, font_class='generic',
            wrapper=False, caller_mode=1, clear=0, footer_table=None, modal=False,
            tooltip=False, kanji_font=None, modal_guarded=False, portrait=False,
            surface_size=(256, 192), deck=False, audit_modal_legacy_guards=False,
            editor_title=False, editor_input=False, sailing_status=False, sword_stats=None,
            duel_actor_index=0, gallery_page=None, item_page=None, item_case=None,
            item_resource_index=None, item_common=None, item_menu=None,
            item_crew_owner=None, item_player_name=None, item_ship_owner=None, item_ship_name=None,
            item_promotional_seed=0, item_role_state=None, item_equipment_slot=None):
    raw = text.encode('cp932')
    if item_crew_owner is not None and (item_page != 'main' or item_resource_index is None):
        raise ValueError('Actual crew ownership requires the complete real main item caller')
    if item_player_name is not None and item_crew_owner is None:
        raise ValueError('Mutable captain name requires an actual item owner configuration')
    if (item_role_state is not None or item_equipment_slot is not None) and item_crew_owner is None:
        raise ValueError('Equipment role/slot requires an actual crew owner')
    if item_ship_owner is not None and (item_page != 'main' or item_resource_index is None or item_crew_owner is not None):
        raise ValueError('Actual ship ownership requires its exclusive complete real main item caller')
    if item_ship_name is not None and item_ship_owner is None:
        raise ValueError('Mutable ship name requires an actual ship owner configuration')
    if item_menu is not None:
        if footer_table is not None or len(item_menu) != 3 or item_menu[0] not in ('gallery', 'regular'):
            raise ValueError('Item menu requires its actual descriptor configuration')
        footer_table = 0x1156A8 if item_menu[0] == 'gallery' else 0x11627C
    if item_resource_index is not None and (item_page not in ('main', 'standalone')
                                           or not 0 <= item_resource_index < 218):
        raise ValueError('Real item data requires a mapped static/default/generated promotional index below 218')
    if item_common is not None and item_resource_index is None:
        raise ValueError('Actual item advice requires the native item resource index')
    if item_page is not None and (item_page not in ('counter', 'main', 'standalone')
                                 or item_case is None or kanji_font is None
                                 or surface_size != ((144, 36) if item_page == 'counter' else (240, 96))
                                 or modal or tooltip or wrapper or deck or editor_title or editor_input
                                 or sailing_status or sword_stats is not None or gallery_page is not None
                                 or footer_table is not None):
        raise ValueError('Item UI requires its mapped native surface, case and font')
    if item_page == 'counter' and (not isinstance(item_case, int) or not 0 <= item_case <= 198):
        raise ValueError('Gallery acquired count must be between zero and its native total 198')
    if item_page in ('main', 'standalone') and (len(item_case) not in (2, 4) or not 0 <= item_case[0] <= 255
                                              or item_case[1] not in (range(7) if item_page == 'main' else (0, 1))
                                              or len(item_case) == 4 and (not 0 <= item_case[2] <= 12
                                                                         or item_case[3] not in (*range(21), 24))):
        raise ValueError('Item detail requires native unsigned-byte effect and mapped owner kind')
    if gallery_page is not None and (gallery_page not in ('events', 'event-0', 'event-1', 'event-2', 'event-3', 'sites', 'site-name')
                                    or surface_size != (256, 192) or kanji_font is None
                                    or modal or tooltip or wrapper or deck or editor_title or editor_input
                                    or sailing_status or sword_stats is not None or footer_table is not None):
        raise ValueError('Gallery requires its mapped page and native 256x192 primary bitmap')
    if duel_actor_index not in (0, 1) or sword_stats is None and duel_actor_index:
        raise ValueError('Duel actor index requires one of the two mapped native stat slots')
    if sword_stats is not None and (surface_size != (156, 12) or modal or tooltip or wrapper
                                   or deck or editor_title or editor_input or sailing_status
                                   or footer_table is not None or font_class != 'generic'
                                   or kanji_font is None or len(sword_stats) != 3
                                   or not 0 <= sword_stats[0] <= 500 or not 0 <= sword_stats[1] <= 65535
                                   or sword_stats[2] not in (*range(7), 255)):
        raise ValueError('Sword statistics require the actual bitmap and mapped skill/HP/state ranges')
    if sailing_status and (surface_size != (256, 32) or modal or tooltip or wrapper
                           or deck or editor_title or editor_input or footer_table is not None
                           or font_class != 'generic' or kanji_font is None):
        raise ValueError('Sailing statuses require the actual 256-by-32 native bitmap/context')
    if editor_input and (editor_title or surface_size != (256, 192) or modal or tooltip
                         or wrapper or deck or footer_table is not None or font_class != 'generic'
                         or x != 0 or y != 0 or len(raw) > 18):
        raise ValueError('Editor input requires the mapped native child and at most 18 bytes')
    text_address = BITMAP + 0x6C if editor_input else TEXT
    if deck and (modal or tooltip or wrapper or footer_table is not None or font_class != 'generic'
                 or surface_size != (168, 84) or x != 0 or y != 0 or tracking != 0):
        raise ValueError('Deck text requires its mapped 168-by-84 bitmap and native zero origin/tracking')
    if editor_title and (surface_size != (108, 12) or modal or tooltip or wrapper or deck
                         or footer_table is not None or font_class != 'generic' or x != 0 or y != 0):
        raise ValueError('Editor title requires its mapped 108-by-12 native context')
    if surface_size not in ((256, 192), (128, 160), (168, 84), (108, 12), (256, 32), (156, 12), (144, 36), (240, 96)) or (surface_size in ((144, 36), (240, 96)) and item_page is None) or (surface_size == (156, 12) and sword_stats is None) or (surface_size == (256, 32) and not sailing_status) or (surface_size == (168, 84) and not deck) or (surface_size == (108, 12) and not editor_title) or (surface_size != (256, 192)
            and (modal or tooltip or wrapper or footer_table is not None)):
        raise ValueError('Unmapped native caption surface size')
    if portrait and not modal:
        raise ValueError('Portrait text requires the mapped modal renderer')
    if audit_modal_legacy_guards and (not modal or not modal_guarded):
        raise ValueError('Legacy guard audit requires an explicit modal invocation')
    if modal_guarded and (not modal or (not audit_modal_legacy_guards
                                      and any(not row.startswith('  ') for row in text.split('\n')[1:]))):
        raise ValueError('Guarded modal continuations require two machine spaces')
    if deck and any(not row.startswith('  ') for row in text.split('\n')[1:]):
        raise ValueError('Deck continuations require generated two-space guards')
    if not raw or any(c < 32 and not ((tooltip or modal_guarded or deck) and c == 10) for c in raw) or mode not in (4, 16):
        raise ValueError('Requires printable CP932 and a mapped pixel format')
    if font_class not in ('generic', 'controller-icons'):
        raise ValueError('Unmapped native font class')
    if wrapper and (font_class != 'generic' or caller_mode not in (0, 1) or clear not in (0, 1)):
        raise ValueError('Unmapped native wrapper arguments')
    if footer_table is not None and (footer_table not in (0x12EC10, 0x12EC28, 0x12EC3C, 0x1156A8, 0x11627C)
                                   or footer_table in (0x1156A8, 0x11627C) and item_menu is None or wrapper):
        raise ValueError('Unmapped Golden Route footer descriptor')
    if modal and (wrapper or footer_table is not None or font_class != 'generic'):
        raise ValueError('Unmapped native modal renderer combination')
    if tooltip and (modal or wrapper or footer_table is not None or font_class != 'generic'
                    or text.count('\n') != 1):
        raise ValueError('Unmapped native two-row map tooltip')
    if len(text) > (256 if audit_modal_legacy_guards else 100) or not 0 <= x <= 255 or not 0 <= y <= 181:
        raise ValueError('Unbounded caption raster input')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_map(0x01FFF000, 0x1000)
    machine.mem_map(0x01FF8000, 0x7000)
    machine.mem_write(BASE, bytes(source))
    itcm_ranges = []
    if kanji_font is not None:
        if len(kanji_font) != 3340 * 22:
            raise ValueError('Requires the complete 3340-cell native Kanji font')
        sections = [section for section in MainCodeFile(bytes(source), BASE).sections
                    if section.ramAddress == 0x01FF8000]
        if len(sections) != 1 or len(sections[0].data) not in (6944, 7596, 7704, 7900, 8160, 8172):
            raise ValueError('Native ITCM autoload section differs')
        section = sections[0]
        machine.mem_write(section.ramAddress, bytes(section.data))
        itcm_ranges.append((section.ramAddress, section.ramAddress + len(section.data)))
        font_pointer = struct.unpack_from('<I', source, 0xD19B8)[0]
        if not BASE + len(source) <= font_pointer < CONTEXT - len(kanji_font):
            raise ValueError('Native Kanji asset pointer outside initialized runtime storage')
        machine.mem_write(font_pointer, bytes(kanji_font))
    sailing_draws = []
    item_helper_ranges, item_helper_executed = [], set()
    if sailing_status or sword_stats is not None or gallery_page is not None or item_page is not None or item_menu is not None:
        staged = MainCodeFile(bytes(source), BASE).sections[3]
        if staged.ramAddress != 0x023A7200:
            raise ValueError('Sailing status pool stage differs')
        machine.mem_write(0x02387A20, bytes(staged.data[:-48]))
        if item_page is not None:
            # Permit only the private lookup functions reached by the four
            # source-locked call sites, never arbitrary late-pool execution.
            def branch_target(field):
                instruction = struct.unpack_from('<I', source, field)[0]
                if instruction >> 24 != 0xEB:
                    raise ValueError('Item projection is not a native BL')
                delta = instruction & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                return BASE + field + 8 + delta * 4

            role, type_wrapper = branch_target(0x4D690), branch_target(0x4D660)
            pool = 0x02387A20
            if role >= pool or type_wrapper >= pool:
                if not pool <= role < type_wrapper < pool + len(staged.data) - 48:
                    raise ValueError('Item helper starts escape their reserved payload')
                relative = type_wrapper - pool + 12
                instruction = struct.unpack_from('<I', staged.data, relative)[0]
                delta = instruction & 0xFFFFFF
                if instruction >> 24 != 0xEB:
                    raise ValueError('Item wrapper lookup is not BL')
                if delta & 0x800000:
                    delta -= 0x1000000
                lookup = type_wrapper + 20 + delta * 4
                if lookup != role + 36 or type_wrapper != lookup + 40 or type_wrapper + 24 > pool + len(staged.data) - 48:
                    raise ValueError('Private item getter extents differ')
                item_helper_ranges = [(role, role + 36), (lookup, lookup + 40), (type_wrapper, type_wrapper + 24)]
                advice = branch_target(0x4D834)
                if advice != branch_target(0x4E50C) or not type_wrapper + 24 <= advice <= pool + len(staged.data) - 96:
                    raise ValueError('Item advice helper escapes its reserved payload')
                item_helper_ranges.append((advice, advice + 48))
                paragraph = branch_target(0x4D840)
                if paragraph != advice + 48 or paragraph != branch_target(0x4E518) or paragraph + 76 > pool + len(staged.data) - 48:
                    raise ValueError('Item paragraph helper escapes its reserved payload')
                item_helper_ranges.append((paragraph, paragraph + 76))

    def put(address, *values):
        machine.mem_write(address, struct.pack('<' + 'I' * len(values), *values))

    def word(address):
        return struct.unpack('<I', machine.mem_read(address, 4))[0]

    put(BITMAP, BITMAP + 0x60)
    put(BITMAP + 0x68, GET_ORIGIN)
    put(BITMAP + 0x10, IMAGE, 5)
    put(BITMAP + 0x28, *surface_size)
    if surface_size != (256, 192):
        put(BITMAP + 0x30, 0, 0, *surface_size)
    pitch = 256 if mode == 16 else 64
    put(IMAGE, mode, pitch)
    put(IMAGE + 0x10, BUFFER - IMAGE)
    font_object = struct.unpack_from('<I', source, 0xD5088)[0]
    if not BASE + len(source) <= font_object < CONTEXT - 12:
        raise ValueError('Font metrics literal no longer names runtime state')
    put(font_object + 4, 6, 12)
    machine.mem_write(text_address, raw + b'\0')
    title_buffer = struct.unpack_from('<I', source, 0xD529C)[0] if editor_title or sailing_status or sword_stats is not None or item_page is not None else None
    size = pitch * 192 * 2
    background = b'\x09\x00' if mode == 16 else b'\x99\x99'
    machine.mem_write(BUFFER - 32, b'\xA5' * 32 + background * (size // 2) + b'\xA5' * 32)
    preserved = {reg: 0x11110000 + i for i, reg in enumerate((
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    for reg, value in preserved.items():
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    glyphs, cp932_glyphs, copies, executed, clear_calls = [], [], [], set(), []
    itcm_executed, cp932_font_flags = set(), []
    glyph_events = []
    views, footer_draws = set(), []
    tooltip_frame, tooltip_rect = BITMAP - 0x30, TEXT + 0x300
    tooltip_composites = []
    draw_context = CONTEXT
    actual_tracking = None
    item_menu_descriptor = None
    if item_menu is not None:
        from scripts.probe_item_advice_descriptor import prepare as prepare_item_menu
        item_menu_descriptor = prepare_item_menu(source, machine, *item_menu)
    stats_actor = TEXT + 0x200
    gallery_frame = BITMAP - 0x6028 - 0xA4
    gallery_draws = []
    item_draws, item_contracts, item_owner_classifications = [], [], []
    item_role_eligibility = []
    item_table, item_resource = TEXT + 0x1000, TEXT + 0x2000
    crew_table, ship_table = TEXT + 0x3000, TEXT + 0x4000
    item_title, item_description, crew_name, ship_name, item_advice = [TEXT + n for n in (0x100, 0x120, 0x140, 0x160, 0x180)]
    common_owner, common_expected, common_ids = None, None, []
    promotional_initialization = None
    item_object_initialization = None
    item_crew_initialization = None
    item_ship_initialization = None
    counter_bitmap = STACK + 0x20
    if item_page is not None:
        for pointer, value in ((item_title, b'Compass '), (item_description, b'Sailing '),
                               (crew_name, b'Raphael '), (ship_name, b'Falcon'),
                               (item_advice, b'Keep a steady course. ')):
            machine.mem_write(pointer, value + b'\0')
        put(item_table + 4, TEXT + 0x200)
        put(TEXT + 0x208, GET_ORIGIN + 8)
        put(crew_table + 4, TEXT + 0x240)
        put(TEXT + 0x260, GET_ORIGIN + 16)
        put(ship_table + 4, TEXT + 0x280)
        put(TEXT + 0x284, GET_ORIGIN + 12)
        put(item_resource + 4, 999999)
        category, attribute = item_case[2:] if item_page != 'counter' and len(item_case) == 4 else (1, 24)
        machine.mem_write(item_resource + 0x10, bytes((category, 0, attribute, 0 if item_page == 'counter' else item_case[0])))
        if item_resource_index is not None:
            item_table = struct.unpack_from('<I', source, 0xCB198)[0]
            if item_resource_index < 188:
                item_resource = BASE + 0x11E210 + item_resource_index * 24
            else:
                from scripts.probe_promotional_item_defaults import OWNER
                context = machine.context_save()
                if item_resource_index < 198:
                    from scripts.probe_promotional_item_defaults import (
                        verify as initialize_promotional,
                    )
                    promotional_initialization = initialize_promotional(source, machine)
                else:
                    from scripts.probe_promotional_item_full import (
                        verify as initialize_full_promotional,
                    )
                    promotional_initialization = initialize_full_promotional(source, item_promotional_seed, machine)
                # Restore the caller CPU state; retain the native name/metadata writes.
                machine.context_restore(context)
                item_resource = OWNER + 0x3E4 + (item_resource_index - 188) * 24
            # The actual metadata initializer and index/resource getters execute;
            # vtable seed and containing runtime table initialization are contracts.
            if struct.unpack_from('<I', source, 0x13C394)[0] != BASE + 0x4A53C:
                raise ValueError('Source item name virtual differs')
            from scripts.probe_item_native_initialization import initialize_item_object
            item_object_initialization = initialize_item_object(source, machine, item_resource_index)
            if item_crew_owner is not None:
                from scripts.prepare_item_crew_owner import prepare as prepare_crew_owner
                item_crew_initialization = prepare_crew_owner(source, machine, item_resource_index,
                                                              item_crew_owner, item_player_name,
                                                              item_role_state, item_equipment_slot)
            if item_ship_owner is not None:
                from scripts.prepare_item_ship_owner import prepare as prepare_ship_owner
                item_ship_initialization = prepare_ship_owner(source, machine, item_resource_index,
                                                              item_ship_owner, item_ship_name)
        if item_common is not None:
            from dk4tool.formats.ilnk import IlnkContainer
            from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries

            message_id = item_resource_index + 0xAFF
            entries = common_message_entries(item_common, source, clean=False)
            common_expected = entries[message_id].text
            directory = [struct.unpack_from('<HH', source, DIRECTORY_OFFSET + block * 4) for block in range(41)]
            block = max(i for i, (first, _) in enumerate(directory) if first <= message_id)
            common_owner = struct.unpack_from('<I', source, 0x552A0)[0]
            machine.mem_write(common_owner + 0x2C, bytes((block, 255, 0, 1)))
            machine.mem_write(common_owner + 0x30, IlnkContainer.parse(item_common).blocks[block])
            machine.mem_write(common_owner + 0x2030, b'\xA5' * 528)
        put(counter_bitmap, BITMAP + 0x60)
        put(counter_bitmap + 0x10, IMAGE, 5)
        put(counter_bitmap + 0x28, 144, 36)
        machine.mem_write(BUFFER, bytes(size))
        views.add(counter_bitmap)

    def code(uc, address, instruction_size, _):
        nonlocal draw_context, actual_tracking
        if item_page is not None:
            if item_role_state is not None and address == BASE + 0x4D73C:
                eligible = uc.reg_read(UC_ARM_REG_R0)
                expected = item_crew_initialization['role_initialization']['expected_eligible']
                if eligible != int(expected):
                    raise ValueError('Native equipment eligibility differs from the controlled assignment state')
                item_role_eligibility.append({'state': item_role_state, 'eligible': bool(eligible)})
            if (item_crew_owner is not None or item_ship_owner is not None) and address == BASE + 0x4D700:
                sp = uc.reg_read(UC_ARM_REG_SP)
                classification = list(struct.unpack('<2I', uc.mem_read(sp + 4, 8)))
                expected_owner = [2, item_crew_owner] if item_crew_owner is not None else [3, item_ship_owner]
                if classification != expected_owner:
                    raise ValueError('Native equipment search selected a different owner')
                item_owner_classifications.append(classification)
            value = None
            if address == GET_ORIGIN + 8:
                value = item_title
                item_contracts.append('item_title_provider')
            elif address == GET_ORIGIN + 12:
                value = ship_name
                item_contracts.append('ship_name_provider')
            elif address == GET_ORIGIN + 16:
                value = crew_name
                item_contracts.append('crew_name_provider')
            elif address == BASE + 0xCB190 and item_resource_index is None:
                value = item_table
                item_contracts.append('item_object_table_provider')
            elif address == BASE + 0xCDAFC and item_resource_index is None:
                if (uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)) != (0, 1):
                    raise ValueError('Native item index/property lookup differs')
                value = item_resource
                item_contracts.append('item_resource_provider')
            elif address == BASE + 0x476A4:
                if uc.reg_read(UC_ARM_REG_R2) != BITMAP - 0x30:
                    raise ValueError('Item detail art selects a different owner')
                value = 1
                item_contracts.append('item_art_provider_not_rendered')
            elif address == BASE + 0x49DE8 and item_crew_owner is None and item_ship_owner is None:
                put(uc.reg_read(UC_ARM_REG_R0), BASE + 0x13C12C, item_case[1], 0)
                value = uc.reg_read(UC_ARM_REG_R0)
                item_contracts.append('item_ownership_provider')
            elif address == BASE + 0xCB184 and item_crew_owner is None:
                value = crew_table
                item_contracts.append('crew_table_provider')
            elif address == BASE + 0xCB148 and item_ship_owner is None and item_role_state is None:
                value = ship_table
                item_contracts.append('ship_table_provider')
            elif address == BASE + 0x7F244 and item_crew_owner is None:
                value = 5
                item_contracts.append('current_captain_index_provider')
            elif address == BASE + 0x49A18 and item_crew_owner is None:
                value = 1
                item_contracts.append('owner_eligible_provider')
            elif address == BASE + 0x5528C and item_common is None:
                value = item_advice
                item_contracts.append('item_advice_common_provider')
            elif address == BASE + 0x5528C:
                selected_id = uc.reg_read(UC_ARM_REG_R0)
                if selected_id != item_resource_index + 0xAFF:
                    raise ValueError('Native item caller selected different COMMON advice')
                common_ids.append(selected_id)
            if value is not None:
                uc.reg_write(UC_ARM_REG_R0, value)
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
                return
        if sword_stats is not None and address == BASE + 0x7DCC8:
            if uc.reg_read(UC_ARM_REG_R0) != stats_actor or uc.reg_read(UC_ARM_REG_R1) != 5:
                raise ValueError('Actual stats caller selects a different actor or skill')
            executed.add(address - BASE)
            uc.reg_write(UC_ARM_REG_R0, sword_stats[0])
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if tooltip and address == GET_ORIGIN + 4:
            if uc.reg_read(UC_ARM_REG_R0) != BITMAP:
                raise ValueError('Tooltip queries an unmapped bitmap')
            uc.reg_write(UC_ARM_REG_R0, 1)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if tooltip and address == BASE + 0x6010:
            if uc.reg_read(UC_ARM_REG_R0) != struct.unpack_from('<I', source, 0x77F0)[0]:
                raise ValueError('Tooltip selects a different UI state')
            # Parent UI-state update contract; native measurement/draw execute.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if tooltip and address == BASE + 0xD351C:
            if uc.reg_read(UC_ARM_REG_R0) != tooltip_frame:
                raise ValueError('Tooltip composites an unmapped owner')
            tooltip_composites.append({'width': word(tooltip_frame + 0x68),
                                       'height': word(tooltip_frame + 0x6C),
                                       'rectangle': [word(tooltip_frame + n) for n in (0x20, 0x24, 0x28, 0x2C)]})
            # Physical parent composition contract; bitmap pixels are native.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if footer_table is not None and address == BASE + 0xD3CE0:
            view = uc.reg_read(UC_ARM_REG_R0)
            sp = uc.reg_read(UC_ARM_REG_SP)
            if uc.reg_read(UC_ARM_REG_R1) != BITMAP or word(sp) != 256 or word(sp + 4) != 12:
                raise ValueError('Footer surface view contract differs')
            if not STACK - 0x1000 <= view <= STACK - 0x30:
                raise ValueError('Footer surface view escapes bounded stack')
            uc.mem_write(view, bytes(0x30))
            put(view, BITMAP + 0x60)
            put(view + 0x10, IMAGE, 5)
            put(view + 0x28, 256, 12)
            views.add(view)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if footer_table is not None and address == BASE + 0xD3BD4:
            if uc.reg_read(UC_ARM_REG_R0) not in views:
                raise ValueError('Footer destroys an unmapped surface view')
            # Surface-view destructor contract; font cleanup remains native.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if address == BASE + 0xD393C and (wrapper or tooltip or editor_input or sword_stats is not None or gallery_page is not None or item_page is not None):
            # Whole bitmap clear contract; complete clear body is not executed.
            if uc.reg_read(UC_ARM_REG_R0) != BITMAP:
                raise ValueError('Wrapper clears a different bitmap')
            uc.mem_write(BUFFER, bytes(size))
            clear_calls.append(BITMAP)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if address == 0x01FF83AC:
            # Preserve the original request-only mode unless an exact font asset
            # is supplied, in which case the actual ITCM painter executes.
            sp = uc.reg_read(UC_ARM_REG_SP)
            if uc.reg_read(UC_ARM_REG_R1) != IMAGE:
                raise ValueError('CP932 painter selects a different image')
            cp932_glyphs.append({'code': word(sp), 'style': word(sp + 4),
                                'x': uc.reg_read(UC_ARM_REG_R2), 'y': uc.reg_read(UC_ARM_REG_R3)})
            glyph_events.append({'kind': 'cp932', **cp932_glyphs[-1]})
            if kanji_font is None:
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
                return
            cp932_font_flags.append(word(uc.reg_read(UC_ARM_REG_R0) + 12))
        if address == GET_ORIGIN:
            destination = uc.reg_read(UC_ARM_REG_R0)
            bitmap = uc.reg_read(UC_ARM_REG_R1)
            if bitmap not in views | {BITMAP} or not STACK - 0x1000 <= destination <= STACK - 8:
                raise ValueError('Unexpected bitmap origin getter')
            put(destination, 0, 0)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if any(lo <= address <= hi - instruction_size for lo, hi in itcm_ranges):
            itcm_executed.add(address)
            return
        if any(lo <= address <= hi - instruction_size for lo, hi in item_helper_ranges):
            item_helper_executed.add(address)
            return
        if not BASE <= address <= BASE + len(source) - instruction_size:
            raise ValueError(f'Raster escaped source at {address:08X}')
        executed.add(address - BASE)
        if address == BASE + 0xD5404:
            draw_context = uc.reg_read(UC_ARM_REG_R0)
            actual_tracking = word(draw_context + 0x1C)
            selected = uc.reg_read(UC_ARM_REG_R1)
            if footer_table is not None:
                if item_menu_descriptor is not None:
                    if selected not in item_menu_descriptor['words']:
                        raise ValueError('Footer selects text outside actual item descriptor')
                    label = bytes(machine.mem_read(selected, 128)).split(b'\0', 1)[0]
                else:
                    off = selected - BASE
                    if not 0 <= off < len(source):
                        raise ValueError('Footer selects text outside ARM9')
                    label = source[off:source.index(0, off)]
                if not label or any(not 32 <= value <= 126 for value in label):
                    raise ValueError('Footer native raster requires complete mapped ASCII')
                footer_draws.append({'pointer': selected, 'text': label.decode('ascii'),
                                     'x': word(draw_context + 0x24), 'y': word(draw_context + 0x28)})
            elif editor_title:
                title_expected = raw.ljust(17, b' ')
                if selected != title_buffer or bytes(machine.mem_read(selected, len(title_expected) + 1)) != title_expected + b'\0':
                    raise ValueError('Title printf renderer changes the complete label')
            elif sailing_status:
                index = len(sailing_draws)
                if index >= 2:
                    raise ValueError('Sailing status caller draws an unexpected extra label')
                pointer = struct.unpack_from('<I', source, (0x68A20, 0x68A24)[index])[0]
                expected = bytes(machine.mem_read(pointer, 64)).split(b'\0', 1)[0]
                actual = bytes(machine.mem_read(selected, 64)).split(b'\0', 1)[0]
                if (selected != title_buffer or actual != expected
                        or (word(draw_context + 0x24), word(draw_context + 0x28), actual_tracking)
                        != (60 + index * 60, 12, 0xFFFFFFFF)):
                    raise ValueError(f'Actual sailing formatter changes label, origin or tracking: {index}, '
                                     f'{selected:08X}/{title_buffer:08X}, {actual!r}/{expected!r}, '
                                     f'{word(draw_context + 0x24)}, {word(draw_context + 0x28)}, {actual_tracking}')
                sailing_draws.append({'text': actual.decode('ascii'), 'x': 60 + index * 60,
                                      'y': 12, 'tracking': actual_tracking})
            elif item_page is not None:
                value = bytes(machine.mem_read(selected, 512)).split(b'\0', 1)[0]
                if not value or actual_tracking != (0 if item_page == 'counter' else 0xFFFFFFFF):
                    raise ValueError('Item UI text or native tracking differs')
                item_draws.append({'pointer': selected, 'text': value.decode('cp932'),
                                   'x': word(draw_context + 0x24), 'y': word(draw_context + 0x28),
                                   'tracking': actual_tracking})
                if common_owner is not None and selected == common_owner + 0x2030 and value != common_expected:
                    raise ValueError('Actual item COMMON copy loses original complete bytes')
            elif gallery_page is not None:
                if actual_tracking != 0:
                    raise ValueError('Gallery native row uses unexpected tracking')
                value = bytes(machine.mem_read(selected, 256)).split(b'\0', 1)[0]
                if not value or any(not 32 <= c <= 126 for c in value):
                    raise ValueError('Gallery native field is not complete printable English')
                gallery_draws.append({'pointer': selected, 'text': value.decode('ascii'),
                                      'x': word(draw_context + 0x24), 'y': word(draw_context + 0x28),
                                      'tracking': actual_tracking})
            elif sword_stats is not None:
                if (selected != title_buffer or bytes(machine.mem_read(selected, len(raw) + 1)) != raw + b'\0'
                        or (word(draw_context + 0x24), word(draw_context + 0x28), actual_tracking) != (0, 0, 0xFFFFFFFF)):
                    raise ValueError('Actual fencing/HP/state formatter changes complete prose, origin or tracking')
            elif selected != text_address:
                raise ValueError('Wrapper renderer selects a different full string')
        elif address == BASE + 0xD16B4:
            sp = uc.reg_read(UC_ARM_REG_SP)
            glyphs.append({'code': word(sp), 'style': word(sp + 4),
                           'x': uc.reg_read(UC_ARM_REG_R2), 'y': uc.reg_read(UC_ARM_REG_R3)})
            glyph_events.append({'kind': 'ascii', **glyphs[-1]})
        elif address == BASE + 0xE2A5C:
            origin, destination, length = (uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
            if length != 11 or not BASE + 0x125A60 <= origin <= BASE + 0x125E75 - 11 or not STACK - 0x1000 <= destination <= STACK - 11:
                raise ValueError('Unexpected glyph copy contract')
            uc.mem_write(destination, bytes(uc.mem_read(origin, length)))
            copies.append(origin)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def write(uc, access, address, length, value, _):
        allowed = ((CONTEXT, CONTEXT + 0x4C), (STACK - 0x1000, STACK + 8),
                   (BUFFER, BUFFER + size), (font_object + 12, font_object + 16),
                   (BITMAP, BITMAP + 0x60))
        if tooltip:
            allowed += ((tooltip_frame, tooltip_frame + 0x80),)
        if editor_title or sailing_status or sword_stats is not None or item_page is not None:
            allowed += ((title_buffer, title_buffer + 1024),)
        if item_page is not None:
            allowed += ((STACK, STACK + 0xE0),)
            # Actual ABFCC rotating scratch formatter writes the separately
            # formatted price value; no mocked printf result is supplied.
            rotating = struct.unpack_from('<I', source, 0x4D87C)[0]
            allowed += ((rotating, rotating + 0x100C),)
            if common_owner is not None:
                allowed += ((common_owner + 0x2C, common_owner + 0x30),
                            (common_owner + 0x2030, common_owner + 0x2230))
        if sailing_status:
            allowed += ((STACK, STACK + 0x68),)
        if gallery_page is not None:
            allowed += ((gallery_frame, gallery_frame + 0x80),)
        if not any(lo <= address and address + length <= hi for lo, hi in allowed):
            raise ValueError(f'Unbounded native raster write at {address:08X}')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)

    def call(offset, arguments):
        for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
            machine.reg_write(reg, value)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + offset, STOP, timeout=10000000, count=1000000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native raster failed to return with intact stack')
        if any(machine.reg_read(reg) != value for reg, value in preserved.items()):
            raise ValueError('Native raster damaged preserved registers')

    if item_page == 'counter':
        machine.reg_write(UC_ARM_REG_R5, item_case)
        machine.emu_start(BASE + 0x44F6C, BASE + 0x44FA0, timeout=10000000, count=1000000)
        if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x44FA0
                or machine.reg_read(UC_ARM_REG_SP) != STACK
                or any(machine.reg_read(reg) != (item_case if reg == UC_ARM_REG_R5 else value)
                       for reg, value in preserved.items())
                or not {0xD5160, 0xD596C, 0xD5200, 0xD5404} <= executed):
            raise ValueError('Actual Gallery count caller/context/printf/renderer fails')
    elif item_page in ('main', 'standalone'):
        title = struct.unpack_from('<I', source, 0x4D260)[0]
        call(0x4D594 if item_page == 'main' else 0x4E3F0,
             (BITMAP - 0x40, item_resource_index or 0, title) if item_page == 'main'
             else (BITMAP, item_resource_index or 0, item_case[1]))
        if not {0x4A3A0, 0x4A3C0, 0x4A55C, 0xD5160, 0xD5404, 0xD5140} <= executed:
            raise ValueError('Item detail bypasses native byte getters, context or renderer')
        if item_resource_index is not None and not {0x4A53C, 0xCDAFC, 0xCB190} <= executed:
            raise ValueError('Real item name/table lookup did not execute')
        if promotional_initialization is not None and 0x102BB0 not in executed:
            raise ValueError('Promotional item lookup bypassed native dynamic metadata provider')
        if item_crew_initialization is not None:
            required = {0x49DE8, 0x7F044, 0xCB184, 0x7F244, 0x49A18}
            required.add(0x1371C if item_player_name is not None else 0x7EB0C)
            if not required <= executed:
                raise ValueError('Actual item crew ownership/name path did not execute')
            if item_owner_classifications != [[2, item_crew_owner]]:
                raise ValueError('Native ownership classification was not observed')
        if item_ship_initialization is not None and (
                not {0x49DE8, 0x4A6B0, 0xA3E5C, 0xCB148, 0x181A0, 0x353D4, 0x1A4E0} <= executed
                or item_owner_classifications != [[3, item_ship_owner]]):
            raise ValueError('Actual item ship search/classification/name path did not execute')
        if common_ids and (common_ids != [item_resource_index + 0xAFF]
                           or not {0x5528C, 0x534F4, 0x53628, 0x535E0, 0xCEC74} <= executed
                           or bytes(machine.mem_read(common_owner + 0x2230, 16)) != b'\xA5' * 16):
            raise ValueError('Native item COMMON selection/copy or output guard differs')
        if common_ids and bytes(machine.mem_read(common_owner + 0x2030, len(common_expected) + 1)) != common_expected + b'\0':
            raise ValueError('Native item COMMON cache copy changed stored source bytes')
    elif gallery_page is not None:
        if gallery_page.startswith('event'):
            machine.reg_write(UC_ARM_REG_R11, gallery_frame)
            # Actual event-page constants establish both description rows and
            # SL=frame+A4; the native draw segment selects all source fields.
            machine.emu_start(BASE + 0x42C2C, BASE + 0x42CE4, count=1000)
            if gallery_page == 'events':
                start, end = 0x42D20, 0x42D98
            else:
                put(gallery_frame + 0x1C, int(gallery_page[-1]))
                start, end = 0x42F70, 0x42FD0
            machine.emu_start(BASE + start, BASE + end, timeout=10000000, count=1000000)
            if machine.reg_read(UC_ARM_REG_PC) != BASE + end or machine.reg_read(UC_ARM_REG_SP) != STACK:
                raise ValueError('Gallery actual event draw sequence fails')
            expected_saved = dict(preserved)
            expected_saved.update({UC_ARM_REG_R4: 2, UC_ARM_REG_R5: 0, UC_ARM_REG_R6: 1,
                                   UC_ARM_REG_R10: BITMAP - 0x6028, UC_ARM_REG_R11: gallery_frame})
            if gallery_page == 'events':
                expected_saved[UC_ARM_REG_R7] = len(gallery_draws[0]['text'])
            if any(machine.reg_read(reg) != value for reg, value in expected_saved.items()):
                raise ValueError('Gallery event draw damages preserved caller state')
        else:
            call(0x44158, (BITMAP - 0x6028, TEXT if gallery_page == 'site-name' else 0))
        if not {0x456A0, 0xCED28, 0xD5160, 0xD5404, 0xD5140} <= executed:
            raise ValueError('Gallery bypasses actual centering, wrapper, context or renderer')
    elif sword_stats is not None:
        _skill, hp, state = sword_stats
        machine.mem_write(stats_actor + 6, bytes((state,)))
        machine.mem_write(stats_actor + 0x18, struct.pack('<H', hp))
        parent = BITMAP - 0x14 - 0x3C - duel_actor_index * 0xA4
        put(parent + 0x34 + duel_actor_index * 4, stats_actor)
        call(0xD54C, (parent, duel_actor_index))
        if not {0xD54C, 0xE290, 0x7DCC8, 0x7E19C, 0x7E0BC, 0x7E100, 0xD5200, 0xD5404, 0xD5140} <= executed:
            raise ValueError('Stats raster bypasses a mapped actual caller, getter, formatter or painter')
    elif sailing_status:
        machine.reg_write(UC_ARM_REG_R4, BITMAP - 0x30)
        machine.emu_start(BASE + 0x687E4, BASE + 0x6883C, timeout=10000000, count=1000000)
        if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x6883C
                or machine.reg_read(UC_ARM_REG_SP) != STACK or len(sailing_draws) != 2):
            raise ValueError('Actual sailing label context/printf/draw/cleanup fails')
        if any(machine.reg_read(reg) != (BITMAP - 0x30 if reg == UC_ARM_REG_R4 else value)
               for reg, value in preserved.items()):
            raise ValueError('Actual sailing label segment damages a preserved register')
    elif tooltip:
        put(BITMAP + 0x74, GET_ORIGIN + 4)
        put(tooltip_frame + 0x1C, 0)
        put(tooltip_frame + 0x78, 0)
        put(tooltip_rect, 0, 0, 256, 192)
        put(STACK, 0xFFFFFFFF)
        machine.reg_write(UC_ARM_REG_R3, 0)
        call(0x763C, (tooltip_frame, TEXT, tooltip_rect))
        if len(tooltip_composites) != 1:
            raise ValueError('Native tooltip does not complete one composite')
    elif modal:
        # Mode-zero dialog dimensions come from the native size table used
        # by 54774. Parent construction/physical bitmap routing is a contract.
        width, height = struct.unpack_from('<2I', source, 0x118AE8)
        if (width, height) != (256, 96):
            raise ValueError('Native mode-zero dialog dimensions differ')
        put(BITMAP + 0x28, width, height)
        put(BITMAP + 0x30, 0, 0, width, height)
        put(BITMAP + 0x48, 0, 0)
        if portrait:
            # Native 54DB0 constructor initializes these two fields. D4DA0
            # consumes their address in 548A8; its current native body is a no-op.
            put(BITMAP + 0x40, 8, 16)
        dialog_state = struct.unpack_from('<I', source, 0x54984)[0]
        if not BASE + len(source) <= dialog_state < CONTEXT - 0x58:
            raise ValueError('Modal runtime state literal differs')
        put(dialog_state + 0x54, 0)
        call(0x548A8, (BITMAP, TEXT))
    elif footer_table is not None:
        call(0xCA890, (BITMAP, item_menu_descriptor['pointer'] if item_menu_descriptor else BASE + footer_table))
    elif wrapper:
        put(STACK, y, caller_mode)
        machine.reg_write(UC_ARM_REG_R3, x)
        call(0x456A0, (BITMAP - 0x6028, clear, TEXT))
    elif editor_input:
        call(0xB0C70, (BITMAP - 0x10,))
    elif editor_title:
        call(0xAC378, (CONTEXT, BITMAP, 1))
        put(CONTEXT + 0x30, 15)  # actual B02A4 title color assignment
        template = struct.unpack_from('<I', source, 0xB0460)[0]
        offset = template - BASE
        if source[offset:source.index(0, offset)] != b'%-17s':
            raise ValueError('Actual editor title printf template differs')
        call(0xD5200, (CONTEXT, template, TEXT))
        call(0xAC358, (CONTEXT,))
    else:
        call(0xD5160, (CONTEXT, BITMAP, 1))
        if font_class == 'controller-icons':
            put(CONTEXT, BASE + 0x152DB8)
        put(CONTEXT + 0x1C, tracking & 0xFFFFFFFF)
        put(CONTEXT + 0x24, x, y)
        call(0xD5404, (CONTEXT, TEXT))
    if bytes(machine.mem_read(BUFFER - 32, 32)) != b'\xA5' * 32 or bytes(machine.mem_read(BUFFER + size, 32)) != b'\xA5' * 32:
        raise ValueError('Pixel buffer guard changed')
    footer_metadata = (list(struct.unpack('<18h', machine.mem_read(BITMAP + 0x2C, 36)))
                       if footer_table is not None else None)
    return {'glyphs': glyphs, 'cp932_glyphs': cp932_glyphs, 'copy_calls': len(copies), 'executed_offsets': sorted(executed),
            'final_x': word(draw_context + 0x24), 'pixels': bytes(machine.mem_read(BUFFER, size)),
            'actual_tracking': actual_tracking, 'clear_calls': clear_calls,
            'sailing_status_draws': sailing_draws,
            'gallery_draws': gallery_draws,
            'item_draws': item_draws, 'item_provider_contracts': sorted(set(item_contracts)),
            'item_pool_executed_addresses': sorted(item_helper_executed),
            'item_actual_resource_index': item_resource_index,
            'item_actual_common_ids': common_ids,
            'item_promotional_default_initialization': promotional_initialization,
            'item_native_object_metadata_initialization': item_object_initialization,
            'item_crew_owner_initialization': item_crew_initialization,
            'item_ship_owner_initialization': item_ship_initialization,
            'item_actual_owner_classifications': item_owner_classifications,
            'item_actual_role_eligibility': item_role_eligibility,
            'item_menu_descriptor': item_menu_descriptor,
            'stats_effective_skill_and_bitmap_clear_are_contracts': sword_stats is not None,
            'footer_draws': footer_draws, 'footer_metadata': footer_metadata,
            'tooltip_composites': tooltip_composites,
            'itcm_executed_addresses': sorted(itcm_executed),
            'cp932_font_flags': cp932_font_flags,
            'glyph_events': glyph_events,
            'cp932_pixel_painter_is_contract': kanji_font is None,
            'footer_labels': (list(struct.unpack('<6I', machine.mem_read(BITMAP + 0x14, 24)))
                              if footer_table is not None else None),
            'stack_and_registers_preserved': True}
