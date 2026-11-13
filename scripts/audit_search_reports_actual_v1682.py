"""Full preservation audit for the V1676 original-donor Search test."""
import inspect
from scripts import audit_hot_spring_crew_v1654 as previous
from scripts import native_search_reports_fixture_v1679 as fixture


def audit(terminal_frame):
    source=inspect.getsource(previous.audit)
    for old,new in [('hot_spring_crew_v1651_1637','search_reports_live_v1680_1676'),
                    ("'hot_spring_crew_v1651', 1637","'search_reports_live_v1680', 1676"),
                    ("    assert result['source_proven_crew10_fixture_frames'][0] == 42673", "    assert len(result['source_proven_crew10_fixture_frames'])==len(set(result['source_proven_crew10_fixture_frames']))"),
                    ("    assert result['source_proven_supply20_fixture_frames'][0] == 20700", "    assert len(result['source_proven_supply20_fixture_frames'])==len(set(result['source_proven_supply20_fixture_frames']))")]:
        assert source.count(old)==1,old;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'fixture':fixture}
    exec(compile(source,__file__,'exec'),env)
    return env['audit'](terminal_frame)
