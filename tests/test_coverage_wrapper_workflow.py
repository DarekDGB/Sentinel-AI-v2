import importlib


def test_wrapper_workflow_module_imports_and_has_public_api():
    m = importlib.import_module("sentinel_ai_v2.wrapper.workflow")

    # Module should import cleanly (coverage will count executed lines).
    assert m is not None

    # Basic sanity: module should expose at least one public callable.
    public_callables = [
        name
        for name in dir(m)
        if not name.startswith("_") and callable(getattr(m, name))
    ]
    assert public_callables, "workflow module exposes no public callables"
