"""Reuse the source-complete Maria host and qualified normal16-frame A input schedule."""
from scripts.prepare_maria301_exit_fixture_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "duration=5, buttons=['A']":"duration=16, buttons=['A']",
    'Maria301':'Maria270',
})
exec(compile(source,__file__+'::same-source-complete-Maria-host-native-command-copy-andnormal-input-pace','exec'),globals())
