"""Spell the prefix manuscript path exactly as the canonical builder does on this host."""
from scripts.prepare_rafael516_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "contract['batches'].extend([prefix_config['manuscript'],str(final)])":
        "contract['batches'].extend([str(Path(prefix_config['manuscript'])),str(final)])",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-registered-preparation-canonical-Path-spelling','exec'),globals())
