"""Write a concise handoff for the verified cumulative retrospective correction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('releases/all_routes_unified_v4987')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v4993/verified_handoff.json');v=read(vp)
    rp=Path('work/analysis/earlier775_release_v4988/registered_release_verification.json');r=read(rp)
    assert v['full_goal_active'] and not v['full_goal_complete'] and r['candidate_sha256']==v['candidate_sha256']
    rom,patch,manifest=map(Path,[r['candidate'],r['patch'],r['manifest']])
    assert sha(rom.read_bytes())==v['candidate_sha256'] and sha(patch.read_bytes())==v['patch_sha256']
    m=read(manifest);assert len(m['batches'])==566 and len(m['checks'])==18 and all(m['checks'].values())
    link=lambda p:Path(p).resolve().as_posix()
    text=(
        '# V4987 cumulative editorial checkpoint\n\n'
        f'[ROM](<{link(rom)}>) · [Clean-input patch](<{link(patch)}>) · [Manifest](<{link(manifest)}>)\n\n'
        'The recommendation offer now uses three rows instead of four, with every word retained. '
        'The two generated trailing spaces preserve the original allocation and terminator. '
        'The other three flagged examples keep their existing layouts because those breaks read better in context. '
        'All four decisions have individual clean-source, wording and layout justifications. No duplicate editorial credit is added.\n\n'
        'This experimental candidate includes the entire V4966 stack: 566 manifest batches and 114 accepted layers. '
        'Only COMMON775 changes from V4966. All other messages, four story files, fonts, graphics, executable components and the staged payload remain exact. '
        'Promoted main remains V4701.\n\n'
        'Verification passed: 42 atomic rejection cases, 78 release/dialogue regression tests, 18 cumulative checks, eight complete native text planes, '
        'all 7,336 warm/cold native message loads, exact message boundaries, complete glyphs, bounds and pagination. '
        'The clean-input patch reconstructs the whole candidate byte for byte. '
        'Current New Game and inherited-battery town cold boots match V4966 across 31 captured frames and five actor/captain checks.\n\n'
        'Two paired 12,001-frame emulator runs exercise the original recommendation, explanation and farewell sequence: 775 → 780 → 766, then normal Istanbul town return. '
        'All six held text panels and ten full paired screens were viewed. The trader portrait/name, measured dialogue timings, 74 surrounding-region samples, '
        'sampled post-farewell images, checked state groups, whole actor and final random seed agree. '
        'These tests use disclosed cargo/demand/share and qualification/quantity inputs. Only two real cargo holds are sold; an earned recommendation or a naturally qualifying large sale is not claimed. '
        'The tests preserve game code and the original effects and do not establish a full playthrough, full-memory or future-world equivalence.\n\n'
        f'ROM SHA-256: `{v["candidate_sha256"]}`\n\n'
        f'Patch SHA-256: `{v["patch_sha256"]}`\n\n'
        f'Required clean-input SHA-256: `{r["clean_input_sha256"]}`\n\n'
        f'Canonical construction base: `{r["canonical_base"]}`\n\n'
        f'Canonical base SHA-256: `{r["canonical_base_sha256"]}`\n\n'
        'Coverage stays at 5,966 completed contextual rereads and 5,969 source/prose reviews. '
        'The next Maria scene has 32 fresh clean-only glosses, with no review credit yet. '
        'The full editorial objective remains active, including every remaining storyline, shared town/shop dialogue, random scenes, Help and other player prose. '
        'Broader earlier wrapping, separate graphics work and the later older-record technical re-audit remain open. All earlier ROMs and translations are preserved.\n\n'
        f'[Current handoff](<{link("docs/editorial_handoff_current.md")}>) · '
        f'[Four-record final review](<{link("translations/earlier_common_wraps_contextual_final_review_v1.json")}>) · '
        f'[Verified checkpoint](<{link(vp)}>)\n')
    ROOT.mkdir(parents=True);p=ROOT/'README.md';p.write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'package_receipt.json',dict(candidate=str(rom),candidate_sha256=v['candidate_sha256'],patch=str(patch),patch_sha256=v['patch_sha256'],
        notes=str(p),notes_sha256=sha(p.read_bytes()),release_proof=str(rp),release_proof_sha256=sha(rp.read_bytes()),checkpoint=str(vp),checkpoint_sha256=sha(vp.read_bytes()),
        new_ROMs=0,all_existing_ROMs_and_earlier_translations_preserved=True,full_goal_active=True,full_goal_complete=False))
    print(dict(notes=str(p),candidate_sha256=v['candidate_sha256'],duplicate_credit=0,Maria_clean_only_uncredited=32,full_goal_active=True))
