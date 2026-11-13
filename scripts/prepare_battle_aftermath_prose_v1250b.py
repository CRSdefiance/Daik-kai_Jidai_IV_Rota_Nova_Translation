"""Successor retains2027's original measured period,as its review intended.

The initial producer stopped before output because that punctuation change
contradicted the intended retained-wording count. All75 decisions are checked
against exact current prose again;no completed or source credit was duplicated.
"""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from scripts import prepare_battle_aftermath_prose_v1250 as previous


if __name__=='__main__':
    review=deepcopy(previous.REVIEW)
    english,meaning,note=review[2027]
    assert english=='Resistance is useless! Surrender!'
    review[2027]=('Resistance is useless. Surrender!',meaning,
        note+' Preserve the measured first sentence and emphatic final order exactly.')
    env={**previous.__dict__,'__file__':__file__,'REVIEW':review,
        'ROOT':Path('work/analysis/battle_aftermath_prose_v1250b')}
    FunctionType(previous.main.__code__,env)()
