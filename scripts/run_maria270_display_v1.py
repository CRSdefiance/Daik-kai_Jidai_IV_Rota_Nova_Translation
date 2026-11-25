"""Use the qualified read-only observer and existing disclosed Maria system unlock."""
from scripts.run_maria301_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'Maria301 initialized native-command display QA.':'Maria270 initialized native-command display QA.'})
if __name__=='__main__':
    exec(compile(source,__file__+'::unchanged-native-observer-andordinary-input-harness','exec'),globals())
