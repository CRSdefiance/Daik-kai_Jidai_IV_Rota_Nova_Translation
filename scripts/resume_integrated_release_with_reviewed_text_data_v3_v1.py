"""Explicit checkpoint continuation of the original reviewed_text_data_v3 stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('reviewed_text_data_v3', __file__)


if __name__ == '__main__':
    main()
