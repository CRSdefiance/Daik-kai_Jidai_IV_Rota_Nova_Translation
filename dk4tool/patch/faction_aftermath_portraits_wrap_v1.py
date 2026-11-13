"""Wrap the original post-dissolution fleet portraits in their native frame."""

from types import FunctionType

from dk4tool.patch import rumor_and_cooperation_wrap_v1 as previous


SOURCE = '0c53bf182b5bd04971f5512b144d21aa1b87703f3d54c990c7fbc4526a1124df'
PRIOR = 0x01FFDF80
HOOK = previous.HOOK
PARAGRAPH = previous.PARAGRAPH
DYNAMIC = {(0x02053F40, 0x274): (0x021170E0, 0x02117160, 0x021171E0)}
assembly = FunctionType(previous.assembly.__code__, vars(previous) | globals())
transform = FunctionType(previous.transform.__code__, vars(previous) | globals() | {'previous': previous.previous})

