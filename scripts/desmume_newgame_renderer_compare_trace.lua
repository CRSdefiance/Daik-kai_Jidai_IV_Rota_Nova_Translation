-- DeSmuME 0.9.13 read-only trace for calls to the shared progressive renderer
-- during a cold-boot New Game transition.
--
-- Historical required ROM (now revoked; retained only for trace provenance):
--   out/dialogue_protected_newline_probe.nds
--
-- Do not load a savestate. Start this script at the title menu, select New
-- Game, wait for Choose Captain, then stop the script. The script never writes
-- emulated memory.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\newgame_renderer_compare_trace.log]]
local MAX_EVENTS = 600

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local events = 0
local calls = 0

local function reg(name)
    local ok, value = pcall(memory.getregister, name)
    if ok then return value end
    return 0
end

local function byte(address)
    if address < 0x02000000 or address >= 0x02400000 then return 0 end
    local ok, value = pcall(memory.readbyte, address)
    if ok then return value end
    return 0
end

local function word(address)
    if address < 0x02000000 or address >= 0x02400000 then return 0 end
    local ok, value = pcall(memory.readdword, address)
    if ok then return value end
    return 0
end

local function bytes(address, count)
    local out = {}
    for i = 0, count - 1 do
        table.insert(out, string.format("%02X", byte(address + i)))
    end
    return table.concat(out, " ")
end

local function ascii(address, count)
    local out = {}
    for i = 0, count - 1 do
        local value = byte(address + i)
        if value >= 0x20 and value <= 0x7E then
            table.insert(out, string.char(value))
        elseif value == 0x0A then
            table.insert(out, "<LF>")
        elseif value == 0 then
            table.insert(out, "<NUL>")
            break
        else
            table.insert(out, ".")
        end
    end
    return table.concat(out)
end

local function emit(tag)
    events = events + 1
    if events > MAX_EVENTS then return end
    local r0 = reg("r0")
    local r1 = reg("r1")
    local lr = reg("r14")
    log:write(string.format(
        "E%04d call=%03d %-8s lr=%08X r0=%08X r1=%08X r2=%08X r3=%08X r4=%08X r5=%08X r8=%08X r9=%08X r10=%08X sp=%08X\n",
        events, calls, tag, lr, r0, r1, reg("r2"), reg("r3"), reg("r4"),
        reg("r5"), reg("r8"), reg("r9"), reg("r10"), reg("r13")
    ))
    log:write(string.format("  source_hex=[%s]\n", bytes(r1, 48)))
    log:write(string.format("  source_txt=[%s]\n", ascii(r1, 48)))
    log:write(string.format(
        "  object=%08X fields=[%08X %08X %08X %08X %08X %08X %08X %08X %08X %08X %08X %08X]\n",
        r0, word(r0), word(r0 + 4), word(r0 + 8), word(r0 + 0x0C),
        word(r0 + 0x10), word(r0 + 0x14), word(r0 + 0x18), word(r0 + 0x1C),
        word(r0 + 0x20), word(r0 + 0x24), word(r0 + 0x28), word(r0 + 0x2C)
    ))
end

memory.registerexec(0x02054924, function()
    calls = calls + 1
    emit("CALLSITE")
end)

memory.registerexec(0x020D5404, function()
    if reg("r14") == 0x02054928 then emit("ENTRY") end
end)

memory.registerexec(0x020D54F4, function()
    if reg("r0") == 0x0A then emit("LF") end
end)

print("NEW GAME COMPARE TRACE READY")
print("From the title menu select New Game; stop after Choose Captain appears.")

emu.registerexit(function()
    log:write(string.format("exit events=%d calls=%d\n", events, calls))
    log:close()
end)

while true do
    gui.text(2, 2, "New Game renderer trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
