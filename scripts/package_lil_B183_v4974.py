"""Package the verified cumulative checkpoint without changing promoted main."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('releases/all_routes_unified_v4966')
if __name__=='__main__':
    assert not ROOT.exists()
    verified=Path('work/analysis/editorial_handoff_verification_v4973/verified_handoff.json');v=read(verified)
    proof=Path('work/analysis/lil_B183_release_v4967/registered_release_verification.json');r=read(proof)
    assert v['full_goal_active'] and not v['full_goal_complete'] and v['candidate_sha256']==r['candidate_sha256']
    rom,patch,manifest=map(Path,[r['candidate'],r['patch'],r['manifest']])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and sha(patch.read_bytes())==v['patch_sha256']
    assert len(read(manifest)['batches'])==565 and all(read(manifest)['checks'].values())
    link=lambda p:Path(p).resolve().as_posix()
    text=(
        '# V4966 cumulative editorial checkpoint\n\n'
        f'[ROM](<{link(rom)}>) · [Clean-input patch](<{link(patch)}>) · [Manifest](<{link(manifest)}>)\n\n'
        'This registered cumulative build adds the complete art-collectors exchange:25 contextual reviews,16 revisions and9 individually justified retentions. '
        'The collectors debate their tastes and declare purchases;polite service gives way to the shopkeeper’s private irritation,candid appraisal and request for secrecy. '
        'The Artwork/Basra forecast remains prospective. Five progressive roles and two impersonal panels retain their original controls.\n\n'
        'The fitting question “What are you two talking about?” now stays together on one line. '
        'The following “That one over there / is obviously better!” uses the native display rules. All words and the other24 encoded targets and native planes stay exact. '
        'This source-bound correction changes no font,width,metric or guard. Earlier premature wrapping remains part of the retroactive review.\n\n'
        'The entire V4914 stack is included:565 manifest batches and114 accepted layers. Only SC2 block183 changes from that parent. '
        'Every other file,font,graphic,story and executable component remains exact. This is an experimental verified editorial checkpoint;promoted main remains V4701.\n\n'
        'Verification passed:57 atomic rejection cases,78 release/dialogue regression tests,18 cumulative checks,complete native planes,source controls,bounds and pagination. '
        'The clean-input patch reconstructs the candidate byte for byte. Current New Game and inherited-battery town cold boots match V4914 across31 captured frames and five actor/captain controls.\n\n'
        'Two disclosed Japanese/English content fixtures show all25 panels and normal return. These are targeted emulator tests;natural event183 eligibility was not exercised. '
        'Five actual panel sheets and14 full screens were viewed.149 paired nontext samples and all sampled postscene images agree. '
        'The11 timing differences and unequal final random seeds remain documented. Five checked state groups and the whole actor agree;no future-world,full-memory,full-playthrough or hardware equivalence is claimed.\n\n'
        f'ROM SHA-256: `{v["candidate_sha256"]}`\n\n'
        f'Patch SHA-256: `{v["patch_sha256"]}`\n\n'
        f'Required clean-input SHA-256: `{r["clean_input_sha256"]}`\n\n'
        'Coverage:5,966 completed contextual rereads,5,969 source/prose reviews,3,780 integrated revisions and2,186 justified retentions. '
        'The full objective remains active,including earlier wrapping,remaining stories,town/shop/random scenes,Help and other player prose. '
        'Graphics work and the later older-record technical re-audit remain separate and open. All earlier ROMs and translations are preserved.\n\n'
        f'[Current handoff](<{link("docs/editorial_handoff_current.md")}>) · '
        f'[Final25-record review](<{link("translations/lil_B183_contextual_final_review_v1.json")}>) · '
        f'[Verified checkpoint](<{link(verified)}>)\n')
    ROOT.mkdir(parents=True);p=ROOT/'README.md';p.write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'package_receipt.json',dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],patch=str(patch),patch_sha256=v['patch_sha256'],
        handoff_notes=str(p),handoff_notes_sha256=sha(p.read_bytes()),release_proof=str(proof),release_proof_sha256=sha(proof.read_bytes()),
        checkpoint_proof=str(verified),checkpoint_proof_sha256=sha(verified.read_bytes()),new_ROMs=0,
        all_existing_ROMs_and_earlier_translations_preserved=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(notes=str(p),candidate_sha256=v['candidate_sha256'],completed=v['completed'],full_goal_active=True))
