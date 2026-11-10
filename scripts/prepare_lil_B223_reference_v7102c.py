"""Bind replacements to literal source keys before simultaneous substitution."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B223_reference_v7102.py')
    source=checked_text(p.read_text('utf8'),{
      "'B2231304_bytes'":"'B2141304_bytes'",
      "'all22_commands8_relative_sites_typed_alias_predicates_staging_and_shipped_census':":"'all27_commands8_relative_sites_typed_alias_predicates_staging_and_shipped_census':",
      "'All22 commands/eight relative sites/typed aliases/two predicates':":"'All27 commands/eight relative sites/typed aliases/two predicates':"})
    exec(compile(source,str(p)+'::literal-source-keys','exec'),dict(__name__='__main__',__file__=__file__))
