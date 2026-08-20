-- DeSmuME 0.9.13 read-only trace for the revoked SC0 block-44 relocation.
--
-- Cold-start the revoked proof, reach its first expanded dialogue box, then start
-- this script. Press A once and stop the script after the game reaches town.
-- Attach work/sc0_b44_control_flow_trace.log to the project.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\sc0_b44_control_flow_trace.log]]
local BLOCK_BASE = 0x0218F2B0
local BLOCK_END = BLOCK_BASE + 0x1A00

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local frame = 0
local last = {}

local function dword(address)
    local ok, value = pcall(memory.readdword, address)
    if ok then return value end
    return 0
end

local function byte(address)
    local ok, value = pcall(memory.readbyte, address)
    if ok then return value end
    return 0
end

local function reg(name)
    local ok, value = pcall(memory.getregister, name)
    if ok then return value end
    return 0
end

local function preview(address)
    local out = {}
    for i = -4, 11 do
        table.insert(out, string.format("%02X", byte(address + i)))
    end
    return table.concat(out, " ")
end

local function in_block(value)
    return value >= BLOCK_BASE and value < BLOCK_END
end

local function scan_range(first, last_address)
    for address = first, last_address, 4 do
        local value = dword(address)
        if in_block(value) then
            if last[address] ~= value then
                log:write(string.format(
                    "frame=%06d PTR stored=%08X value=%08X offset=%04X bytes=[%s]\n",
                    frame, address, value, value - BLOCK_BASE, preview(value)
                ))
            end
            last[address] = value
        elseif last[address] ~= nil then
            log:write(string.format(
                "frame=%06d PTR_CLEAR stored=%08X old=%08X new=%08X\n",
                frame, address, last[address], value
            ))
            last[address] = nil
        end
    end
end

memory.registerexec(0x020D5404, function()
    local r1 = reg("r1")
    local r9 = reg("r9")
    if in_block(r1) or in_block(r9) then
        log:write(string.format(
            "frame=%06d RENDER lr=%08X r1=%08X r9=%08X r1bytes=[%s] r9bytes=[%s]\n",
            frame, reg("r14"), r1, r9, preview(r1), preview(r9)
        ))
    end
end)

log:write(string.format(
    "header=%02X %02X %02X %02X %02X %02X %02X %02X\n",
    byte(BLOCK_BASE), byte(BLOCK_BASE + 1), byte(BLOCK_BASE + 2),
    byte(BLOCK_BASE + 3), byte(BLOCK_BASE + 4), byte(BLOCK_BASE + 5),
    byte(BLOCK_BASE + 6), byte(BLOCK_BASE + 7)
))
print("SC0 B44 CONTROL-FLOW TRACE READY")
print("Press A once, stop after town appears, then attach the log.")

emu.registerexit(function()
    log:write(string.format("exit frame=%d\n", frame))
    log:close()
end)

while true do
    frame = frame + 1
    -- Known-good state structures held pointers here during this same scene.
    scan_range(0x0218ED80, 0x0218EDF0)
    scan_range(0x0218F180, 0x0218F2AC)
    gui.text(2, 2, "SC0 B44 trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
