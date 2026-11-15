"""Independent B52 native providers and existing actual caption/highlight RGB.

Native backing bounds remain offline evidence. No live owner/RAM/VRAM/palette
or backing-byte identity is inferred from these screenshots.
"""
import json
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract
from dk4tool.dialogue.hodram_B52_choices_v1 import compile_choices
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.square_shopkeeper_font_oracles_v7020 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as original_expected
from scripts.prove_lil_B208_name_planes_v6405 import codes


def check_menu_actual(data, doc, parent, load, require):
    frozen = contract()
    provider, source, declared = data['menu_provider'], data['source_menu_VM'], data['menu_actual']
    trusted = Path('work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json')
    require(sha(trusted.read_bytes()) == frozen['dependencies'][str(trusted.resolve())], 'frozen original menu adapter owner')
    adapter = json.loads(trusted.read_bytes())['source_owned_VM_adapter']
    require(provider['source_owned_VM_adapter'] == source['source_owned_VM_adapter'] == adapter, 'exact trusted original menu VM adapter')
    require(declared['no_new_owner_pointer_RAM_VRAM_palette_orunowned_backing_byte_identity_claim'], 'actual RGB versus offline backing scope')
    require(declared['menu_backing_native_bounds_remain_the_separate_offline_native_plane_proof'], 'native backing scope remains offline')
    arm, font = parent.read_file('/__arm9__.bin'), parent.read_file('/GRP/KANJI.FNT')
    require(sha(arm) == doc['current_ARM9_sha256'] == source['ARM9_sha256'] == frozen['runtime_component_hashes']['/__arm9__.bin'], 'exact original menu runtime')
    require(sha(font) == frozen['runtime_component_hashes']['/GRP/KANJI.FNT'], 'exact original menu font')
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data[:-48])
    require(len(payload) == 123264, 'complete current staged payload')
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=payload)]
    executed = set()

    def machine(value):
        require(value == arm, 'original menu machine input')
        cpu = original.machine(value)

        def exact(u, pc, size, unused):
            hits = [s for s in owners if s.ramAddress <= pc and pc+size <= s.ramAddress+len(s.data)]
            require(len(hits) == 1, 'unique original menu instruction owner')
            owner = hits[0]
            at = pc-owner.ramAddress
            require(bytes(u.mem_read(pc, size)) == bytes(owner.data[at:at+size]), 'every executed original menu instruction byte')
            executed.add(pc)

        cpu.hook_add(UC_HOOK_CODE, exact)
        return cpu

    env = {**original.__dict__, 'machine': machine}
    exec(compile(adapter, __file__ + '::trusted-menu-provider', 'exec'), env)
    tables = [dict(version='clean_Japanese', object_hex=source['source_choice']['command']['whole_command_hex'], cases=source['even_alignment_provider_cases'])]
    require([v['version'] for v in provider['versions']] == ['current-padded-English', 'reviewed-stored-English'], 'exact current/reviewed provider membership')
    tables += provider['versions']
    source_command = next(c for c in frozen['source_control_binding']['exact_original_source_commands'] if c['word'] == 0x2100)
    require(tables[0]['object_hex'] == source_command['whole_command_hex'], 'complete frozen clean Japanese menu object')
    current_block = IlnkContainer.parse(parent.read_file('/data/SC1.DK4')).blocks[52]
    require(tables[1]['object_hex'] == current_block[68:104].hex(), 'complete current English native menu object')
    typed = compile_choices(doc['typed_choice_records'])
    require(tables[2]['object_hex'] == typed.hex() and len(typed) == 32, 'complete ordered native two-choice object')
    computed = {}
    for entry in tables:
        raw = bytes.fromhex(entry['object_hex'])
        require(len(entry['cases']) == 2, 'both original even alignments')
        for alignment, case in zip([0, 2], entry['cases'], strict=True):
            result = env['choice_vm'](arm, raw, alignment)
            require(case['alignment'] == alignment and case['native_VM'] == result, 'complete independent native menu result:' + entry['version'])
            require([(r['modal_selection'], r['VM_state']) for r in result['VM_cases']] == [(0, 2), (1, 2), (-1, 0)], 'original bridged result-kind mapping')
            require(all(r['next_command_delta'] == len(raw) and r['original_dispatch_ABI_and_guards_pass'] for r in result['VM_cases']), 'complete native command consumption/ABI guards')
        computed[entry['version']] = result
    require(computed['clean_Japanese']['native_menu_rectangle'] == computed['current-padded-English']['native_menu_rectangle'] == [70, 64, 186, 128], 'source/current width84 geometry')
    require(computed['reviewed-stored-English']['native_menu_rectangle'] == [76, 64, 180, 128], 'reviewed width72 geometry')
    require(computed['current-padded-English']['native_width_units'] == [14, 12] and computed['reviewed-stored-English']['native_width_units'] == [11, 12], 'only unspoken storage padding removed')
    oracle_env = {**original_expected.__globals__, 'WIDTH': 256, 'HEIGHT': 36}
    exec(compile(PROGRESSIVE_ORACLE_SOURCE, __file__ + '::independent-font', 'exec'), oracle_env)
    oracle = oracle_env['expected_pixels']
    require(len(declared['groups']) == 4 and {(r['version'], r['choice']) for r in declared['groups']} == {(v, i) for v in ['clean_Japanese', 'revised_English'] for i in [0, 1]}, 'all four actual menu cases')
    summaries = []
    for group in declared['groups']:
        version, choice = group['version'], group['choice']
        actual = data['withdrawal' if choice == 0 else 'opposition']
        require(not actual['unresolved'], 'actual body/name/flow proof unresolved')
        actual_group = next(r for r in actual['groups'] if r['version'] == version)
        pair = next(r for r in actual_group['command_pairs'] if r['word'] == 0x2100)
        require(group['actual_menu_pair'] == pair and pair['native_result'] == [2, choice], 'exact observed ordinary controller selection')
        require(group['capture_report'] == actual_group['capture_report'], 'actual report identity')
        report = load(group['capture_report'])
        require(report['ROM_sha256'] == actual_group['fixture']['research_ROM_sha256'], 'actual fixture/report binding')
        vm = computed['clean_Japanese' if version == 'clean_Japanese' else 'reviewed-stored-English']
        rect, width = vm['native_menu_rectangle'], vm['minimum_width_units']*6
        require(group['constructor_rectangle'] == rect and group['logical_width_px'] == width and group['labels'] == vm['labels'], 'constructor-derived labels and geometry')
        x = rect[0]+16
        require(x == (256-width)//2, 'constructor-based caption coordinate')
        masks = []
        for label in vm['labels']:
            points = codes(label.encode('cp932'))
            advance = sum(6 if c < 128 else 12 for c in points)
            cursor = (width-advance)//2
            events = []
            require(cursor >= 0, 'complete centered caption fits')
            for code in points:
                events.append(dict(kind='ascii' if code < 128 else 'cp932', code=code, style=8, x=cursor, y=0))
                cursor += 6 if code < 128 else 12
            require(cursor <= width, 'complete final caption character fits')
            plane = oracle(arm, font, events, canvas_height=12)
            ink = {(at % 256, at // 256) for at, value in enumerate(plane) if value}
            require(ink and all(0 <= xx < width and 0 <= yy < 12 for xx, yy in ink), 'complete glyph bounds')
            masks.append(ink)
        require([s['frame'] for s in group['samples']] == [4090, 4150, 4210], 'three original actual menu samples')
        for sample in group['samples']:
            frame = sample['frame']
            photo = next(p for p in report['frames_captured'] if p['frame'] == frame)
            require(sample['capture'] == photo and sha(Path(photo['path']).read_bytes()) == photo['PNG_sha256'], 'whole actual PNG identity')
            require(pair['start']+20 < frame < pair['returned']-4, 'captured menu interval')
            im = Image.open(photo['path']).convert('RGB')
            require(im.size == (256, 384), 'whole actual framebuffer dimensions')
            selected = 1 if choice == 1 and frame > 4105 else 0
            require(sample['native_selected_option_expected_from_ordinary_input'] == selected and len(sample['labels']) == 2, 'selection from unchanged ordinary input')
            visible_selected = []
            for index, ink in enumerate(masks):
                y = 192+rect[1]+16+20*index
                caption = sample['labels'][index]
                require(caption['option_index'] == index and caption['label'] == vm['labels'][index] and caption['caption_origin'] == [x, y] and caption['logical_view'] == [width, 12], 'exact actual caption source/index/geometry')
                black = {(xx-x, yy-y) for yy in range(y-1, y+13) for xx in range(x-2, x+width+2) if im.getpixel((xx, yy)) == (8, 8, 8)}
                require(black == ink, 'all leading/internal/final native glyphs and blank guards')
                digest = sha(bytes(int((xx, yy) in ink) for yy in range(12) for xx in range(width)))
                require(caption['independent_font_mask_sha256'] == digest, 'independent complete caption-mask identity')
                positions = {(xx, yy) for yy in range(y-4, y+16) for xx in range(x, x+width)} - {(x+xx, y+yy) for xx, yy in ink}
                cyan = {p for p in positions if im.getpixel(p) == (0, 165, 172)}
                visible = bool(cyan)
                require((cyan == positions and index == selected) or not cyan, 'complete correct selected highlight')
                background = (0, 165, 172) if visible else (205, 198, 180)
                require(all(im.getpixel(p) == background for p in positions), 'complete original visible background')
                require(caption['selected'] == (index == selected) and caption['highlight_visible'] == visible, 'declared actual highlight/blink phase')
                require(caption['complete_leading_internal_final_glyphs_andblank_guards_equal'] and caption['native_background_pixels_exact'], 'complete actual caption claims')
                if visible:
                    visible_selected.append(index)
            require(sample['visible_selected_option_index'] == (visible_selected[0] if visible_selected else None), 'original highlight blink-off retained')
            summaries.append(dict(version=version, choice=choice, frame=frame, visible_selected=visible_selected, two_complete_caption_masks_equal=True))
    require(len(summaries) == declared['actual_menu_samples'] == 12 and declared['complete_actual_caption_glyph_andbackground_checks'] == 24, 'all twelve actual menus/twenty-four captions')
    return dict(native_provider_alignments=6, bridged_modal_returns=18, actual_menu_samples=12, actual_caption_checks=24,
        native_geometry_andoriginal_result_channels_exact=True, actual_visible_RGB=summaries,
        offline_backing_bounds_separate_no_live_owner_RAM_VRAM_palette_orbacking_identity_claim=True,
        actual_cancel_availability_andoriginal_event_activation_not_claimed=True,
        new_emulator_runs=0, original_instruction_addresses_checked=len(executed))
