from __future__ import annotations
from typing import Callable, Dict, List, Any, Optional

class Hooks:
    """A tiny, dependency-free hook system.

    - Register callbacks under a string key (event name).
    - Emit events with arbitrary kwargs; results are collected and returned.
    - Supports simple middleware patterns across modules (HTTP, clients, diagnostics).

    Example:
        hooks = Hooks()
        hooks.on("http:before_request", lambda req: req)
        hooks.emit("http:before_request", req=request)
    """

    def __init__(self) -> None:
        self._events: Dict[str, List[Callable[..., Any]]] = {}

    def on(self, event: str, fn: Callable[..., Any]) -> None:
        """Register a callback for an event.

        Args:
            event: The event name.
            fn: The callback function.
        """
        self._events.setdefault(event, []).append(fn)

    def off(self, event: str, fn: Callable[..., Any]) -> None:
        """Remove a callback for an event if present."""
        if event in self._events:
            self._events[event] = [f for f in self._events[event] if f is not fn]
            if not self._events[event]:
                del self._events[event]

    def clear(self, event: Optional[str] = None) -> None:
        """Clear all callbacks for an event, or all events if None."""
        if event is None:
            self._events.clear()
        else:
            self._events.pop(event, None)

    def emit(self, event: str, **kwargs: Any) -> List[Any]:
        """Emit an event and collect results from listeners.

        Args:
            event: The event name.
            **kwargs: Arbitrary keyword args to pass to listeners.

        Returns:
            A list of results returned by listeners (order preserved).
        """
        listeners = self._events.get(event, [])
        results: List[Any] = []
        for fn in listeners:
            try:
                results.append(fn(**kwargs))
            except Exception as _:
                # Best-effort hooks: ignore listener errors to avoid breaking core flows
                results.append(None)
        return results
