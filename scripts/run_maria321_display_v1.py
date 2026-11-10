"""Use the qualified read-only observer and disclosed Maria system-only unlock."""
from scripts.run_maria390_display_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Maria390 initialized native-command display QA.':
        'Maria321 B196-B215 initialized native-command display QA.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::unchanged-observer-normal-inputs-andexisting-system-only-unlock', 'exec'), globals())
