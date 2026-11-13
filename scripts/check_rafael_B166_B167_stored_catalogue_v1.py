"""Check every newly stored B166–B167 speech through the original catalogue lookup."""
from scripts.check_rafael_B161_B165_stored_catalogue_v1 import source as previous, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "Path('work/analysis/Rafael_B161_B165_stored_catalogue_v1_20261105')":
        "Path('work/analysis/Rafael_B166_B167_current1674_20261105/stored_catalogue_v1')",
    "Path('work/analysis/Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json')":
        "Path('work/analysis/Rafael_B166_B167_current1674_20261105/stored_native_v1/stored_native_verification.json')",
    "Path('work/analysis/Rafael_B161_B165_current1607_20261105/current_effective.json')":
        "Path('work/analysis/Rafael_B166_B167_current1674_20261105/current_effective.json')",
    'len(rows)==67':'len(rows)==186',
    'all67_stored_effective_body_bindings.json':'all186_stored_effective_body_bindings.json',
    '67 stored story bodies pass':'186 stored story bodies pass',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-native-catalogue-lookup','exec'),globals())
