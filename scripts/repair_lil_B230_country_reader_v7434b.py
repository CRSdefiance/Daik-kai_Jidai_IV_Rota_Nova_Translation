"""Use the established exact current-directory reader, preserving failed history."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    target=Path('scripts/bind_lil_B230_Britain_term_v7434b.py');assert not target.exists()
    derive('scripts/bind_lil_B230_Britain_term_v7434.py',str(target),{'from dk4tool.script.common_message_table import common_message_entries':'from dk4tool.script.common_message_table import common_message_entries\nfrom dk4tool.patch.duel_editorial import owned_entries',"common_message_entries(new.read_file('/COMMON/MESFILE.DK4'),b,clean=False)":"owned_entries(new.read_file('/COMMON/MESFILE.DK4'),b,'80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e')"})
