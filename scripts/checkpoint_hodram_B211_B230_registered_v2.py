"""Keep the newly credited batch immutable and add the next scope as a new entry."""
import inspect
from scripts import checkpoint_hodram_B211_B230_registered_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=inspect.getsource(previous.main)
start=source.index("    pins=Path('translations/rom_retention_pins.json')")
end=source.index('    summary=',start)
source=source[:start]+"""    pins=Path('translations/rom_retention_pins.json');values=load(pins)
    backup=CANDIDATE.parent/'retention_pins_before_registered_checkpoint.json'
    assert backup.exists()
    for rom in (CANDIDATE,INVERSE_PATCH):
        assert digest(rom)==release['candidate_sha256']
        assert any(Path(v['path']).resolve()==rom.resolve() for v in values)
"""+source[end:]
source=checked_text(source,{
    "additional_updates={'Hodram_B211_B230_clean_next_20261104':dict(registered_integration_pending=False,\n            stored_reconstruction_andregistered_release_pending=False,prose_comparison_anddisplay_pending=False),\n            'Hodram_B231_B250_clean_next_20261107':":
        "new_entries={'Hodram_B231_B250_clean_next_20261107':",
    "mutation=CANDIDATE.parent/'registered_documentation_v1'":"mutation=CANDIDATE.parent/'registered_documentation_v2'",
})
env={**vars(previous),'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-checkpoint-no-credited-batch-mutation','exec'),env)
if __name__=='__main__':env['main']()
