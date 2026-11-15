"""Reuse page-aware layout preferences with this batch's exact clean source bindings."""
from types import FunctionType
from scripts import replan_hodram_B151_B170_page_padding as previous
from scripts.plan_hodram_B171_B190 import qualify_source

main = FunctionType(previous.main.__code__, {**previous.main.__globals__, 'qualify_source': qualify_source,
    '__file__': __file__}, argdefs=previous.main.__defaults__)


if __name__ == '__main__':
    main()
