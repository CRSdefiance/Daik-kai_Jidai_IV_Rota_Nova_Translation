"""Save the completed351 append while retaining every earlier review and remaining scope."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


def main():
    root=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105')
    release=load(root/'registered_release_verification.json');credit=load(root/'completion_checkpoint.json')
    assert credit['new_credit']==351 and credit['counts']['completed']==12712
    summary=("Rafael early story and all tutorials remain first. B121–B140's351 reviews are now registered andcredited once "
        "after verified516:201 revisions/150 justified retentions. Cumulative candidate3bf32397 has681 entries/all114 accepted "
        "layers/eight final stages/26 passing release checks andan exactly reconstructable clean-input patch. All867 reviewed "
        "records are integrated in two disjoint credited families;total12712 =7283 revisions+5429 retentions. New351 evidence "
        "covers344 viewed/native body pages,10 captions,22 public names and132 observed variants/134 pages;209 variants remain "
        "offline-only,menu cursor0 only observed. Fresh4001-frame own-identity startup,captain0/route0 andboth Fernan getters pass. "
        "The verified canonical prefix is reused explicitly;new transaction,original final safety contracts andall eight stage "
        "guards execute. Earlier metadata/compiler failures are preserved. Main3cb8,all ROMs andfull scope remain unchanged. "
        "Continue unreviewed Rafael/tutorial complete exchanges fromthe ledger;two catalogue de fixes/global names remain open. "
        "No guide photos orpromotion;deferred artwork andlater older-record re-audit remain separate.")
    document='''# Registered Rafael867 cumulative checkpoint — November 5, 2026

Rafael's early story and all tutorials remain first. Every other storyline, unfinished earlier contextual review, shared town/shop exchange, random scene, speaker label and remaining prose stays in scope. Preserve all translations, ROMs and evidence. No guide photos or main promotion.

## Integrated result

B121–B140 contributes **351 unique reviews:201 revisions/150 justified retentions**. The prior516 andthese351 are now integrated in two disjoint credited families. Total **12712 =7283 revisions+5429 retentions**; historical source/prose12715. `translations/rafael351_integrated_final_review_v2.json` retains exact source/current/final references, individual findings andall five gates. Earlier ledger prefixes andunrelated fields are preserved by the compressed backup andatomic `completion_checkpoint.json`.

Experimental profile: **all-routes-rafael867-extended-checkpoint-v3-20261105**. Candidate: `out/all_routes_rafael867_extended_checkpoint_v3_20261105_candidate.nds`. SHA-256 **3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c**. Its neighboring manifest andxdelta patch are required artifacts. The release proof verifies **681 entries/114 accepted layers/eight final stages/26 checks**,exact record bindings,baseline invariants andbyte-exact reconstruction from clean SHA-256 **f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d**.

Only18 owned SC0 blocks differ from verified516; controls130/131 are unchanged. The cumulative867 changes47 disjoint blocks relative to verified678. All other files/components,accepted artwork,font,names andruntime—including ASCII right bounds—remain exact. SC0 SHA-256 **66a86822e35c2a7a34132ee0c8ccf20198909bfed9c3d747e2f8d3f63d0938e7**. Main3cb827e4,verified516/a51c79e4 andverified678/cc71ec06 are preserved.

## Review and observation scope

Reuse [the351 research-ready checkpoint](editorial_Rafael351_research_ready_20261105.md) for individual prose,wrap,glyph,control,native/storage/catalogue/loader andvisual decisions. All341 speech variants/344 pages,10 captions/five menus and22 public names are checked andviewed. Five full-width I corrections,phrase/page refinements andthe FE planning guard are integrated; no new wording/layout changes were needed during release integration.

The disclosed351 fixtures observed132 variants/134 pages in43,282 frames;209 variants remain offline-only. Menu cursor0 was observed; other states,returns,source branches andcancellation remain offline checks. The previous516 andnew351 fixtures together observed250 variants/255 pages;589 variants remain offline-only. This is composite targeted emulator evidence,not natural conditional activation,original locations,earned chronology,a full route orhardware testing.

Fresh4001-frame ordinary New Game startup uses the exact candidate identity with no savestate/RAM override. Ten RGB pairs match prior directly reviewed frames; own snapshot checks confirm captain0/route0,complete staged payload andruntime resources. Both original actor35 getters return **Fernan Silveira** with normal ASCII F. Full-catalogue UI remains unvisited.

## Authoritative release evidence

All final proofs are under `work/analysis/Rafael867_extended_release_verified_v3_20261105/`: `registered_release_verification.json`,`exact_integrated_record_bindings.json`,`own_registered_startup_verification.json`,`own_Fernan_name_getter_verification.json` and`completion_checkpoint.json`.

The registered v3 workflow reuses the exact672-entry canonical prefix,applies the qualified351 transaction,executes the original canonical builder's complete final safety-contract source andthenall eight original stage bodies/guards/inverses. The manifest explicitly discloses prefix provenance,appended extension andsource hashes;it does not claim a fresh full-prefix build. Transaction andresume qualifications each reject ten bad-input cases. Existing profiles/accepted layers are unchanged. See `Rafael351_release_qualification_v3_20261105/qualification.json`,`Rafael867_registered_extended_resume_v3_20261105/checkpoint_qualification.json` andthe build terminal under `work/analysis/`.

Preserve the failed menu-offset/index-metadata adapter attempts andv2 pre-ROM compiler failure with their telemetry. V3 uses complete native-proof identities,exact current-reference indices andcompiles the original indented extension in function context. No check was weakened andno failed partial result was accepted.

## Continue

Continue unreviewed Rafael/tutorial complete exchanges from clean source andthe coverage ledger;numeric block order is not narrative chronology. Retain completed credit andcompatible evidence. The two catalogue particles **Dinis デ Albuquerque → Dinis de Albuquerque** and **Garcia デ Oviedo → Garcia de Oviedo** still need a qualified pointer-field owner;do not put them inactor35's Fernan-only stage. Global207-name/full-catalogue UI review remains open. Deferred artwork andthe later older-record technical re-audit stay separate. Full goal active.
'''
    checkpoint(mutation='work/analysis/Rafael867_integrated_documentation_checkpoint_v3_20261105',
        batch_key='Rafael867_qualified_cumulative_research_20261105',
        batch_updates=dict(new_credit=0,all867_registered_andcredited_in_two_disjoint_families=True,
            remaining_new_source_credit=0,not_registered_or_promoted=False,registered=True,experimental_not_promoted=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael867 integrated;continue remainingRafael/tutorial complete exchanges',
            current351_registered_verified_andcredited_once=True,current_batch_not_yet_integrated=False,
            registered_integration_pending=False,registered_build_live=False,
            next_action='Continue unreviewed Rafael/tutorial complete exchanges fromclean source/coverage ledger;qualify two catalogue particles separately.',guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael867_registered_checkpoint_v3_20261105.md',document_text=document,completed=12712,
        protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256'],
            'out/all_routes_rafael516_checkpoint_v2_20261105_candidate.nds':'a51c79e4a3581fb49acb0c76de1d5093cb20aad3033bd670e56652575a71fe8f'})
    print('Saved registered867/12712 completion checkpoint;main/full scope preserved. Continue remainingRafael/tutorial editorial work.')


if __name__=='__main__':main()
