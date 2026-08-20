-- DeSmuME 0.9.13 read-only execution trace for the progressive dialogue
-- renderer's newline/resume contract.
--
-- Required fixture:
--   out/dialogue_live_safe_v3.nds
--   dialogue_live_save_v3.dst
--
-- Load the state first, then start this script. Advance through the early
-- Prince Henry line and stop the script after the next line begins.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\dialogue_resume_trace.log]]
local MAX_EVENTS = 800

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")

local event_count = 0
local sequence = 0

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

local function preview(address)
    local out = {}
    for i = 0, 7 do
        table.insert(out, string.format("%02X", byte(address + i)))
    end
    return table.concat(out, " ")
end

local function emit(tag)
    event_count = event_count + 1
    if event_count > MAX_EVENTS then return end

    local r9 = reg("r9")
    local r10 = reg("r10")
    local lr = reg("r14")
    local r0 = reg("r0")
    local r1 = reg("r1")
    local r2 = reg("r2")
    local r3 = reg("r3")
    log:write(string.format(
        "E%04d seq=%03d %-9s lr=%08X r0=%08X r1=%08X r2=%08X r3=%08X r9=%08X [%s] r10=%08X\n",
        event_count, sequence, tag, lr, r0, r1, r2, r3, r9, preview(r9), r10
    ))
end

local function entry()
    sequence = sequence + 1
    emit("ENTRY")
end

-- 0x020D5404: progressive draw function entry. r1/r9 points at the current
-- source position depending on the call stage; LR identifies the caller.
memory.registerexec(0x020D5404, entry)

-- 0x020D54F4: compare current source byte with LF.
memory.registerexec(0x020D54F4, function() emit("LF_CMP") end)

-- 0x020D550C: native source advance after the LF helper. This must remain
-- unpatched; the trace records the pointer before its one-byte advance.
memory.registerexec(0x020D550C, function() emit("LF_ADV") end)

-- 0x020D5808: common function exit path; r9 is the source pointer returned.
memory.registerexec(0x020D5808, function() emit("EXIT") end)

-- 0x020D5818: immediately before the epilogue returns r9 in r0.
memory.registerexec(0x020D5818, function() emit("RETURN") end)

print("RESUME TRACE READY")
print("Advance through the Prince Henry line and stop after the following line begins.")

emu.registerexit(function()
    log:write(string.format("exit events=%d sequences=%d\n", event_count, sequence))
    log:close()
end)

while true do
    gui.text(2, 2, "Resume trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
