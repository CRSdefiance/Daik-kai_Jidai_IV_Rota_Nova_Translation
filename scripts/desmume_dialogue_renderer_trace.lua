-- DeSmuME 0.9.13 live tracer for the standard dialogue reader/renderer.
--
-- Intended ROM/state pair:
--   out/dialogue_live_safe_v3.nds
--   dialogue_live_save_v3.dst
--
-- Load the state first, then run this script from DeSmuME's Lua window.
-- It never writes emulated memory. It only observes reads from the known
-- early-Raphael dialogue block and logs the ARM9 register state.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\dialogue_renderer_trace.log]]
local SEARCH_FIRST = 0x0218E000
local SEARCH_LAST  = 0x02192000
local MARKER = "Prince Henry and Duke Leon"
local TRACE_BEFORE_MARKER = 0x120
local TRACE_AFTER_MARKER = 0x3C0
local MAX_EVENTS = 3000

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")

local function emit(line)
    print(line)
    log:write(line, "\n")
end

local function byte_at(address)
    return memory.readbyte(address)
end

local function matches(address, text)
    for i = 1, #text do
        if byte_at(address + i - 1) ~= string.byte(text, i) then
            return false
        end
    end
    return true
end

local marker_address = nil
for address = SEARCH_FIRST, SEARCH_LAST - #MARKER do
    if matches(address, MARKER) then
        marker_address = address
        break
    end
end

if marker_address == nil then
    emit("ERROR: marker text was not found in ARM9 RAM.")
    emit("Load dialogue_live_safe_v3.nds and dialogue_live_save_v3.dst, then restart this script.")
    log:close()
    error("dialogue marker not found")
end

local trace_first = marker_address - TRACE_BEFORE_MARKER
local trace_last = marker_address + TRACE_AFTER_MARKER
local trace_size = trace_last - trace_first + 1

-- Cache the bytes before installing hooks. Reading hooked addresses from the
-- callback would recursively invoke the callback.
local cached = {}
local after_newline = {}
for address = trace_first, trace_last do
    cached[address] = byte_at(address)
    if address > trace_first and cached[address - 1] == 0x0A then
        after_newline[address] = true
    end
end

local event_count = 0
local suppressed_count = 0
local pc_counts = {}

local function printable(value)
    if value >= 0x20 and value <= 0x7E then
        return string.char(value)
    end
    return "."
end

local function register_value(name)
    local ok, value = pcall(memory.getregister, name)
    if ok then return value end
    return 0
end

local function trace_read(access_address, access_size)
    event_count = event_count + 1
    if event_count > MAX_EVENTS then
        suppressed_count = suppressed_count + 1
        return
    end

    local raw_pc = register_value("r15")
    local cpsr = register_value("cpsr")
    local thumb = math.floor(cpsr / 0x20) % 2 == 1
    local instruction_address = raw_pc - (thumb and 4 or 8)
    pc_counts[instruction_address] = (pc_counts[instruction_address] or 0) + 1

    local value = cached[access_address] or 0
    local is_control = value < 0x20 or value == 0xFF
    local is_line_start = after_newline[access_address] == true

    -- Log the beginning of the stream, all control-byte reads, and every read
    -- of the first byte after a newline. These are the events needed to find
    -- the dropped-glyph/indentation branch without producing an enormous log.
    if event_count <= 120 or is_control or is_line_start then
        emit(string.format(
            "E%04d read=%08X size=%d byte=%02X '%s' pc=%08X rawpc=%08X lr=%08X cpsr=%08X r0=%08X r1=%08X r2=%08X r3=%08X r4=%08X r5=%08X",
            event_count,
            access_address,
            access_size,
            value,
            printable(value),
            instruction_address,
            raw_pc,
            register_value("r14"),
            cpsr,
            register_value("r0"),
            register_value("r1"),
            register_value("r2"),
            register_value("r3"),
            register_value("r4"),
            register_value("r5")
        ))
    end
end

memory.registerread(trace_first, trace_size, trace_read)

emit(string.format("marker=%08X trace=%08X-%08X bytes=%d", marker_address, trace_first, trace_last, trace_size))
emit("TRACE READY: advance dialogue through the 'Prince Henry' and 'Behold, the Carteira' lines.")
emit("When both have appeared, pause emulation and stop this Lua script.")

emu.registerexit(function()
    emit(string.format("exit events=%d suppressed=%d", event_count, suppressed_count))
    local entries = {}
    for pc, count in pairs(pc_counts) do
        table.insert(entries, {pc = pc, count = count})
    end
    table.sort(entries, function(a, b) return a.count > b.count end)
    emit("instruction summary:")
    for i = 1, math.min(20, #entries) do
        emit(string.format("  pc=%08X reads=%d", entries[i].pc, entries[i].count))
    end
    log:close()
end)

while true do
    gui.text(2, 2, "Dialogue trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
