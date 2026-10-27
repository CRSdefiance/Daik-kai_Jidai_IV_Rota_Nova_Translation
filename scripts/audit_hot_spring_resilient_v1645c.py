"""Same exact fixture/input/RAM audit with live-crew preservation."""
import inspect
from scripts import audit_hot_spring_supplied_v1643c as previous
from scripts import native_hot_spring_resilient_v1644 as fixture
def audit(terminal_frame):
    source=inspect.getsource(previous.audit).replace('hot_spring_notice_supplied_v1643','hot_spring_notice_resilient_v1645')
    source=source.replace('assert supply==[20700]','assert supply and supply[0]==20700 and len(supply)==len(set(supply))')
    env={**previous.__dict__,'fixture':fixture};exec(compile(source,__file__,'exec'),env)
    return env['audit'](terminal_frame)
