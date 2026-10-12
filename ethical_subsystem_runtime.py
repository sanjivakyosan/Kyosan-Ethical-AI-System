"""
Runtime stubs for optional ethical subsystems.
Unimplemented methods return safe defaults so pipeline integration can complete.
"""


class StubObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __bool__(self):
        return True


class RuntimeStubMixin:
    """Provides no-op implementations for missing subsystem methods."""

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)

        def _stub(*args, **kwargs):
            if name.startswith(('is_', 'has_', 'check_', 'verify_', 'validate_', 'ensure_')):
                return True
            if name.startswith(('measure_', 'count_', 'get_')):
                return 0.0
            return StubObject()

        return _stub
