"""Bridge all sealed clean-first drafts to the unchanged current-text binders."""
import inspect
from scripts import prepare_hodram_B231_B250_current_inputs_v1 as previous
from scripts.draft_hodram_B251_B280_clean_v1 import ROOT,OUT as DRAFTS
from scripts.gloss_hodram_B251_B280_clean_v1 import PACKET as ELIGIBLE
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'binding_inputs_v1'
source=checked_text(inspect.getsource(previous.main),{'225':'216','209':'193','14 style and two caption':'16 style and seven caption'})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-sealed-input-bridge-exact-new-scope','exec'),env)
if __name__=='__main__':env['main']()
