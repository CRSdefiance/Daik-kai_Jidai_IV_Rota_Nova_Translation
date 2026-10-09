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
    def __init__(self, out):
        self.out = out
        self.frame = 0
        self.pixel_format = 0
        self.pressed = set()
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
    parser.add_argument("--dump-ram", action="store_true")
    parser.add_argument("--pause-at", type=int, help="Pause for JSON navigation commands at this frame; defaults remain unattended.")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    downloaded = json.loads((ROOT / "core_download.json").read_text())
    assert sha(CORE.read_bytes()) == downloaded["DLL_sha256"]
    assert sha(DEFAULT_ROM.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    frontend = Frontend(args.out)
    schedule = json.loads(args.inputs_json.read_text()) if args.inputs_json else []
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
    next_pause = args.pause_at
    try:
        for frame in range(1, args.frames + 1):
            frontend.frame = frame
            frontend.pressed = {3} if args.press_start <= frame < args.press_start + 5 and args.press_start >= 0 else set()
            for event in schedule:
                if event["start"] <= frame < event["start"] + event.get("duration", 5):
                    frontend.pressed.update(buttons[name] for name in event["buttons"])
            core.retro_run()
            if frame in (1, 60, 180) or frame % args.capture_every == 0:
                frontend.save_frame("cold_boot")
                print(f"Frame {frame}; elapsed {time.monotonic() - started:.1f}s; video callbacks {frontend.video_calls}", flush=True)
            if frame == next_pause:
                frontend.save_frame("navigation")
                print(f"Navigation paused at frame {frame}; enter JSON with until/buttons/duration, or stop=true.", flush=True)
                command = json.loads(input())
                if command.get("stop"):
                    break
                next_pause = int(command["until"])
                assert frame < next_pause <= args.frames
                names = command.get("buttons", [])
                assert all(name in buttons for name in names)
                duration = int(command.get("duration", 12))
                assert 0 < duration <= next_pause - frame
                if names:
                    schedule.append({"start": frame + 1, "duration": duration, "buttons": names})
        frontend.save_frame("final")
        if args.dump_ram:
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
    finally:
        core.retro_unload_game()
        core.retro_deinit()
    report = {"core_name": info.name.decode(), "core_version": info.version.decode(), "core_DLL_sha256": downloaded["DLL_sha256"], "ROM": str(args.rom), "ROM_sha256": sha(args.rom.read_bytes()), "cold_boot": True, "savestate_loaded": False, "frames": frontend.frame, "scripted_start_frame": args.press_start, "frames_captured": frontend.events, "core_options": {key: value.decode() for key, value in frontend.options.items()}, "environment_calls": frontend.environment_calls, "callback_errors": frontend.errors, "core_log_unformatted_patterns": frontend.log_patterns, "emulator_Graphics_capture": True, "hardware_device_verification": False, "goal_complete": False}
    report["scripted_input_schedule"] = schedule
    report["read_only_RAM_snapshot"] = ram_snapshot
    (args.out / "capture_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Saved cold-boot frame evidence:", args.out, flush=True)


if __name__ == "__main__":
    main()
