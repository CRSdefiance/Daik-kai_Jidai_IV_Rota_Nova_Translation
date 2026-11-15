"""Write a concise reviewable handoff for the verified cumulative V4914 build."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('releases/all_routes_unified_v4914')
if __name__=='__main__':
    assert not ROOT.exists()
    verified=Path('work/analysis/editorial_handoff_verification_v4921/verified_handoff.json');v=read(verified)
    proof=Path('work/analysis/lil_B182_release_v4915/registered_release_verification.json');r=read(proof)
    assert v['full_goal_active'] and not v['full_goal_complete'] and v['candidate_sha256']==r['candidate_sha256']
    rom,patch,manifest=map(Path,[r['candidate'],r['patch'],r['manifest']])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and sha(patch.read_bytes())==v['patch_sha256']
    assert len(read(manifest)['batches'])==564 and all(read(manifest)['checks'].values())
    link=lambda p:Path(p).resolve().as_posix()
    text=(
        '# V4914 cumulative editorial checkpoint\n\n'
        f'[ROM](<{link(rom)}>) · [Clean-input patch](<{link(patch)}>) · [Manifest](<{link(manifest)}>)\n\n'
        'This registered cumulative build adds the complete engagement-ring gossip scene: eight contextual reviews, six revisions and two individually justified retentions. '
        'It restores hearsay, the forthcoming engagement to the duke\'s son, the extravagant ring-price comparison, and the joke that neither speaker knows the gemstone. '
        'The Gems/London forecast remains prospective. The formatter owns wrapping; all wording uses the verified native display rules.\n\n'
        'The entire V4867 stack is included: 564 manifest batches and 114 accepted layers. Only SC2 block182 changes from that parent. '
        'Every other file, font, graphic, story, executable component and staged payload remains exact. This is an experimental verified editorial checkpoint; the promoted main remains V4701.\n\n'
        'Verification passed: 58 meaningful atomic rejection cases, 78 release/dialogue regression tests, 18 cumulative release checks, complete native text planes, source controls, bounds and pagination. '
        'The clean-input patch reconstructs the candidate byte for byte. Current New Game and inherited-battery town cold boots match the prior verified build across 31 captured frames and five actor/captain controls.\n\n'
        'The scene was observed in two disclosed Japanese/English content fixtures, not a naturally earned event182 activation. All eight panels, portraits, nameplates, impersonal notice and normal return were checked. '
        'The review preserves 13 command-timing differences, 18 later differences confined to the original animated A-button indicator, and differing final random seeds. '
        'The scene selects the same unforced effect in both runs; checked state groups, the whole actor model and final image agree. No full-playthrough, future-world, full-memory or hardware claim is made.\n\n'
        f'ROM SHA-256: `{v["candidate_sha256"]}`\n\n'
        f'Patch SHA-256: `{v["patch_sha256"]}`\n\n'
        f'Required clean-input SHA-256: `{r["clean_input_sha256"]}`\n\n'
        'Coverage: 5,941 completed contextual rereads, 5,944 source/prose reviews, 3,764 integrated revisions and 2,177 justified retentions. '
        'The full editorial objective remains active. Earlier wrapping findings, remaining story/town/shop/random/Help prose, separate graphics work and the later older-record technical re-audit remain open. '
        'The next art-collectors scene has a complete clean-Japanese inventory and 25 fresh glosses, with no review credit yet.\n\n'
        f'[Current handoff](<{link("docs/editorial_handoff_current.md")}>) · '
        f'[Final eight-record review](<{link("translations/lil_B182_contextual_final_review_v1.json")}>) · '
        f'[Verified checkpoint](<{link(verified)}>)\n')
    ROOT.mkdir(parents=True);p=ROOT/'README.md';p.write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'package_receipt.json',dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],patch=str(patch),patch_sha256=v['patch_sha256'],
        handoff_notes=str(p),handoff_notes_sha256=sha(p.read_bytes()),release_proof=str(proof),release_proof_sha256=sha(proof.read_bytes()),
        checkpoint_proof=str(verified),checkpoint_proof_sha256=sha(verified.read_bytes()),new_ROMs=0,
        all_existing_ROMs_and_earlier_translations_preserved=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(notes=str(p),candidate_sha256=v['candidate_sha256'],completed=v['completed'],full_goal_active=True))
