"""Stage the source-reviewed Trade category names on the registered Trade build."""

from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch import trade_category_names_20261119 as patch
from scripts import register_square_label_wording_20261119 as square
from scripts import register_trade_labels_20261119 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.stage_square_label_wording_20261119 import former_scratch_references

base,native = parent.base,parent.native
ARM,COMMON,CLEAN,PENDING = parent.stage.ARM,parent.stage.COMMON,parent.stage.CLEAN,parent.stage.PENDING
ROOT = Path("work/trade_categories_20261119/staged_v1")
ROM,PROOF = ROOT/"Trade_Categories_STAGED.nds",ROOT/"staged.json"
NATIVE = ROOT/"native_categories.json"
REVISED = {1,2,8,11,13,17}
LABELS = (
    ("Food","Food remains clear for food staples and common produce."),
    ("Seasonings","Use the full name already shown in Square for sugar, salt, honey and cooking oil. The shop and the inventory describe the same category."),
    ("Delicacy","Keep the established category term for prized food such as caviar and smoked salmon, with its last letters visible."),
    ("Spices","The stock includes pepper, clove and other spices. This label distinguishes them from the broader seasonings."),
    ("Treats","The established name covers discretionary goods that include tea, coffee, cocoa and tobacco."),
    ("Liquor","Keep the familiar collective category for the alcoholic drinks in this game's stock."),
    ("Metals","This compact heading identifies Gold, Silver and Platinum in the stock list. The form fits alongside the percentage at its native maximum."),
    ("Crafts","The category groups manufactured decorative items such as glass and lacquerware."),
    ("Textiles","The stock includes both raw fibers and finished cloth. Textiles also matches the Square's Textile Shop and fits the shared market-rumor sentence."),
    ("Luxury","The category covers luxury goods, including carpets, antiques and artwork."),
    ("Scents","The stock groups aromatics such as musk, frankincense and ambergris."),
    ("Jewelry","Use the same name as Jewelry Shop for the category of ornamental materials. The Gems category remains distinct."),
    ("Gems","The one-word category identifies gemstones and pearls in the trade catalogue."),
    ("Medicine","Use the full category name shown in Square for ingredients such as ginseng and quinine."),
    ("Dyes","The established name captures the shared use of these coloring ingredients."),
    ("Arms","The term covers the game's weapons and related equipment, including armor."),
    ("Ore","Keep the established mining category for ore and other mineral commodities."),
    ("Sundries","Use the existing shop term for the miscellaneous grouping of timber, leather, wax and related stock."),
)


def stage_arm(image,arm,previous):
    source = MainCodeFile(arm,patch.BASE).sections
    for start,stop in ((patch.HELPER,patch.END),(patch.OLD_FORMAT,patch.CAPTURE)):
        verify = FunctionType(former_scratch_references.__code__,former_scratch_references.__globals__|
            {"STUB":start,"LIMIT":stop})
        assert verify(image,source)==([],[])
    installed,helper = patch.propose(arm)
    result = MainCodeFile(installed,patch.BASE).sections
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in source]==[(s.ramAddress,len(s.data),s.bssSize) for s in result]
    assert result[3].data==source[3].data and result[5].data==source[5].data
    verify = FunctionType(former_scratch_references.__code__,former_scratch_references.__globals__|
        {"STUB":patch.HELPER,"LIMIT":patch.END})
    assert verify(image,result)==([],[(pc,patch.HELPER) for pc in patch.CALLS])
    verify_runtime(installed,previous)
    return installed,helper


def main():
    assert not ROOT.exists()
    previous,ledger = map(base.load,(parent.RELEASE,base.LEDGER))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY)==previous["registry_sha256"] and base.digest(CLEAN)==previous["clean_input_sha256"]
    assert len(base.load(square.REVIEW)["records"])==len(LABELS)==18
    image = base.NdsImage.open(parent.ROM)
    arm = image.read_file(ARM)
    assert native.digest(arm)==previous["target_ARM9_sha256"]
    installed,helper = stage_arm(image,arm,previous)
    image.replace_file(ARM,installed)
    data = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),parent_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"],target_ARM9_sha256=native.digest(installed),
        entire_parent_inverse=True,helper_hex=helper.hex(),private_code=[patch.HELPER,patch.END],
        reused_inactive_string=[patch.OLD_FORMAT,patch.CAPTURE],trade_source_calls=list(patch.CALLS),
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,square.REVIEW,Path(patch.__file__),Path(__file__))}))
    print("Staged the six Trade category names in the existing label and atlas system.")


if __name__=="__main__":
    main()
