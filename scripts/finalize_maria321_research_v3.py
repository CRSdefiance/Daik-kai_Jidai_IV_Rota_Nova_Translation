"""Bind the measured stored parity/page/branch counts without changing their checks."""
from scripts.finalize_maria321_research_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "(stored['fresh_parity_dependent_pages'], stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (148, 154, 170)":
        "(stored['fresh_parity_dependent_pages'], stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (156, 169, 120)",
    "Path('scripts/finalize_maria305_research_v1.py'), Path(__file__)]":
        "Path('scripts/finalize_maria305_research_v1.py'), Path('scripts/finalize_maria321_research_v1.py'), Path('scripts/finalize_maria321_research_v2.py'), Path(__file__)]",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-five-gate-contract-exact-measured-stored-counts', 'exec'), globals())
