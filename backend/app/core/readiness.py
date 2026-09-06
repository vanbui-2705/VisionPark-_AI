from dataclasses import dataclass
from typing import Protocol

from fastapi import Request


@dataclass(frozen=True)
class ReadinessStatus:
    ready: bool
    message: str
    provider: str | None = None
    version: str | None = None

    def to_dict(self) -> dict[str, str | bool | None]:
        return {
            "status": "ready" if self.ready else "not_ready",
            "message": self.message,
            "provider": self.provider,
            "version": self.version,
        }


class ALPRReadinessProbe(Protocol):
    """Stable boundary consumed by Backend Core for `/health/ready`."""

    def readiness(self) -> ReadinessStatus: ...


class ALPRRuntime(Protocol):
    def is_ready(self) -> tuple[bool, str]: ...


class RuntimeALPRProbe:
    """Adapt Person 1's ALPR runtime interface to the shared health contract."""

    def __init__(self, runtime: ALPRRuntime, *, provider: str, version: str) -> None:
        self.runtime = runtime
        self.provider = provider
        self.version = version

    def readiness(self) -> ReadinessStatus:
        try:
            ready, message = self.runtime.is_ready()
        except Exception:
            return ReadinessStatus(
                ready=False,
                message="ALPR readiness check failed.",
                provider=self.provider,
                version=self.version,
            )
        return ReadinessStatus(
            ready=ready,
            message=message,
            provider=self.provider,
            version=self.version,
        )


class UnconfiguredALPRProbe:
    def __init__(self, configured_provider: str):
        self.configured_provider = configured_provider

    def readiness(self) -> ReadinessStatus:
        return ReadinessStatus(
            ready=False,
            message="ALPR runtime has not been wired into the application.",
            provider=self.configured_provider,
            version=None,
        )


def get_alpr_readiness_probe(request: Request) -> ALPRReadinessProbe:
    return request.app.state.alpr_readiness_probe
