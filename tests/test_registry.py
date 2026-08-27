import pytest

from mmwo.capabilities import Capability
from mmwo.providers.base import ProviderDescriptor
from mmwo.registry import CapabilityRegistry


def test_registry_resolves_single_provider() -> None:
    registry = CapabilityRegistry()
    provider = object()
    registry.register(ProviderDescriptor("mock-image", Capability.IMAGE_GENERATION, "mock"), provider)
    assert registry.resolve(Capability.IMAGE_GENERATION) is provider


def test_registry_rejects_duplicate_ids() -> None:
    registry = CapabilityRegistry()
    descriptor = ProviderDescriptor("mock-image", Capability.IMAGE_GENERATION, "mock")
    registry.register(descriptor, object())
    with pytest.raises(ValueError):
        registry.register(descriptor, object())
