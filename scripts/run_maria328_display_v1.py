"""Use the qualified read-only observer and ordinary inputs for the Maria328 fixture."""
from scripts.run_maria303_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'Maria303 initialized native-command display QA.':'Maria328 initialized native-command display QA.'})
if __name__=='__main__':exec(compile(source,__file__+'::unchanged-observer-ordinary-inputs-anddisclosed-system-unlock','exec'),globals())
