"""Use the qualified read-only Maria observer without an obsolete batch label."""
from scripts.run_maria390_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'Maria390 initialized native-command display QA.':'Initialized Maria reviewed-command display QA.'})
if __name__=='__main__':exec(compile(source,__file__+'::same-readonly-observer-normal-inputs-and-disclosed-system-unlock','exec'),globals())
