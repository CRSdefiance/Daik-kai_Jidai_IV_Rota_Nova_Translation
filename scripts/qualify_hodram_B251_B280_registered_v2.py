"""Use the correct new-scope diagnostic while preserving the first rejected harness run."""
from scripts import qualify_hodram_B251_B280_registered_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{'all four distinct FE panels':'all 31 FE bodies'})
env={**previous.env,'OUT':previous.ROOT/'registered_semantic_checks_v2','__file__':__file__}
exec(compile(source,__file__+'::same-eight-rejections-correct-scope-diagnostic','exec'),env)
if __name__=='__main__':env['main']()
