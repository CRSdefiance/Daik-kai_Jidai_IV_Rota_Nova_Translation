-- Read-only DeSmuME 0.9.13 boot regression trace.
-- Open V148 without a savestate, run this script, and let 300 frames pass.
-- If already at the black screen, the periodic register samples still help.
-- Never writes emulated memory, loads a state, or resets the running emulator.

local LOG_PATH = [[C:\Projects\Personal Projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\analysis\v148_desmume_boot_trace.log]]
local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local events, frame = 0, 0
local hooks = {
    {0x02000800, "HEADER_ENTRY"}, {0x020009E0, "AUTOLOAD"},
    {0x0200088C, "BSS_CLEAR"}, {0x020008E4, "AFTER_BSS"},
    {0x02005310, "CONSTRUCTORS"}, {0x02000B88, "MAIN_ENTRY"},
    {0x01FF995C, "IRQ_ENTRY"},
    {0x020E47C8, "ARENA_INIT"}, {0x020E5B1C, "ARM7_WAIT"}
}

local function reg(name)
    local ok, value = pcall(memory.getregister, name)
    if not ok then error("Register API failed: " .. name) end
    return value
end

local function word(address)
    local ok, value = pcall(memory.readdword, address)
    if not ok then error("Memory API failed") end
    return value
end

local function snapshot(tag)
    if events >= 1000 then return end
    events = events + 1
    log:write(string.format("E%04d frame=%d %s", events, frame, tag))
    for n = 0, 15 do
        log:write(string.format(" r%d=%08X", n, reg("r" .. n)))
    end
    log:write(string.format(" autoload=[%08X %08X %08X] bss=[%08X %08X] heap_literal=%08X pool_first=%08X\n",
        word(0x02000B4C), word(0x02000B50), word(0x02000B54),
        word(0x02000B58), word(0x02000B5C), word(0x020E45DC), word(0x02387A20)))
end

for _, entry in ipairs(hooks) do
    local address, label = entry[1], entry[2]
    local hits = 0
    memory.registerexec(address, function()
        hits = hits + 1
        if hits <= 10 then snapshot(label) end
    end)
end
snapshot("SCRIPT_START")
print("BOOT TRACE READY: read-only; logging 300 frames to " .. LOG_PATH)

local closed = false
local function close()
    if closed then return end
    for _, entry in ipairs(hooks) do memory.registerexec(entry[1], nil) end
    log:write(string.format("TRACE_END frames=%d events=%d\n", frame, events))
    log:close()
    closed = true
end
emu.registerexit(close)
for n = 1, 300 do
    frame = n
    if n <= 10 or n % 30 == 0 then snapshot("FRAME_SAMPLE") end
    emu.frameadvance()
end
snapshot("FINAL_SAMPLE")
close()
print("BOOT TRACE COMPLETE")
