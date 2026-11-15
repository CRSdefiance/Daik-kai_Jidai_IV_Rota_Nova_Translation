"""Reuse Maria's complete QA host with the qualified ordinary 16-frame A pulse.

The v1 derivation stopped before output: its optional Maria301 prose key was
absent. Preserve that producer and change only the actual input schedule here.
"""
from scripts.prepare_maria301_exit_fixture_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "duration=5, buttons=['A']":"duration=16, buttons=['A']",
})
exec(compile(source,__file__+'::same-complete-Maria-host-andqualified-normal-A-schedule','exec'),globals())
