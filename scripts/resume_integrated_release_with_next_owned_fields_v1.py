"""Explicit checkpoint continuation of the original next_owned_fields stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('next_owned_fields', __file__)


if __name__ == '__main__':
    main()
