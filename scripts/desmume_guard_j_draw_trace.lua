-- Read-only DeSmuME 0.9.13 trace for the missing J after a protected break.
-- Use only for diagnosis with out/dialogue_guard_cursor_one_pixel_probe.nds.
-- Cold-load the ROM; do not load a savestate that replaces the patched ARM9.

local LOG_PATH = [[C:\Users\chris.r.francis\.codex\.chatgpt-projects\g-p-6a676ab5787c819181af4a29d5cebfbc\dk4-translation-tool\work\guard_j_draw_trace.log]]
local LOOP_READ = 0x020D54F0
local DRAW_CALL = 0x020D5774
local PAIR_DRAW_CALL = 0x020D4FA4
local MAX_EVENTS = 80
local TARGET = {0x0A, 0x20, 0x4A, 0x61, 0x6E} -- LF, space, "Jan"

local log = assert(io.open(LOG_PATH, "w"))
log:setvbuf("no")
local events = 0
local hooked_callbacks = {}
local hooked_inner_callbacks = {}

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

local function find_target(source)
    -- r9 advances through the protected break, so accept any event whose source
    -- pointer lies from six bytes before through six bytes after the exact target.
    for delta = -6, 6 do
        local candidate = source + delta
        local matches = true
        for index = 1, #TARGET do
            if byte(candidate + index - 1) ~= TARGET[index] then
                matches = false
                break
            end
        end
        if matches then return candidate end
    end
    return nil
end

local function emit(tag, target)
    if events >= MAX_EVENTS then return end
    events = events + 1
    local source = reg("r9")
    local buffer = reg("r2")
    local cursor_pointer = reg("r1")
    log:write(string.format(
        "E%04d %-14s pc=%08X lr=%08X target=%08X r9=%08X rel=%+d src=[%02X %02X %02X %02X %02X %02X %02X %02X %02X] r0=%08X r1=%08X r2=%08X r3=%08X glyph=%02X cursor=%08X\n",
        events, tag, reg("r15"), reg("r14"), target,
        source, source - target,
        byte(source - 4), byte(source - 3), byte(source - 2), byte(source - 1),
        byte(source), byte(source + 1), byte(source + 2), byte(source + 3),
        byte(source + 4),
        reg("r0"), cursor_pointer, buffer, reg("r3"), byte(buffer),
        word(cursor_pointer)
    ))
end

local function capture(tag)
    local target = find_target(reg("r9"))
    if target then
        emit(tag, target)
    end
end

local function capture_draw()
    local target = find_target(reg("r9"))
    if not target then return end
    emit("DRAW_CALL", target)

    local callback = reg("r3")
    local glyph = byte(reg("r2"))
    if glyph == 0x4A or glyph == 0x61 then
        local object = reg("r0")
        local vtable = word(object)
        local inner = word(vtable + 0x20)
        log:write(string.format(
            "dispatch glyph=%02X object=%08X vtable=%08X inner=%08X\n",
            glyph, object, vtable, inner
        ))
        if inner ~= 0 and not hooked_inner_callbacks[inner] then
            hooked_inner_callbacks[inner] = true
            memory.registerexec(inner, function()
                local inner_target = find_target(reg("r9"))
                if not inner_target then return end
                local rectangle = reg("r2")
                local text_pointer = reg("r3")
                if byte(text_pointer) ~= 0x4A and byte(text_pointer + 1) ~= 0x4A then
                    return
                end
                events = events + 1
                log:write(string.format(
                    "E%04d INNER_ENTRY pc=%08X function=%08X rect_ptr=%08X rect=[%08X %08X %08X %08X] text_ptr=%08X text=[%02X %02X %02X]\n",
                    events, reg("r15"), inner, rectangle,
                    word(rectangle), word(rectangle + 4), word(rectangle + 8),
                    word(rectangle + 12), text_pointer, byte(text_pointer),
                    byte(text_pointer + 1), byte(text_pointer + 2)
                ))
            end)
        end
    end
    if byte(reg("r2")) == 0x4A and not hooked_callbacks[callback] then
        hooked_callbacks[callback] = true
        log:write(string.format("hook callback=%08X for protected J\n", callback))
        memory.registerexec(callback, function()
            local callback_target = find_target(reg("r9"))
            if callback_target then emit("CALLBACK_ENTRY", callback_target) end
        end)
    end
end

local function capture_pair_draw()
    local target = find_target(reg("r9"))
    if not target then return end
    local pair = reg("r3")
    if byte(pair) ~= 0x4A and byte(pair + 1) ~= 0x4A then return end
    events = events + 1
    local rectangle = reg("r2")
    local text_pointer = reg("r3")
    log:write(string.format(
        "E%04d PAIR_DRAW_CALL pc=%08X inner=%08X rect_ptr=%08X rect=[%08X %08X %08X %08X] text_ptr=%08X text=[%02X %02X %02X]\n",
        events, reg("r15"), reg("r12"), rectangle,
        word(rectangle), word(rectangle + 4), word(rectangle + 8),
        word(rectangle + 12), text_pointer, byte(text_pointer),
        byte(text_pointer + 1), byte(text_pointer + 2)
    ))
end

memory.registerexec(LOOP_READ, function() capture("LOOP_READ") end)
memory.registerexec(DRAW_CALL, capture_draw)
memory.registerexec(PAIR_DRAW_CALL, capture_pair_draw)

print("GUARD J DRAW TRACE READY")
print("Logging only the exact protected byte sequence 0A 20 4A 61 6E.")
print("Cold-play to 'She was a wreck...' and stop after the next line appears.")

emu.registerexit(function()
    log:write(string.format("exit events=%d\n", events))
    log:close()
end)

while true do
    gui.text(2, 2, "Guard J draw trace ACTIVE", "yellow", "black")
    emu.frameadvance()
end
