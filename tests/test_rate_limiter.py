import pytest

from app.security.rate_limiter import RateLimiter


class MockClock:
    def __init__(self, value=0.0):
        self.value = value

    def __call__(self):
        return self.value


def test_client_can_reach_configured_limit():
    clock = MockClock()
    limiter = RateLimiter(max_requests=2, window_seconds=10, clock=clock)

    assert limiter.check("client") == (True, 0)
    assert limiter.check("client") == (True, 0)


def test_next_request_is_rejected():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    limiter.check("client")

    allowed, retry_after = limiter.check("client")

    assert allowed is False
    assert retry_after == 10


def test_request_is_allowed_after_complete_window():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    assert limiter.check("client")[0] is True
    clock.value = 10

    assert limiter.check("client") == (True, 0)


def test_different_clients_have_independent_limits():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    assert limiter.check("client-a")[0] is True
    assert limiter.check("client-a")[0] is False
    assert limiter.check("client-b") == (True, 0)


def test_reset_clears_limiter_state():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    limiter.check("client")
    limiter.reset()

    assert limiter.check("client") == (True, 0)



def test_retry_after_rounds_up_fractional_remaining_time():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    limiter.check("client")
    clock.value = 0.1

    allowed, retry_after = limiter.check("client")

    assert allowed is False
    assert retry_after == 10

    clock.value = 7.2

    allowed, retry_after = limiter.check("client")

    assert allowed is False
    assert retry_after == 3


def test_expired_client_entries_are_removed():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    limiter.check("expired-client")
    clock.value = 10
    limiter.check("active-client")

    assert "expired-client" not in limiter._requests
    assert "active-client" in limiter._requests


@pytest.mark.parametrize(
    ("max_requests", "window_seconds"),
    [(0, 10), (-1, 10), (1, 0), (1, -1)],
)
def test_invalid_constructor_parameters_are_rejected(
    max_requests, window_seconds
):
    with pytest.raises(ValueError):
        RateLimiter(max_requests, window_seconds)


def test_exact_expiration_boundary_is_allowed():
    clock = MockClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)

    limiter.check("client")
    clock.value = 10.0

    assert limiter.check("client") == (True, 0)
