"""Cold-boot a saved ROM through the official libretro core, without a GUI."""

import argparse
import ctypes as ct
import hashlib
import json
import time
from pathlib import Path

from PIL import Image

ROOT = Path("work/emulation_v193")
CORE = ROOT / "desmume_libretro.dll"
DEFAULT_ROM = Path("out/all_routes_combined_v189_candidate.nds")
ENV = ct.CFUNCTYPE(ct.c_bool, ct.c_uint, ct.c_void_p)
VIDEO = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_uint, ct.c_uint, ct.c_size_t)
SAMPLE = ct.CFUNCTYPE(None, ct.c_int16, ct.c_int16)
BATCH = ct.CFUNCTYPE(ct.c_size_t, ct.c_void_p, ct.c_size_t)
POLL = ct.CFUNCTYPE(None)
INPUT = ct.CFUNCTYPE(ct.c_int16, ct.c_uint, ct.c_uint, ct.c_uint, ct.c_uint)
LOG = ct.CFUNCTYPE(None, ct.c_int, ct.c_char_p)


class Variable(ct.Structure):
    _fields_ = [("key", ct.c_char_p), ("value", ct.c_char_p)]


class GameInfo(ct.Structure):
    _fields_ = [("path", ct.c_char_p), ("data", ct.c_void_p), ("size", ct.c_size_t), ("meta", ct.c_char_p)]


class SystemInfo(ct.Structure):
    _fields_ = [("name", ct.c_char_p), ("version", ct.c_char_p), ("extensions", ct.c_char_p), ("fullpath", ct.c_bool), ("block_extract", ct.c_bool)]


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Frontend:
    def __init__(self, out, touchscreen=False):
        self.out = out
        self.frame = 0
        self.pixel_format = 0
        self.pressed = set()
        self.touch = None
        self.touchscreen = touchscreen
        self.last = None
        self.video_calls = 0
        self.environment_calls = {}
        self.options = {}
        self.keepalive = []
        self.events = []
        self.errors = []
        self.log_patterns = []
        for name in ("system", "saves"):
            folder = out / name
            folder.mkdir(parents=True, exist_ok=True)
            value = str(folder.resolve()).encode("utf-8")
            self.keepalive.append(value)
            setattr(self, name + "_bytes", value)
        self.overrides = {
            "desmume_cpu_mode": "interpreter",
            "desmume_num_cores": "1",
            "desmume_internal_resolution": "256x192",
            "desmume_use_external_bios": "disabled",
            "desmume_boot_into_bios": "disabled",
            "desmume_firmware_language": "English",
            "desmume_gfx_multisampling": "disabled",
            "desmume_gfx_texture_scaling": "1",
            "desmume_screens_layout": "top/bottom",
            "desmume_screens_gap": "0",
            "desmume_frameskip": "0",
        }
        if touchscreen:
            self.overrides["desmume_pointer_type"] = "touch"
        self.environment_callback = ENV(self.environment)
        self.video_callback = VIDEO(self.video)
        self.sample_callback = SAMPLE(lambda left, right: None)
        self.batch_callback = BATCH(lambda data, count: count)
        self.poll_callback = POLL(lambda: None)
        self.input_callback = INPUT(self.input)
        # The core's retro_init calls its logger even when GET_LOG_INTERFACE is
        # unavailable. Extra variadic C arguments are ignored; formats are stored
        # explicitly as unformatted patterns rather than invented messages.
        self.log_callback = LOG(self.log)

    def log(self, level, pattern):
        if pattern and len(self.log_patterns) < 300:
            self.log_patterns.append({"level": level, "unformatted_pattern": pattern.decode("utf-8", errors="replace")})

    def environment(self, command, data):
        self.environment_calls[command] = self.environment_calls.get(command, 0) + 1
        try:
            if command == 3:
                ct.cast(data, ct.POINTER(ct.c_bool))[0] = True
                return True
            if command in (9, 31, 30):
                value = self.system_bytes if command == 9 else self.saves_bytes
                ct.cast(data, ct.POINTER(ct.c_char_p))[0] = value
                return True
            if command == 10:
                self.pixel_format = ct.cast(data, ct.POINTER(ct.c_uint))[0]
                return self.pixel_format in (0, 1, 2)
            if command == 15:
                variable = ct.cast(data, ct.POINTER(Variable)).contents
                key = variable.key.decode("utf-8")
                if key not in self.options:
                    return False
                variable.value = self.options[key]
                return True
            if command == 16:
                variables = ct.cast(data, ct.POINTER(Variable))
                index = 0
                while variables[index].key:
                    key = variables[index].key.decode("utf-8")
                    description = variables[index].value.decode("utf-8")
                    choices = description.split(";", 1)[1].strip().split("|")
                    desired = self.overrides.get(key, choices[0])
                    value = (desired if desired in choices else choices[0]).encode("utf-8")
                    self.options[key] = value
                    self.keepalive.append(value)
                    index += 1
                return True
            if command == 17:
                ct.cast(data, ct.POINTER(ct.c_bool))[0] = False
                return True
            if command == 52:
                ct.cast(data, ct.POINTER(ct.c_uint))[0] = 0
                return True
            if command == 27:
                ct.cast(data, ct.POINTER(ct.c_void_p))[0] = ct.cast(self.log_callback, ct.c_void_p).value
                return True
            # No hardware-render context, filesystem shim or emulated memory hooks.
            return command in (11, 18, 32, 37, 44, 53)
        except (ValueError, IndexError, UnicodeError) as error:
            self.errors.append(f"environment {command}: {error}")
            return False

    def video(self, data, width, height, pitch):
        if data:
            self.last = (ct.string_at(data, height * pitch), width, height, pitch, self.pixel_format)
        self.video_calls += 1

    def input(self, port, device, index, key):
        if port == 0 and device == 1:
            return int(key in self.pressed)
        if port == 0 and device == 6 and index == 0 and self.touchscreen and self.touch is not None:
            # Pinned core converts normalized combined-layout coordinates into
            # the bottom192-row screen. Pixel centers prevent integer truncation.
            x, y = self.touch
            if key == 0:
                return ((2 * x + 1) * 65536 // 512) - 32768
            if key == 1:
                return ((2 * (192 + y) + 1) * 65536 // 768) - 32768
            if key == 2:
                return 1
        return 0

    def save_frame(self, label):
        if self.last is None:
            return None
        raw, width, height, pitch, pixel_format = self.last
        if pixel_format == 1:
            image = Image.frombytes("RGB", (width, height), raw, "raw", "BGRX", pitch)
        else:
            rgb = bytearray()
            for y in range(height):
                for x in range(width):
                    value = int.from_bytes(raw[y * pitch + x * 2 : y * pitch + x * 2 + 2], "little")
                    if pixel_format == 2:
                        red, green, blue = (value >> 11) & 31, (value >> 5) & 63, value & 31
                        rgb.extend((red * 255 // 31, green * 255 // 63, blue * 255 // 31))
                    else:
                        rgb.extend((((value >> 10) & 31) * 255 // 31, ((value >> 5) & 31) * 255 // 31, (value & 31) * 255 // 31))
            image = Image.frombytes("RGB", (width, height), bytes(rgb))
        path = self.out / f"frame_{self.frame:06d}_{label}.png"
        image.save(path)
        row = {"frame": self.frame, "path": str(path), "dimensions": [width, height], "pixel_format": pixel_format, "PNG_sha256": sha(path.read_bytes()), "framebuffer_sha256": sha(raw)}
        self.events.append(row)
        return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--out", type=Path, default=ROOT / "cold_boot")
    parser.add_argument("--frames", type=int, default=1800)
    parser.add_argument("--press-start", type=int, default=-1)
    parser.add_argument("--inputs-json", type=Path)
    parser.add_argument("--capture-every", type=int, default=300)
    parser.add_argument("--capture-at", type=int, nargs="+", default=[], help="Capture these exact frames without changing emulator inputs or timing.")
    parser.add_argument("--dump-capture-ram", action="store_true", help="Read-only RAM snapshots at explicitly requested capture-at frames.")
    parser.add_argument("--capture-native-state-at", type=int, nargs="+", default=[], help="Read-only CPU/TCM/VRAM exports at these exact capture frames; never loads a state.")
    parser.add_argument("--capture-window", type=int, nargs=2, metavar=("FIRST", "LAST"), help="Capture every frame within this inclusive interval; controls are unchanged.")
    parser.add_argument("--dump-ram", action="store_true")
    parser.add_argument("--dump-pause-ram", action="store_true", help="Read-only RAM export at interactive navigation pauses; never loads or modifies state.")
    parser.add_argument("--dump-native-state", action="store_true", help="Read-only CPU/TCM export; never loads a state.")
    parser.add_argument("--touchscreen", action="store_true", help="Enable ordinary stylus events using bottom-screen native pixel coordinates.")
    parser.add_argument("--pause-at", type=int, help="Pause for JSON navigation commands at this frame; defaults remain unattended.")
    parser.add_argument("--battery-save", type=Path, help="Copy an unmodified cartridge DSV save into a fresh isolated save folder before cold boot; never loads a savestate.")
    parser.add_argument("--allow-inventory-fixtures", action="store_true", help="Allow explicitly labeled synthetic equipment inventory at interactive pauses; original saves remain unchanged.")
    parser.add_argument("--allow-ending-fixtures", action="store_true", help="Allow labeled temporary ending-state tests; never verifies earned route completion.")
    parser.add_argument("--allow-location-fixtures", action="store_true", help="Allow labeled isolated Osaka/Naha location tests; never verifies normal travel.")
    parser.add_argument("--allow-condition-fixtures", action="store_true", help="Allow labeled isolated crew condition tests; never verifies natural condition events.")
    parser.add_argument("--allow-battle-fixtures", action="store_true", help="Allow bounded own-ship recovery/proximity in the isolated Speyer test; never verifies earned repair, travel or victory.")
    parser.add_argument("--allow-golden-route-fixtures", action="store_true", help="Allow explicit source-setter Golden Route display records; never verifies earned discovery, reporting or payment.")
    parser.add_argument("--allow-finance-fixtures", action="store_true", help="Allow explicit isolated company funds through the original money method; never verifies earned wealth.")
    parser.add_argument("--allow-regional-finance-fixtures", action="store_true", help="Allow only the declared isolated regional financial display words; no monthly or earned-progress credit.")
    parser.add_argument("--allow-crew-ability-fixtures", action="store_true", help="Allow explicit one-byte Gerhard ability prerequisite through the original attribute method; never verifies earned abilities.")
    parser.add_argument("--allow-missionary-fixtures", action="store_true", help="Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.")
    parser.add_argument("--allow-strategist-fixtures", action="store_true", help="Allow a bounded three-byte Gerhard Strategist assignment for hidden Tavern display testing.")
    parser.add_argument("--allow-ship-type-fixtures", action="store_true", help="Allow labeled one-byte ship layout selection research; never verifies normal acquisition or a complete refit.")
    parser.add_argument("--allow-gallery-fixtures", action="store_true", help="Allow labeled isolated Gallery access tests; never verifies earned unlocks.")
    parser.add_argument("--gallery-save-fixture-manifest", type=Path, help="Explicit provenance for an authorized copied Gallery save fixture.")
    parser.add_argument('--capture-gpu-state-at', type=int, nargs='*', default=[],
                        help='Read-only GPU matrix/geometry export at exact frames; never loads a state.')
    args = parser.parse_args()
    if args.capture_window is not None and not (1 <= args.capture_window[0] <= args.capture_window[1] <= args.frames):
        parser.error("capture-window must be an ordered interval within frames")
    if args.capture_every <= 0:
        parser.error("capture-every must be positive")
    if any(not 1 <= frame <= args.frames for frame in args.capture_at):
        parser.error("capture-at frames must be within the run")
    capture_native_at = set(args.capture_native_state_at)
    capture_gpu_at = set(args.capture_gpu_state_at)
    capture_gpu_snapshots = []
    if any(frame < 1 or frame > args.frames for frame in capture_gpu_at):
        raise ValueError('GPU-state capture frames must lie inside the requested run')
    if any(frame < 1 or frame > args.frames for frame in capture_native_at):
        raise ValueError("Native-state capture frames must lie inside the requested run")
    capture_at = set(args.capture_at) | capture_native_at | capture_gpu_at
    if args.dump_capture_ram and not capture_at:
        parser.error('dump-capture-ram requires explicit capture-at frames')
    args.out.mkdir(parents=True, exist_ok=True)
    downloaded = json.loads((ROOT / "core_download.json").read_text())
    assert sha(CORE.read_bytes()) == downloaded["DLL_sha256"]
    assert sha(DEFAULT_ROM.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    frontend = Frontend(args.out, touchscreen=args.touchscreen)
    battery = None
    if args.battery_save is not None:
        source = args.battery_save.read_bytes()
        if not source.endswith(b"|-DESMUME SAVE-|") or not 122 <= len(source) <= 16 * 1024 * 1024:
            raise ValueError("Expected a bounded DeSmuME cartridge battery save")
        destination = args.out / "saves" / (args.rom.stem + ".dsv")
        if destination.exists():
            raise ValueError("Use a fresh output folder; do not overwrite an existing battery save")
        destination.write_bytes(source)
        assert destination.read_bytes() == source
        battery = {"source": str(args.battery_save), "destination": str(destination),
                   "bytes": len(source), "source_sha256": sha(source),
                   "copied_byte_exact_before_cold_boot": True, "savestate_loaded": False}
    schedule = json.loads(args.inputs_json.read_text()) if args.inputs_json else []
    def validate_touch(point):
        assert args.touchscreen and isinstance(point, list) and len(point) == 2
        assert all(type(v) is int for v in point) and 0 <= point[0] < 256 and 0 <= point[1] < 192
    for event in schedule:
        if "touch" in event:
            validate_touch(event["touch"])
    buttons = {"B": 0, "Y": 1, "SELECT": 2, "START": 3, "UP": 4, "DOWN": 5, "LEFT": 6, "RIGHT": 7, "A": 8, "X": 9, "L": 10, "R": 11}
    core = ct.CDLL(str(CORE.resolve()))
    for name, kind, callback in (("retro_set_environment", ENV, frontend.environment_callback), ("retro_set_video_refresh", VIDEO, frontend.video_callback), ("retro_set_audio_sample", SAMPLE, frontend.sample_callback), ("retro_set_audio_sample_batch", BATCH, frontend.batch_callback), ("retro_set_input_poll", POLL, frontend.poll_callback), ("retro_set_input_state", INPUT, frontend.input_callback)):
        function = getattr(core, name)
        function.argtypes = [kind]
        function(callback)
    core.retro_api_version.restype = ct.c_uint
    assert core.retro_api_version() == 1
    core.retro_get_system_info.argtypes = [ct.POINTER(SystemInfo)]
    info = SystemInfo()
    core.retro_get_system_info(ct.byref(info))
    print("Core:", info.name.decode(), info.version.decode(), flush=True)
    core.retro_load_game.argtypes = [ct.POINTER(GameInfo)]
    core.retro_load_game.restype = ct.c_bool
    core.retro_init()
    path_bytes = str(args.rom.resolve()).encode("utf-8")
    game = GameInfo(path_bytes, None, 0, None)
    assert core.retro_load_game(ct.byref(game)), "Core rejected ROM"
    core.retro_set_controller_port_device.argtypes = [ct.c_uint, ct.c_uint]
    core.retro_set_controller_port_device(0, 1)
    started = time.monotonic()
    ram_snapshot = None
    native_state = None
    pause_snapshots = []
    capture_snapshots = []
    capture_native_snapshots = []
    inventory_fixtures = []
    commodity_label_fixtures = []
    equipment_fixtures = []
    ending_fixtures = []
    location_fixtures = []
    condition_fixtures = []
    battle_fixtures = []
    golden_route_fixtures = []
    finance_fixtures = []
    regional_finance_fixtures = []
    crew_ability_fixtures = []
    missionary_fixtures = []
    strategist_fixtures = []
    navigation_commands = []
    ship_type_fixtures = []
    gallery_fixtures = []
    if args.gallery_save_fixture_manifest is not None:
        if not args.allow_gallery_fixtures or battery is None:
            raise ValueError('Gallery save fixture requires --allow-gallery-fixtures and --battery-save')
        fixture = json.loads(args.gallery_save_fixture_manifest.read_text(encoding='utf-8'))
        assert fixture['synthetic_gallery_fixture'] and not fixture['earned_unlock_verified']
        assert sha(args.battery_save.read_bytes()) == fixture['fixture_save_sha256']
        assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
        assert sha(args.rom.read_bytes()) == fixture['production_ROM_sha256']
        if fixture.get('only_supported_source_Gallery_images_selected'):
            from dk4tool.rom.nds import NdsImage

            arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
            table = int.from_bytes(arm[0x446C4:0x446C8], 'little') - 0x02000000
            assert table == fixture['source_image_pointer_table'] == 0x115748
            available = [i for i in range(21) if int.from_bytes(arm[table + i * 4:table + i * 4 + 4], 'little')]
            save_bytes = args.battery_save.read_bytes()
            assert save_bytes[0x3C000:0x3C004] == b'DK4R'
            bits = int.from_bytes(save_bytes[0x3C038:0x3C03B], 'little') & 0x1FFFFF
            selected = [i for i in range(21) if bits & (1 << i)]
            assert available == fixture['original_available_site_image_ids']
            assert set(selected) <= set(available), 'Supported Gallery fixture selects a null image slot'
            assert [i for i in range(21) if i not in available] == fixture['excluded_original_null_image_placeholder_ids']
            fixture['validated_selected_supported_site_ids'] = selected
        gallery_fixtures.append({'preloaded_save_manifest': str(args.gallery_save_fixture_manifest),
                                 'manifest_sha256': sha(args.gallery_save_fixture_manifest.read_bytes()),
                                 'synthetic_gallery_fixture': True, 'earned_unlock_verified': False,
                                 'validated_selected_supported_site_ids': fixture.get('validated_selected_supported_site_ids')})
    next_pause = args.pause_at
    try:
        for frame in range(1, args.frames + 1):
            frontend.frame = frame
            frontend.pressed = {3} if args.press_start <= frame < args.press_start + 5 and args.press_start >= 0 else set()
            frontend.touch = None
            for event in schedule:
                if event["start"] <= frame < event["start"] + event.get("duration", 5):
                    frontend.pressed.update(buttons[name] for name in event.get("buttons", []))
                    if "touch" in event:
                        frontend.touch = event["touch"]
            core.retro_run()
            in_window = args.capture_window is not None and args.capture_window[0] <= frame <= args.capture_window[1]
            if frame in (1, 60, 180) or frame % args.capture_every == 0 or in_window or frame in capture_at:
                frontend.save_frame("cold_boot")
                print(f"Frame {frame}; elapsed {time.monotonic() - started:.1f}s; video callbacks {frontend.video_calls}", flush=True)
                if args.dump_capture_ram and frame in capture_at:
                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    raw = ct.string_at(pointer, size)
                    snapshot_path = args.out / f"frame_{frame:06d}_arm9_ram.bin"
                    snapshot_path.write_bytes(raw)
                    capture_snapshots.append({'frame': frame, 'path': str(snapshot_path),
                                              'bytes': size, 'sha256': sha(raw), 'read_only_export': True})
                if frame in capture_native_at:
                    from scripts.inspect_desmume_state_v249 import export

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    raw = ct.string_at(pointer, size)
                    captured_native = export(core, args.out / f'capture_native_state_{frame:06d}', raw)
                    capture_native_snapshots.append({'frame': frame, **captured_native})
                if frame in capture_gpu_at:
                    from scripts.inspect_desmume_gpu_v630 import export as export_gpu

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    raw = ct.string_at(pointer, size)
                    captured_gpu = export_gpu(core, args.out / f'capture_gpu_state_{frame:06d}', raw)
                    capture_gpu_snapshots.append({'frame': frame, **captured_gpu})
            if frame == next_pause:
                frontend.save_frame("navigation")
                if args.dump_pause_ram:
                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    raw = ct.string_at(pointer, size)
                    snapshot_path = args.out / f"frame_{frame:06d}_arm9_ram.bin"
                    snapshot_path.write_bytes(raw)
                    pause_snapshots.append({"frame": frame, "path": str(snapshot_path), "bytes": size,
                                            "sha256": sha(raw), "read_only_export": True})
                print(f"Navigation paused at frame {frame}; enter JSON with until/buttons/duration, or stop=true.", flush=True)
                while True:
                    command = json.loads(input())
                    invalid = None
                    try:
                        assert isinstance(command, dict), 'Navigation must be a JSON object'
                        if not command.get('stop'):
                            until = command['until']
                            assert type(until) is int and frame < until <= args.frames, 'Invalid next frame'
                            names = command.get('buttons', [])
                            assert isinstance(names, list) and all(name in buttons for name in names), 'Invalid buttons'
                            if command.get('touch') is not None:
                                validate_touch(command['touch'])
                            duration = command.get('duration', 12)
                            assert type(duration) is int and 0 < duration <= until - frame, 'Invalid duration'
                    except (AssertionError, KeyError, TypeError, ValueError) as error:
                        invalid = str(error) or 'Invalid navigation coordinates or fields'
                    navigation_commands.append({'frame': frame, 'command': command, 'validation_passed': invalid is None,
                                                **({'rejected_before_any_input_or_fixture': invalid} if invalid else {})})
                    (args.out / 'navigation_command_journal.json').write_text(json.dumps({
                        'ROM_sha256': sha(args.rom.read_bytes()), 'commands_received': navigation_commands,
                        'last_command_frame': frame, 'commands_are_not_execution_receipts': True,
                        'completion_confirmed': False,
                    }, indent=2) + '\n', encoding='utf-8')
                    if invalid is None:
                        break
                    print(f'Rejected navigation without applying input or fixtures: {invalid}. Enter another command.', flush=True)
                if command.get('export_native_state'):
                    from scripts.inspect_desmume_state_v249 import export

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    raw = ct.string_at(pointer, size)
                    native_state = export(core, args.out / f'native_state_{frame:06d}', raw)
                if command.get("stop"):
                    break
                if 'commodity_label_fixture' in command:
                    if not args.allow_inventory_fixtures:
                        raise ValueError('Synthetic commodity label requires --allow-inventory-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_commodity_label_fixture_v635 import substitute

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = substitute(arm, before, command['commodity_label_fixture'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    commodity_label_fixtures.append(fixture)
                    print('Synthetic complete name only;original commodity identity and stock unchanged.', flush=True)
                if command.get('gallery_fixture'):
                    if not args.allow_gallery_fixtures or command['gallery_fixture'] is not True:
                        raise ValueError('Synthetic Gallery requires --allow-gallery-fixtures and true')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_gallery_fixture_v521 import enable_gallery

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = enable_gallery(arm, before)
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    gallery_fixtures.append(fixture)
                    print('Synthetic Gallery access applied; earned unlock is not verified.', flush=True)
                if 'ship_type_fixture' in command:
                    if not args.allow_ship_type_fixtures:
                        raise ValueError('Synthetic ship type requires --allow-ship-type-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_ship_type_fixture_v600 import set_ship_type

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = set_ship_type(arm, before, command['ship_type_fixture'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    ship_type_fixtures.append(fixture)
                    print('Synthetic one-byte ship layout selection applied; no acquisition or complete refit credit.', flush=True)
                if 'battle_fixture' in command:
                    if not args.allow_battle_fixtures:
                        raise ValueError('Battle recovery/proximity requires --allow-battle-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_battle_fixture_v620 import apply_fixture

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = apply_fixture(arm, before, command['battle_fixture'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    battle_fixtures.append(fixture)
                    print('Bounded isolated ship recovery/proximity applied; no earned repair, travel or victory credit.', flush=True)
                if 'condition_fixture' in command:
                    if not args.allow_condition_fixtures:
                        raise ValueError('Synthetic condition requires --allow-condition-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_condition_fixture_v520 import set_condition

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    from scripts.native_condition_fixture_v637 import (
                        ARM_SHA as current_condition_sha,
                    )

                    if sha(arm) == current_condition_sha:
                        from scripts.native_condition_fixture_v637 import set_condition
                    after, fixture = set_condition(arm, before, command['condition_fixture'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    condition_fixtures.append(fixture)
                    print('Synthetic condition applied; natural condition event is not verified.', flush=True)
                if 'location_town' in command:
                    if not args.allow_location_fixtures:
                        raise ValueError('Synthetic location requires --allow-location-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_location_fixture_v519 import relocate

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = relocate(arm, before, command['location_town'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    location_fixtures.append(fixture)
                    print('Synthetic location applied; normal travel is not verified.', flush=True)
                if 'strategist_fixture' in command or 'strategist_expert_fixture' in command:
                    if not args.allow_strategist_fixtures:
                        raise ValueError('Strategist fixture requires --allow-strategist-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_strategist_fixture_v624 import assign, assign_expert

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    assert not ('strategist_fixture' in command and 'strategist_expert_fixture' in command)
                    key = 'strategist_expert_fixture' if 'strategist_expert_fixture' in command else 'strategist_fixture'
                    assign_strategist = assign_expert if key == 'strategist_expert_fixture' else assign
                    after, fixture = assign_strategist(arm, before, command[key])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    strategist_fixtures.append(fixture)
                    print('Isolated Gerhard Strategist fixture applied; no earned refit or assignment credit.', flush=True)
                if 'missionary_fixture' in command:
                    if not args.allow_missionary_fixtures:
                        raise ValueError('Missionary display fixture requires --allow-missionary-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_missionary_fixture_v623 import assign as assign_missionary

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = assign_missionary(arm, before, command['missionary_fixture'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    missionary_fixtures.append(fixture)
                    print('Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.', flush=True)
                for ability_key, ability_actor in (('regional_admiral_command', 16), ('regional_manuel_command', 23)):
                    if ability_key not in command:
                        continue
                    if not args.allow_crew_ability_fixtures:
                        raise ValueError('Synthetic ability requires --allow-crew-ability-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_finance_fixture_v615 import enable_admiral

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = enable_admiral(arm, before, command[ability_key], actor_id=ability_actor)
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    crew_ability_fixtures.append(fixture)
                    print(f"Synthetic one-byte {fixture['original_given_name']} attribute applied; original Command150 verified,earned abilities not verified.", flush=True)
                if 'regional_finance_display' in command:
                    if not args.allow_regional_finance_fixtures:
                        raise ValueError('Regional financial display requires --allow-regional-finance-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_regional_finance_v617 import (
                        populate as populate_regional_finance,
                    )

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = populate_regional_finance(arm, before, command['regional_finance_display'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    regional_finance_fixtures.append(fixture)
                    print('Synthetic three-word regional financial display applied; monthly or earned values are not verified.', flush=True)
                if 'company_funds' in command:
                    if not args.allow_finance_fixtures:
                        raise ValueError('Synthetic funds require --allow-finance-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_finance_fixture_v615 import fund_company

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = fund_company(arm, before, command['company_funds'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    finance_fixtures.append(fixture)
                    print('Synthetic one-word company funds applied; earned wealth is not verified.', flush=True)
                if 'golden_route_records' in command:
                    if not args.allow_golden_route_fixtures:
                        raise ValueError('Synthetic Golden Route records require --allow-golden-route-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_golden_route_fixture_v613 import populate

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = populate(arm, before, command['golden_route_records'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    golden_route_fixtures.append(fixture)
                    print('Synthetic Golden Route display records applied; earned discovery/reporting/payment is not verified.', flush=True)
                if 'golden_route_purchase_cost' in command:
                    if not args.allow_golden_route_fixtures:
                        raise ValueError('Synthetic Golden Route purchase cost requires --allow-golden-route-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_golden_route_fixture_v613 import discount_salt_purchase

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = discount_salt_purchase(arm, before, command['golden_route_purchase_cost'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    golden_route_fixtures.append(fixture)
                    print('Synthetic purchase-cost word applied; original sale/discovery flow must still execute.', flush=True)
                if 'ending_captain' in command:
                    if not args.allow_ending_fixtures:
                        raise ValueError('Synthetic ending requires --allow-ending-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_ending_fixture_v537 import request_ending

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = request_ending(arm, before, command['ending_captain'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    ending_fixtures.append(fixture)
                    print('Synthetic ending state applied; earned completion is not verified.', flush=True)
                if 'equipment_items' in command:
                    if not args.allow_inventory_fixtures:
                        raise ValueError('Synthetic equipment requires --allow-inventory-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_equipment_fixture_v586 import equip

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = equip(arm, before, command['equipment_items'])
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    equipment_fixtures.append(fixture)
                    print('Synthetic equipment display fixture applied; normal acquisition/eligibility is not verified.', flush=True)
                if 'inventory_items' in command:
                    if not args.allow_inventory_fixtures:
                        raise ValueError('Synthetic inventory requires --allow-inventory-fixtures')
                    from dk4tool.rom.nds import NdsImage
                    from scripts.native_inventory_fixture_v481 import transfer

                    core.retro_get_memory_data.argtypes = [ct.c_uint]
                    core.retro_get_memory_data.restype = ct.c_void_p
                    core.retro_get_memory_size.argtypes = [ct.c_uint]
                    core.retro_get_memory_size.restype = ct.c_size_t
                    pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
                    assert pointer and size == 0x400000
                    before = ct.string_at(pointer, size)
                    arm = NdsImage.open(args.rom).read_file('/__arm9__.bin')
                    after, fixture = transfer(arm, before, command['inventory_items'])
                    # Apply only the validated inventory bytes, never executable code.
                    for change in fixture['changes']:
                        ct.c_ubyte.from_address(pointer + change['address'] - 0x02000000).value = change['after']
                    assert ct.string_at(pointer, size) == after
                    fixture['frame'] = frame
                    inventory_fixtures.append(fixture)
                    print('Synthetic inventory fixture applied; normal acquisition is not verified.', flush=True)
                next_pause = int(command["until"])
                assert frame < next_pause <= args.frames
                names = command.get("buttons", [])
                point = command.get("touch")
                if point is not None:
                    validate_touch(point)
                assert all(name in buttons for name in names)
                duration = int(command.get("duration", 12))
                assert 0 < duration <= next_pause - frame
                if names or point is not None:
                    event = {"start": frame + 1, "duration": duration, "buttons": names}
                    if point is not None:
                        event["touch"] = point
                    schedule.append(event)
        frontend.save_frame("final")
        if args.dump_ram or args.dump_native_state:
            core.retro_get_memory_data.argtypes = [ct.c_uint]
            core.retro_get_memory_data.restype = ct.c_void_p
            core.retro_get_memory_size.argtypes = [ct.c_uint]
            core.retro_get_memory_size.restype = ct.c_size_t
            pointer, size = core.retro_get_memory_data(2), core.retro_get_memory_size(2)
            assert pointer and size == 0x400000
            raw = ct.string_at(pointer, size)
            path = args.out / "final_arm9_ram.bin"
            path.write_bytes(raw)
            ram_snapshot = {"path": str(path), "bytes": size, "sha256": sha(raw), "read_only_export": True}
            if args.dump_native_state:
                from scripts.inspect_desmume_state_v249 import export

                native_state = export(core, args.out / "native_state", raw)
    finally:
        core.retro_unload_game()
        core.retro_deinit()
    report = {"core_name": info.name.decode(), "core_version": info.version.decode(), "core_DLL_sha256": downloaded["DLL_sha256"], "ROM": str(args.rom), "ROM_sha256": sha(args.rom.read_bytes()), "cold_boot": True, "savestate_loaded": False, "frames": frontend.frame, "scripted_start_frame": args.press_start, "frames_captured": frontend.events, "core_options": {key: value.decode() for key, value in frontend.options.items()}, "environment_calls": frontend.environment_calls, "callback_errors": frontend.errors, "core_log_unformatted_patterns": frontend.log_patterns, "emulator_Graphics_capture": True, "hardware_device_verification": False, "goal_complete": False}
    report["scripted_input_schedule"] = schedule
    if capture_snapshots:
        report['read_only_capture_RAM_snapshots'] = capture_snapshots
    if capture_native_snapshots:
        report['read_only_capture_native_states'] = capture_native_snapshots
        report['exact_requested_native_state_capture_frames'] = sorted(capture_native_at)
    if capture_gpu_snapshots:
        report['read_only_capture_GPU_states'] = capture_gpu_snapshots
        report['exact_requested_GPU_state_capture_frames'] = sorted(capture_gpu_at)
    if gallery_fixtures:
        report['synthetic_gallery_fixtures'] = gallery_fixtures
        report['earned_unlock_verified'] = False
    if condition_fixtures:
        report['synthetic_condition_fixtures'] = condition_fixtures
        report['natural_condition_event_verified'] = False
    if battle_fixtures:
        report['synthetic_battle_recovery_proximity_fixtures'] = battle_fixtures
        report['earned_repair_travel_or_battle_victory_verified'] = False
    if golden_route_fixtures:
        report['synthetic_golden_route_display_fixtures'] = golden_route_fixtures
        report['earned_golden_route_discovery_reporting_or_payment_verified'] = False
    if finance_fixtures:
        report['synthetic_finance_fixtures'] = finance_fixtures
        report['earned_wealth_or_ordinary_fleet_prerequisites_verified'] = False
    if regional_finance_fixtures:
        report['synthetic_regional_financial_display_fixtures'] = regional_finance_fixtures
        report['actual_monthly_or_earned_regional_finances_verified'] = False
    if strategist_fixtures:
        report['synthetic_strategist_room_assignment_fixtures'] = strategist_fixtures
        report['earned_strategist_qualifications_refit_or_assignment_verified'] = False
    if missionary_fixtures:
        report['synthetic_missionary_Chapel_assignment_fixtures'] = missionary_fixtures
        report['earned_qualifications_refit_assignment_or_goods_acquisition_verified'] = False
    if crew_ability_fixtures:
        report['synthetic_crew_ability_fixtures'] = crew_ability_fixtures
        report['earned_ability_or_ordinary_fleet_prerequisites_verified'] = False
    if ship_type_fixtures:
        report['synthetic_ship_type_fixtures'] = ship_type_fixtures
        report['normal_ship_acquisition_or_refit_verified'] = False
    if location_fixtures:
        report['synthetic_location_fixtures'] = location_fixtures
        report['normal_travel_verified'] = False
    if inventory_fixtures:
        report['synthetic_inventory_fixtures'] = inventory_fixtures
        report['normal_acquisition_verified'] = False
    if commodity_label_fixtures:
        report['synthetic_complete_commodity_label_fixtures'] = commodity_label_fixtures
        report['normal_goods_acquisition_or_original_item_identity_verified'] = False
    if equipment_fixtures:
        report['synthetic_equipment_display_fixtures'] = equipment_fixtures
        report['normal_acquisition_or_eligibility_verified'] = False
    if ending_fixtures:
        report['synthetic_ending_fixtures'] = ending_fixtures
        report['earned_completion_verified'] = False
    if args.capture_window is not None:
        report["every_frame_capture_window"] = args.capture_window
    if args.capture_at:
        report["exact_requested_capture_frames"] = sorted(capture_at)
    if battery is not None:
        report["battery_save_preloaded"] = battery
    report["read_only_RAM_snapshot"] = ram_snapshot
    if args.dump_pause_ram:
        report["read_only_pause_RAM_snapshots"] = pause_snapshots
    if native_state is not None:
        report["read_only_native_state"] = native_state
    (args.out / "capture_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Saved cold-boot frame evidence:", args.out, flush=True)


if __name__ == "__main__":
    main()
