"""Native literal safety must not disable genuine macro substitution."""

from pathlib import Path

import pytest

from dk4tool.patch.common_literal_prefix import transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_common_literal_prefix_native_v255 import expand, setup


@pytest.fixture(scope="module")
def sources():
    prior = NdsImage.open("out/all_routes_combined_v254_candidate.nds").read_file("/__arm9__.bin")
    fixed, _ = transform(prior)
    return prior, fixed


@pytest.mark.parametrize("text", [b"Fair. I wish a good opportunity.", b"Find it. I'll follow.",
                                  b"F", b"I", b"Indigo Fleet", b"It is fine.", b"Is this okay?"])
def test_real_expander_retains_every_plain_English_byte(sources, text):
    prior, fixed = sources
    assert expand(setup(prior), text) != text
    assert expand(setup(fixed), text) == text


@pytest.mark.parametrize("token,expected", [(b"FI", b"Fleet"), (b"FA", b"Argot Co."),
                                           (b"FO", b"Amsterdam"), (b"FU", b"Indigo")])
def test_genuine_dynamic_name_macros_keep_the_native_dispatch(sources, token, expected):
    prior, fixed = sources
    assert expand(setup(prior), token) == expand(setup(fixed), token) == expected


@pytest.mark.parametrize("actor", [0, 1])
def test_source_IC_pronoun_and_legacy_non_Latin_suffixes_unchanged(sources, actor):
    prior, fixed = sources
    for raw in (b"IC", b"I\n", b"I\x80" + "です".encode("cp932")):
        assert expand(setup(prior), raw, actor) == expand(setup(fixed), raw, actor)


def test_unpinned_source_is_rejected_and_saved_research_matches(sources):
    _prior, fixed = sources
    assert fixed == Path("work/analysis/common_literal_prefix_v255/research_arm9.bin").read_bytes()
    with pytest.raises(ValueError, match="Exact complete V254"):
        transform(fixed)
