"""Successor: the frozen runner contains two fixture-path literals, not three.

V1232 stopped before creating a run, loading a ROM or executing any inputs.
"""
import inspect
from scripts import run_duel_special_live_v1232 as previous


if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = "source.count('scripts/native_duel_bark_fixture_v1207.py') == 3"
    assert source.count(old) == 1
    source = source.replace(old, "source.count('scripts/native_duel_bark_fixture_v1207.py') == 2")
    env = {**previous.__dict__, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
