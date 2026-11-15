"""Use the prior approval's actual evidence-map binding; preserve the first partial projection."""
from scripts import check_maria330_names_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "ROOT/'name_inputs_v1/review.json'":"ROOT/'name_inputs_v2/review.json'",
    "ROOT/'name_inputs_v1/bindings.json'":"ROOT/'name_inputs_v2/bindings.json'",
    "ROOT/'name_planes_v1'":"ROOT/'name_planes_v2'",
    "ROOT/'name_planes_v1/native_name_planes.json'":"ROOT/'name_planes_v2/native_name_planes.json'",
    "approval['names_sha256']==digest(PRIOR)":"approval['evidence'][str(PRIOR)]==digest(PRIOR)",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-name-checks-exact-prior-visual-evidence-map-binding','exec'),globals())
