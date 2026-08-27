from __future__ import annotations

from collections import defaultdict
from typing import Any

from mmwo.capabilities import Capability
from mmwo.providers.base import ProviderDescriptor


class CapabilityRegistry:
    def __init__(self) -> None:
        self._providers: dict[Capability, dict[str, tuple[ProviderDescriptor, Any]]] = defaultdict(dict)

    def register(self, descriptor: ProviderDescriptor, provider: Any) -> None:
        bucket = self._providers[descriptor.capability]
        if descriptor.id in bucket:
            raise ValueError(f"Provider id already registered: {descriptor.id}")
        bucket[descriptor.id] = (descriptor, provider)

    def resolve(self, capability: Capability, provider_id: str | None = None) -> Any:
        bucket = self._providers.get(capability, {})
        if provider_id is not None:
            try:
                return bucket[provider_id][1]
            except KeyError as exc:
                raise KeyError(f"Unknown provider {provider_id!r} for {capability.value}") from exc
        if len(bucket) != 1:
            raise LookupError(f"Expected one provider for {capability.value}, found {len(bucket)}")
        return next(iter(bucket.values()))[1]

    def descriptors(self, capability: Capability | None = None) -> list[ProviderDescriptor]:
        buckets = [self._providers.get(capability, {})] if capability else self._providers.values()
        return [descriptor for bucket in buckets for descriptor, _ in bucket.values()]
