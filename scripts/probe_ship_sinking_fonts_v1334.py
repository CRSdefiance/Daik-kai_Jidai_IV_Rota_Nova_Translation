"""Recheck all96 native font cases after the two v2 prose revisions."""
from pathlib import Path
from types import FunctionType
from scripts import probe_ship_sinking_fonts_v1331 as previous

if __name__=='__main__':
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/ship_sinking_fonts_v1334'),
        'PLAN':Path('work/analysis/ship_sinking_payload_v1333/native_payload_plan.json'),
        'MANUSCRIPT':Path('translations/ship_sinking_editorial_manuscript_v2.json')}
    FunctionType(previous.main.__code__,env,argdefs=previous.main.__defaults__)()
