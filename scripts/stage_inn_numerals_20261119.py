"""Stage the three Inn numeral call-site corrections on the registered build."""

from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch import inn_numerals_20261119 as patch
from scripts import checkpoint_inn_number_width_20261119 as lead
from scripts import register_inn_conversations_20261119 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.stage_square_label_wording_20261119 import former_scratch_references

base,native,workflow = parent.base,parent.native,parent.stage.workflow
ARM,COMMON,CLEAN,PENDING = parent.stage.ARM,parent.stage.COMMON,parent.stage.CLEAN,parent.stage.PENDING
ROOT = Path("work/inn_numerals_20261119/staged_v1")
ROM,PROOF = ROOT/"Inn_Numerals_STAGED.nds",ROOT/"staged.json"
NATIVE_PROOF = ROOT/"native_number_and_layout_proof.json"
AFFECTED = (1180,1195,1196,1197,1198)


def recompile(image, arm, previous):
    census = FunctionType(former_scratch_references.__code__,former_scratch_references.__globals__|
        {"STUB":patch.HELPER,"LIMIT":patch.END})
    before = MainCodeFile(arm,patch.BASE).sections
    assert census(image,before)==([],[])
    installed,helper = patch.propose(arm)
    after = MainCodeFile(installed,patch.BASE).sections
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in before]==[(s.ramAddress,len(s.data),s.bssSize) for s in after]
    references = [(c,patch.HELPER) for c in patch.CALLS] + [(patch.HELPER+36,patch.HELPER+16)]
    assert census(image,after)==([],references)
    current = [r for section in before for r in lead.calls(section)]
    surviving = [r for section in after for r in lead.calls(section)]
    assert len(current)==69
    assert [x for x in surviving if x["address"]!=patch.HELPER+4]==[x for x in current if x["address"] not in patch.CALLS]
    assert sum(x["address"]==patch.HELPER+4 for x in surviving)==1
    verify_runtime(installed,previous)
    assert before[3].data==after[3].data
    return installed,helper


def main():
    assert not ROOT.exists()
    previous,record,ledger = map(base.load,(parent.RELEASE,lead.RECEIPT,base.LEDGER))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==record["candidate_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY)==previous["registry_sha256"]
    assert base.digest(CLEAN)==previous["clean_input_sha256"]
    image = base.NdsImage.open(parent.ROM)
    arm = image.read_file(ARM)
    assert native.digest(arm)==record["arm9_sha256"]==previous["target_ARM9_sha256"]
    installed,helper = recompile(image,arm,previous)
    image.replace_file(ARM,installed)
    data = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),parent_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"],target_ARM9_sha256=native.digest(installed),
        target_COMMON_sha256=previous["target_COMMON_sha256"],entire_parent_inverse=True,
        original_calls=list(patch.CALLS),helper_range=[patch.HELPER,patch.HELPER+len(helper)],helper_hex=helper.hex(),
        other_aligned_main_formatter_calls_preserved=66,affected_common_ids=list(AFFECTED),
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,parent.REVIEW,lead.RECEIPT,Path(patch.__file__),Path(__file__))}))
    print("Staged three Inn number calls in a verified 44-byte released ITCM span.")


if __name__=="__main__":
    main()
