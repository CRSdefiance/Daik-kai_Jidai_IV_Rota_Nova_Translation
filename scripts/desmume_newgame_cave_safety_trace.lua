-- Historical read-only DeSmuME 0.9.13 trace that proved the proposed ARM9
-- trampoline storage was live structured data. Do not use the revoked ROM as
-- a parent or test candidate; this script remains only as audit evidence.
--
-- Required ROM:
--   out/dialogue_protected_newline_probe.nds
--
-- Do not load a savestate. Start at the title menu, run this script, select
-- New Game, wait for Choose Captain, then stop the script. This script never
-- writes emulated memory.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\newgame_cave_safety_trace.log]]
local FLAG_ADDRESS = 0x021723FC
local CAVE_START = 0x02172400
local CAVE_LENGTH = 0x64
local MAX_EVENTS = 2000

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local events = 0
local cursor_hits = 0

local function reg(name)
    local ok, value = pcall(memory.getregister, name)
    if ok then return value end
    return 0
end

local function byte(address)
    local ok, value = pcall(memory.readbyte, address)
    if ok then return value end
    return 0
end

local function word(address)
    local ok, value = pcall(memory.readdword, address)
    if ok then return value end
    return 0
end

local function hexbytes(address, count)
    local out = {}
    for i = 0, count - 1 do
        out[#out + 1] = string.format("%02X", byte(address + i))
    end
    return table.concat(out, " ")
end

local function snapshot(tag)
    events = events + 1
    if events > MAX_EVENTS then return end
    log:write(string.format(
        "E%04d %-12s pc=%08X lr=%08X r9=%08X r10=%08X r12=%08X sp=%08X flag=%02X cursor=%08X source=%02X next=%02X\n",
        events, tag, reg("r15"), reg("r14"), reg("r9"), reg("r10"),
        reg("r12"), reg("r13"), byte(FLAG_ADDRESS),
        word(reg("r10") + 0x24), byte(reg("r9")), byte(reg("r9") + 1)
    ))
    log:write("  cave=[" .. hexbytes(CAVE_START, CAVE_LENGTH) .. "]\n")
end

log:write("start flag=" .. string.format("%02X", byte(FLAG_ADDRESS)) .. "\n")
log:write("start_cave=[" .. hexbytes(CAVE_START, CAVE_LENGTH) .. "]\n")

-- This is the exact instruction replaced by the failed experiments.
memory.registerexec(0x020D5504, function()
    cursor_hits = cursor_hits + 1
    snapshot("CURSOR_PRE")
end)

-- Record the state immediately after the original load. This proves what the
-- unmodified path preserves and whether the proposed storage changed meanwhile.
memory.registerexec(0x020D5508, function()
    snapshot("CURSOR_POST")
end)

-- Track the story call independently. It should remain absent during New Game.
memory.registerexec(0x02054924, function()
    snapshot("STORY_CALL")
end)

print("NEW GAME CAVE SAFETY TRACE READY")
print("Select New Game; stop after Choose Captain appears.")

emu.registerexit(function()
    log:write(string.format("exit events=%d cursor_hits=%d flag=%02X\n",
        events, cursor_hits, byte(FLAG_ADDRESS)))
    log:write("exit_cave=[" .. hexbytes(CAVE_START, CAVE_LENGTH) .. "]\n")
    log:close()
end)

while true do
    gui.text(2, 2, "New Game cave trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
