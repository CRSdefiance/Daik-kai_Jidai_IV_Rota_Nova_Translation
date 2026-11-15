"""Reload the corrected archive; refresh handoff cases only for the changed block."""
from scripts.check_qualified_rafael_loaders_v1 import source as previous,parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "    assert changed == set(rebuilt['changed_blocks'])":"""    prior_rom=Path(latest['research_ROM']);assert sha(prior_rom.read_bytes())==latest['research_ROM_sha256']
    prior_image=NdsImage.open(prior_rom);assert prior_image.read_file('/__arm9__.bin')==arm
    prior_blocks=IlnkContainer.parse(prior_image.read_file('/data/SC0.DK4')).blocks
    assert {i for i,(a,b) in enumerate(zip(prior_blocks,blocks,strict=True)) if a!=b}==changed=={154}
    assert changed<=set(rebuilt['changed_blocks'])""",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-loaders-single-changed-block','exec'),globals())
