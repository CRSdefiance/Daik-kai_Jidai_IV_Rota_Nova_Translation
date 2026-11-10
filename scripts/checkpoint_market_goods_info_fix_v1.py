"""Record the registered user-reported fix and continue the preserved editorial queue."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS,NEW_FORMAT,PAYLOAD
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT=Path('work/market_goods_info_terminator_20261109_v1')
OUT=Path('work/market_goods_info_terminator_release_v1')

def main():
    release_path=OUT/'registered_release_verification.json';release=load(release_path)
    registry_path=Path('translations/release_stack.json');registry=load(registry_path)
    assert digest(registry_path)==release['registry_sha256']
    assert digest(release['candidate'])==release['candidate_sha256'] and digest(release['patch'])==release['patch_sha256']
    assert digest(release['manifest'])==release['manifest_sha256']
    assert Path(release['exact_clean_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert (release['registered_manifest_entries'],release['passing_release_checks'],release['accepted_layers'])==(710,45,114)
    assert not release['own_registered_startup_pending'] and not release['market_gameplay_pending']
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    arm=NdsImage.open(release['candidate']).read_file('/__arm9__.bin');sections=MainCodeFile(arm,0x02000000).sections
    assert len(sections)==6 and (sections[-1].ramAddress,bytes(sections[-1].data))==(NEW_FORMAT,PAYLOAD)
    assert all(struct.unpack_from('<I',arm,f)[0]==NEW_FORMAT for f in FIELDS)
    diagnosis=load(ROOT/'diagnosis.json');source_records=[]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for ident,field,offset in [('Local',0xC3EF8,0x15A058),('Cargo',0xC4074,0x15A074)]:
        original=clean[offset:clean.index(0,offset)]
        source_records.append(dict(id='MARKET_GOODS_INFO_'+ident.upper()+'_PRINTF_TERMINATOR',
            source_reference=dict(file_path='/__arm9__.bin',pointer_field=field,format_offset=offset,source_hex=original.hex()),
            source_Japanese_format=original.decode('cp932'),
            current_reference=dict(ROM=diagnosis['build_bindings'][0]['ROM'],ROM_sha256=diagnosis['build_bindings'][0]['ROM_sha256'],
                pointer_field=field,format_address=0x01FFC6A0,missing_terminator_address=0x01FFC6AC),
            registered_reference=dict(ROM=release['candidate'],ROM_sha256=release['candidate_sha256'],pointer_field=field,
                format_address=NEW_FORMAT,exact_terminated_allocation_hex=PAYLOAD.hex()),
            finding='Town capture code at1FFC6AC replaced the format’s required NUL; native printf continued into live machine code.',
            revision='Relocate the shared complete terminated format to a new declared16-byte read-only autoload section; point this original consumer to it.',
            meaning_andargument_order_preserved='commodity name/category/integer percentage; one literal percent; no change to shortage/trend predicates.',
            technical_display_fix_not_new_contextual_dialogue_credit=True,new_credit=0))
    coverage=OUT/'source_current_registered_coverage.json'
    assert not coverage.exists()
    save(coverage,dict(records=source_records,root_causes_fixed=1,original_consumer_aliases_fixed=2,
        new_localized_dialogue_records=0,integrated_editorial_totals_unchanged=19462,new_credit=0,
        diagnosis=str(ROOT/'diagnosis.json'),diagnosis_sha256=digest(ROOT/'diagnosis.json'),
        native_verification=str(ROOT/'native_verification_v1.json'),native_verification_sha256=digest(ROOT/'native_verification_v1.json'),
        gameplay=release['market_gameplay'],gameplay_sha256=release['market_gameplay_sha256']))
    build_doc=Path('docs/build_continuity_protocol.md');backup=OUT/'build_continuity.before.md'
    assert not backup.exists();backup.write_bytes(build_doc.read_bytes())
    intro='''Market Goods Info terminator correction uses `scripts/build_registered_market_goods_info_fix_v4.py`
over the exact registered Maria301 predecessor. Profiles carrying
`market_goods_info_terminator` must preserve its registered16-byte read-only
autoload section at01FFD000 and the two Local/Cargo format pointers. The original
town capture instruction at01FFC6AC must remain code; restoring a zero there would
break the town-label routine. Require the full710-entry prefix,114 accepted layers,
ASCII right-bound stage, exact clean-input patch and verified own startup/market
proofs. Later editorial successors must extend this registered output and reconcile
their parent config; do not silently rebuild from Maria301 and lose the correction.
The Maria270 offline/source prose remains valid: SC3/COMMON/fonts and its relevant
renderer/macro/name instructions are unchanged. Reuse exact matching dependencies;
do not replay its completed266 bodies. B50’s16-record FE issue remains separate.
Main promotion still requires user acceptance.

'''
    build_doc.write_text(intro+build_doc.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    summary=('The user-reported Trade/Goods Info garbage is fixed in the registered710-entry/45-check cumulative candidate '
        '243e21fc, preserving114 accepted layers andthe ASCII right-bound repair. Native Cheese/Food101 reproduces the exact '
        'Rafael2952 defect; corrected Local/Cargo gameplay, own coldboot/new data and24 protected getters pass. Exact clean-input '
        'patch reconstructs the candidate. Main andintegrated19,462 remain unchanged. Resume Maria270 stored/gameplay checks; '
        'B50/16 stays held for its independent FE risk. No guide photos ornew editorial credit.')
    text=f'''# Registered Market Goods Info fix — November 9, 2026

The reported Japanese-looking text is a confirmed formatting/allocation defect, now fixed in a registered cumulative test candidate. The user’s `all_routes_rafael2952_extended_checkpoint_v1_20261106_candidate.nds` (SHA-256 `eea90c3c20fffd8b1f9261be82fe2c76933757a9c2e577cf77f4455b0b9fa22f`) and the later Maria301 both point Local/Cargo formats to01FFC6A0. Their required NUL at01FFC6AC was overwritten by the live town-stock CAPTURE instruction. Executing native printf reproduces the screenshot’s extra “ら…岩…ょ” bytes from that machine code; this is not an untranslated Japanese sentence.

Testing candidate: [all_routes_market_goods_info_fix_candidate.nds](../{OUT.as_posix()}/all_routes_market_goods_info_fix_candidate.nds), SHA-256 `{release['candidate_sha256']}`.
Clean-input patch: [all_routes_market_goods_info_fix_candidate.xdelta](../{OUT.as_posix()}/all_routes_market_goods_info_fix_candidate.xdelta), SHA-256 `{release['patch_sha256']}`.
The patch reconstructs the whole candidate byte for byte from `work/clean.nds` (`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`). The manifest is `{release['manifest']}`, SHA-256 `{release['manifest_sha256']}`.

Only ARM9 changes: two original literal pointers now select a complete terminated format in a new declared16-byte read-only autoload section at01FFD000. Every preexisting code/data section and the town-capture opcode remain intact except the two pointers and required autoload metadata. Complete serialized ARM9 and whole-ROM parent inverses pass. All dialogue archives, names, fonts, graphics, trade calculations, shortage/trend predicates and other components are preserved. The screenshot and exact source/current/registered aliases are bound in `source_current_registered_coverage.json`. One root cause/two aliases fixed; zero new dialogue-review credit.

The native matrix runs12 old-defect and12 exact corrected cases with identical name/category/integer arguments, including Cheese/Food101 and both original Local/Cargo pointer fields. All complete outputs/NULs, ABI returns, input/output canaries and unowned memory pass. A fresh4,001-frame ordinary Rafael New Game matches six earlier approved startup RGB frames; its own ITCM/main-RAM export proves the new allocation, pointers and unchanged town instruction loaded correctly. Both original getters return all12 protected names from this candidate’s own RAM.

An11,600-frame genuine-save coldboot uses the unchanged original controller/stylus schedule and an isolated byte-exact battery copy. Actual Local and Cargo Goods Info show Olive Oil/Cond.100 with all224 expected text pixels and all formerly garbled suffix cells blank. The source Cheese/Food101 case is exact native evidence; the actual gameplay case is Olive Oil, not Amsterdam/Cheese. Town stock and both panel views were directly viewed. Pending cargo totals are a drag preview, not proof of a completed purchase. No savestate, stock/location/money/RNG/event override or hardware claim.

The historical V354 pixel origin needed its current one-pixel composition offset for exact matching; no font, spacing or bitmap geometry was changed. Initial pre-stage syntax/AST/component-classification failures and pre-frame harness-option/touchscreen rejections are preserved. The registered driver isv4; successful startup is `startup_run_v2`, market replay is `market_run_v3`. Do not rerun the failed producers or confuse them with target-ROM failures.

Registration preserves the exact709-entry predecessor prefix and adds the technical correction as entry710/check45, with all114 accepted layers andthe ASCII right-bound correction retained. Registry SHA-256 `{release['registry_sha256']}`. Every prior profile, the canonical baseline and promoted main `all-routes-unified-v4701` remain unchanged; no promotion occurred. All generated ROMs andearlier translations/evidence remain. Use a copy of an existing save with the matching new ROM basename when testing; preserve the original save.

**Continue from [Maria270 offline](editorial_Maria270_offline_20261109.md)**:270 contextual reviews/161 revisions/109 retentions,266 native bodies/272 viewed pages,26 wrap improvements/six layout retentions andfour pages reclaimed. Stored-script checks, representative gameplay andregistered integration remain. The full286 source/prose reviews are preserved; completeB50/16 remains held for its independent long-FE guard/bounds issue. This market fix does not resolve or defer that issue. Reconcile the new registered parent before a later build, reuse matching SC3/COMMON/font/renderer dependencies anddo not repeat completed checks. Full story/town/shop/random/name/player prose scope remains active; integrated totals stay19,462. No guide photos. Deferred artwork andthe later older-record technical re-audit remain separate. No process is live.
'''
    handoff=OUT/'testing_handoff.md'
    save_text=('Registered cumulative test candidate;main unchanged.\n\n'
        f'ROM: `{CANDIDATE_NAME}`\n' if False else
        f'# Market Goods Info test candidate\n\nROM: [all_routes_market_goods_info_fix_candidate.nds](all_routes_market_goods_info_fix_candidate.nds)\n\n'
        f'Clean-input patch: [all_routes_market_goods_info_fix_candidate.xdelta](all_routes_market_goods_info_fix_candidate.xdelta)\n\n'
        f'ROM SHA-256: `{release["candidate_sha256"]}`\n\n'
        'Fixes the Goods Info machine-code suffix in both Local and Cargo; native and genuine-save emulator checks pass. Includes every registered predecessor layer; main remains unchanged. Preserve your old ROM/save and use a copied save with the new ROM basename. Hardware remains untested.\n')
    assert not handoff.exists();handoff.write_text(save_text,encoding='utf-8')
    checkpoint(mutation=OUT/'registered_documentation_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Market Goods Info NUL bug registered;resume Maria270 stored/gameplay checks.',
            next_action='Reconcile710-entry market-fix parent;continue Maria270 stored reconstruction/catalogue/load checks andrepresentative gameplay,thenregistered integration. Retain B50 full source/prose andFE risk.',
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False),
        new_entries={'market_goods_info_NUL_fix_20261109':dict(new_credit=0,status='registered-fixed',root_causes_fixed=1,
            consumer_aliases_fixed=2,source_current_registered_references=str(coverage),coverage_sha256=digest(coverage),
            release=str(release_path),release_sha256=digest(release_path),registered_candidate=release['candidate'],
            registered_candidate_sha256=release['candidate_sha256'],new_localized_records=0,
            native_source_cases=12,native_corrected_cases=12,actual_gameplay='genuine-save Local/Cargo,11600frames',
            startup_frames=4001,protected_name_getters=24,hardware_unverified=True,full_goal_complete=False)},
        summary=summary,document='docs/editorial_market_goods_info_fix_20261109.md',document_text=text,
        completed=19462,protected={str(registry_path):release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256'],
            diagnosis['build_bindings'][0]['ROM']:diagnosis['build_bindings'][0]['ROM_sha256']})
    save(OUT/'final_handoff_readback.json',dict(candidate_sha256=digest(release['candidate']),manifest_sha256=digest(release['manifest']),
        patch_sha256=digest(release['patch']),registry_sha256=digest(registry_path),integrated_records=19462,
        original_user_ROM_preserved=True,main_profile_unchanged='all-routes-unified-v4701',new_credit=0,
        build_continuity_before_sha256=digest(backup),build_continuity_after_sha256=digest(build_doc),full_goal_complete=False))
    print('Savedregistered market fix/testing handoff;original userROM/main preserved;19462 credited unchanged. Maria270 resumesnext.')

if __name__=='__main__':main()
