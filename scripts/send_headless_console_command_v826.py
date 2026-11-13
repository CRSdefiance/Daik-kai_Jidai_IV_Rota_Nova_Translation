"""Recover stdin for the already-running V826 test; no game-memory access.

The original exec response was printed without its session identifier. This
bounded fallback sends only the harness's ordinary JSON navigation protocol to
that same Windows console. Do not use it for other applications or new runs.
"""

import ctypes as ct
import json
import sys
from ctypes import wintypes as wt
from pathlib import Path


def main():
    assert sys.platform == 'win32'
    folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ceremony_Lil_temple_and_dance_v826')
    assert folder.is_dir() and not (folder/'capture_report.json').exists()
    command = json.loads(sys.argv[1])
    assert isinstance(command, dict)
    assert set(command) <= {'until', 'buttons', 'duration', 'touch', 'condition_fixture', 'stop'}
    k = ct.WinDLL('kernel32', use_last_error=True)
    k.FreeConsole()
    k.AttachConsole.argtypes = [wt.DWORD]
    k.AttachConsole.restype = wt.BOOL
    assert k.AttachConsole(52924), ct.get_last_error()
    k.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, ct.c_void_p, wt.DWORD, wt.DWORD, wt.HANDLE]
    k.CreateFileW.restype = wt.HANDLE
    handle = k.CreateFileW('CONIN$', 0xC0000000, 3, None, 3, 0, None)
    assert handle not in (None, ct.c_void_p(-1).value), ct.get_last_error()

    class Key(ct.Structure):
        _fields_ = [('down', wt.BOOL), ('repeat', wt.WORD), ('vk', wt.WORD),
                    ('scan', wt.WORD), ('char', wt.WCHAR), ('state', wt.DWORD)]

    class Data(ct.Union):
        _fields_ = [('key', Key), ('padding', ct.c_byte*16)]

    class Record(ct.Structure):
        _fields_ = [('type', wt.WORD), ('data', Data)]

    text = json.dumps(command, separators=(',', ':'))+'\r'
    records = (Record*len(text))()
    for record, char in zip(records, text):
        record.type = 1
        record.data.key = Key(1, 1, 13 if char == '\r' else 0, 0, char, 0)
    count = wt.DWORD()
    k.WriteConsoleInputW.argtypes = [wt.HANDLE, ct.POINTER(Record), wt.DWORD, ct.POINTER(wt.DWORD)]
    k.WriteConsoleInputW.restype = wt.BOOL
    assert k.WriteConsoleInputW(handle, records, len(records), ct.byref(count)), ct.get_last_error()
    assert count.value == len(records)
    k.CloseHandle(handle)
    print('Sent to existing V826 console:', json.dumps(command), flush=True)


if __name__ == '__main__':
    main()
