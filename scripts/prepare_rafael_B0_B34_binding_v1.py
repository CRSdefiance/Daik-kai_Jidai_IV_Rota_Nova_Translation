"""Adapt sealed residual drafts to the existing current-text binder without editing the seal."""
from hashlib import sha256
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT, PACKET, SEALED


def main():
    out = ROOT / 'binding_inputs_v1'
    assert not out.exists()
    sealed = SEALED / 'sealed_drafts.json'
    drafts, packet = map(load, (sealed, PACKET))
    assert drafts['records_count'] == 283
    assert all(digest(p) == value for p, value in drafts['evidence'].items())
    groups = [{**g, 'clean_block_sha256': sha256(bytes.fromhex(g['clean_block_hex'])).hexdigest()}
              for g in packet['groups']]
    out.mkdir()
    source = out / 'source_packet.json'
    save(source, {**packet, 'groups': groups, 'unaltered_source_packet': str(PACKET),
        'unaltered_source_packet_sha256': digest(PACKET)})
    save(out / 'meanings.json', dict(records=[{**r, 'current_ROM_English_unconsulted': True}
        for r in drafts['records']], meanings=283, source_packet=str(source), source_packet_sha256=digest(source),
        all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    print('Prepared existing-binder inputs; original seal unchanged.')


if __name__ == '__main__':
    main()
