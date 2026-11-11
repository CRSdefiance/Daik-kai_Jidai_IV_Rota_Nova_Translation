"""Use the established paragraph wrapper for the original letter portrait tables."""

from types import FunctionType

from dk4tool.patch import rumor_and_cooperation_wrap_v1 as previous


SOURCE = '81bb1e01a94551f867442e38a0bf4cffe9c005c5a9b2e910304dc289839899be'
PRIOR = 0x01FFDE14
HOOK = previous.HOOK
PARAGRAPH = previous.PARAGRAPH
DYNAMIC = {
    (0x02053F40, 0x274): (
        0x02117260, 0x021172C0, 0x021173A0, 0x02117600, 0x02117720, 0x02117880, 0x02117A40,
        0x02117C00, 0x02117DA0, 0x02117FC0, 0x02118420, 0x021187E0, 0x021168E0, 0x02116960,
    ),
}
assembly = FunctionType(previous.assembly.__code__, vars(previous) | globals())
transform = FunctionType(previous.transform.__code__, vars(previous) | globals() | {'previous': previous.previous})

