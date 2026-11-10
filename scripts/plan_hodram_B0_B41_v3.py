"""Keep every formatter/source guard and bind the reviewed full-FO follow-up."""
from pathlib import Path
from types import FunctionType
from scripts import plan_hodram_B0_B41_v2 as previous

original=previous.main.__globals__['qualify_source']
qualifier=FunctionType(original.__code__,dict(original.__globals__,
    PROSE=Path('translations/hodram_B0_B41_contextual_review_v3.json')),
    argdefs=original.__defaults__)
main=FunctionType(previous.main.__code__,dict(previous.main.__globals__,qualify_source=qualifier),
    argdefs=previous.main.__defaults__)

if __name__=='__main__':main()
