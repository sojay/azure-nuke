"""Compatibility tests for legacy top-level src imports."""


def test_legacy_src_modules_reexport_canonical_implementations():
    """Legacy src.* imports should point at aznuke.src implementations."""
    from aznuke.src import auth as canonical_auth
    from aznuke.src import deletion as canonical_deletion
    from aznuke.src import discovery as canonical_discovery
    from aznuke.src import filtering as canonical_filtering
    from aznuke.src import safety as canonical_safety
    from src import auth as legacy_auth
    from src import deletion as legacy_deletion
    from src import discovery as legacy_discovery
    from src import filtering as legacy_filtering
    from src import safety as legacy_safety

    assert legacy_auth.get_credentials is canonical_auth.get_credentials
    assert legacy_discovery.discover_all_resources is canonical_discovery.discover_all_resources
    assert legacy_filtering.filter_resources is canonical_filtering.filter_resources
    assert legacy_safety.require_confirmation is canonical_safety.require_confirmation
    assert legacy_deletion.detach_disk is canonical_deletion.detach_disk
    assert legacy_deletion.delete_resources is canonical_deletion.delete_resources
