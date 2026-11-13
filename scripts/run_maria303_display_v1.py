"""Run the unchanged read-only observer and qualified ordinary Maria input schedule."""
from scripts.run_maria301_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'Maria301 initialized native-command display QA.':'Maria303 initialized native-command display QA.'})
if __name__=='__main__':exec(compile(source,__file__+'::same-readonly-observer-existing-system-unlock-andordinary-inputs','exec'),globals())
