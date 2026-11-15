"""Apply the exact native research plan to the v3 source-reviewed manuscript."""
from pathlib import Path
from types import FunctionType
from scripts import ship_sinking_native_plan_v1330 as previous

if __name__=='__main__':
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/ship_sinking_payload_v1337'),
        'MANUSCRIPT':Path('translations/ship_sinking_editorial_manuscript_v3.json')}
    FunctionType(previous.main.__code__,env,argdefs=previous.main.__defaults__)()
