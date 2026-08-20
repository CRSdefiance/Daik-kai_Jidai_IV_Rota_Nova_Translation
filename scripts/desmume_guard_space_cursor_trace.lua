-- Read-only DeSmuME 0.9.13 trace for protected LF+SPACE cursor behavior.
--
-- Required ROM: out/dialogue_live_safe_v3.nds
-- Required state: the known-good Raphael dialogue savestate documented in
-- docs/desmume_runtime_trace.md. Do not use a revoked probe ROM.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\guard_space_cursor_trace.log]]
local BYTE_LOOP = 0x020D54F0
local LF_CURSOR_LOAD = 0x020D5504
local LF_SOURCE_ADVANCE = 0x020D550C
local MAX_EVENTS = 500

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local events = 0

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

local function relevant(source)
    return byte(source) == 0x0A
        or (byte(source) == 0x20 and byte(source - 1) == 0x0A)
        or (byte(source - 1) == 0x20 and byte(source - 2) == 0x0A)
end

local function emit(tag)
    local source = reg("r9")
    if not relevant(source) or events >= MAX_EVENTS then return end
    events = events + 1
    local context = {}
    for offset = -2, 3 do
        context[#context + 1] = string.format("%02X", byte(source + offset))
    end
    log:write(string.format(
        "E%04d %-12s pc=%08X lr=%08X r9=%08X r10=%08X cursor=%08X bytes=[%s]\n",
        events, tag, reg("r15"), reg("r14"), source, reg("r10"),
        word(reg("r10") + 0x24), table.concat(context, " ")
    ))
end

memory.registerexec(BYTE_LOOP, function() emit("BYTE_LOOP") end)
memory.registerexec(LF_CURSOR_LOAD, function() emit("LF_CURSOR") end)
memory.registerexec(LF_SOURCE_ADVANCE, function() emit("LF_ADVANCE") end)

print("GUARD SPACE CURSOR TRACE READY")
print("Advance through the three known protected-break dialogue fixtures.")

emu.registerexit(function()
    log:write(string.format("exit events=%d\n", events))
    log:close()
end)

while true do
    gui.text(2, 2, "Guard-space cursor trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
