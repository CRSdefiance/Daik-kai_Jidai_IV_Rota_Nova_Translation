"""Repack the four refined drafts with the same frozen source/ownership plan."""
from pathlib import Path
from types import FunctionType
from scripts import battle_aftermath_native_plan_v1255 as previous


if __name__ == '__main__':
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_payload_v1259'),
        'MANUSCRIPT':Path('translations/battle_aftermath_editorial_manuscript_v2.json')}
    FunctionType(previous.main.__code__,env)()
