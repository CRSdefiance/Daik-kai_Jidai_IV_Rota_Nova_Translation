"""Keep the complete town-raid reaction together in the observed Istanbul exchange."""

from pathlib import Path
from types import FunctionType

from scripts import stage_inn_numerals_context_20261119 as earlier

base,native,workflow = earlier.base,earlier.native,earlier.workflow
parent,lead,patch,previous = earlier.parent,earlier.lead,earlier.patch,earlier.previous
ARM,COMMON,CLEAN,PENDING,AFFECTED = earlier.ARM,earlier.COMMON,earlier.CLEAN,earlier.PENDING,earlier.AFFECTED
ROOT = earlier.ROOT.parent/"staged_v3"
ROM,PROOF,NATIVE_PROOF = ROOT/earlier.ROM.name,ROOT/earlier.PROOF.name,ROOT/earlier.NATIVE_PROOF.name
REVISED = earlier.REVISED
WORDS = "%s, %s attacked %s. What a lousy thing to do!"
NOTE = "The innkeeper first reports the attack and then condemns what the attackers did. Lousy keeps the familiar voice and the direct judgment. The complete reaction stays together in the Istanbul replay, and the 121 original-format variants preserve the full thought."


def main():
    candidate,verified_earlier = map(base.load,(earlier.PROOF,earlier.NATIVE_PROOF))
    assert base.digest(earlier.ROM)==candidate["candidate_sha256"]==verified_earlier["candidate_sha256"]
    run = FunctionType(earlier.main.__code__,vars(earlier)|globals())
    run()
    proof = base.load(PROOF)
    proof["source_proofs"].update({str(p):base.digest(p) for p in (earlier.PROOF,earlier.NATIVE_PROOF,Path(earlier.__file__))})
    base.save(PROOF,proof)


if __name__=="__main__":
    main()
