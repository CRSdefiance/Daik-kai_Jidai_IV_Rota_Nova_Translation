"""Require the explicitly requested protagonist while retaining all own-snapshot guards."""
import inspect
from scripts import registered_editorial_runtime as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.RegisteredRuntime),{
    'def __init__(self, release, startup):':
        'def __init__(self, release, startup, *, captain):\n        assert captain in range(4)\n        self.expected_captain = captain',
    "self.startup['actual_captain_getter'] == 1":"self.startup['actual_captain_getter'] == self.expected_captain",
    'get(0x7F244) == 1':'get(0x7F244) == self.expected_captain',
    'captain=1':'captain=self.expected_captain',
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-own-ROM-snapshot-explicit-protagonist','exec'),env)
RegisteredRuntime=env['RegisteredRuntime']
