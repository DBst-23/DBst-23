"""Fail-closed The Odds API v4 *live event-odds* credit accounting.

Pure functions only: no HTTP, credentials or database calls. This is NOT the
historical endpoint (different, 10x billing), nor the all-events odds endpoint.
Provider reference: https://the-odds-api.com/liveapi/guides/v4/
"""
from collections.abc import Mapping

# Limit the pilot to NBA second-half markets, including each team's 2H total.
# The Odds API counts one unique market key, not one per team, in a region.
PILOT_MARKETS = frozenset(("totals_h2", "spreads_h2", "h2h_h2", "team_totals_h2"))
VALID_REGIONS = frozenset(("us", "us2", "uk", "eu", "au"))
USAGE_FIELDS = ("x-requests-last", "x-requests-used", "x-requests-remaining")


class CreditAccountingError(ValueError):
    """Inconsistent/unknown provider billing; retain the full reservation."""


def parse_regions(regions):
    if not isinstance(regions, str):
        raise CreditAccountingError("Regions must be a comma-separated string")
    parts = regions.split(",")
    if not parts or any(not item or item != item.strip() for item in parts):
        raise CreditAccountingError("Malformed regions")
    if len(parts) != len(set(parts)) or not set(parts) <= VALID_REGIONS:
        raise CreditAccountingError("Duplicate or unsupported regions")
    return tuple(parts)


def validate_markets(markets):
    if not isinstance(markets, (tuple, list)) or not markets:
        raise CreditAccountingError("Markets must be a nonempty list or tuple")
    if any(not isinstance(m, str) for m in markets):
        raise CreditAccountingError("Invalid market")
    if len(markets) != len(set(markets)) or not set(markets) <= PILOT_MARKETS:
        raise CreditAccountingError("Duplicate or unsupported pilot market")
    return tuple(markets)


def worst_case_credits(markets, regions):
    """Event odds maximum = requested distinct market count x region count."""
    return len(validate_markets(markets)) * len(parse_regions(regions))


def parse_usage_headers(headers):
    """Read numeric billing metadata. Never return raw headers or API keys."""
    if not isinstance(headers, Mapping):
        raise CreditAccountingError("Missing usage headers")
    lowered = {str(k).lower(): v for k, v in headers.items()}
    result = {}
    for key in USAGE_FIELDS:
        value = lowered.get(key)
        if not isinstance(value, str) or not value.strip().isascii() or not value.strip().isdigit():
            raise CreditAccountingError("Missing or invalid provider usage header")
        result[key] = int(value.strip())
    charge = result["x-requests-last"]
    used = result["x-requests-used"]
    if charge > used:
        raise CreditAccountingError("Provider usage counters inconsistent")
    return {"charge": charge, "used": used, "remaining": result["x-requests-remaining"]}


def reconcile_event_usage(headers, payload, markets, regions, reserved_credits):
    """Validate v4 event-odds charge against response markets and pre-call hold.

    A returned market counts only once even when multiple bookmakers offer it.
    Missing/malformed metadata fails closed; zero-cost empty bookmaker data is
    accepted ONLY with an explicit x-requests-last: 0 provider header.
    """
    requested = set(validate_markets(markets))
    region_count = len(parse_regions(regions))
    maximum = len(requested) * region_count
    if type(reserved_credits) is not int or reserved_credits < maximum:
        raise CreditAccountingError("Insufficient worst-case credit reservation")
    if not isinstance(payload, dict) or not isinstance(payload.get("bookmakers"), list):
        raise CreditAccountingError("Malformed event odds response")
    seen = set()
    for book in payload["bookmakers"]:
        if not isinstance(book, dict) or not isinstance(book.get("markets"), list):
            raise CreditAccountingError("Malformed bookmaker markets")
        for market in book["markets"]:
            if not isinstance(market, dict) or not isinstance(market.get("key"), str):
                raise CreditAccountingError("Malformed returned market")
            seen.add(market["key"])
    if not seen <= requested:
        raise CreditAccountingError("Unexpected market in provider response")
    reported = parse_usage_headers(headers)
    expected_charge = len(seen) * region_count
    if reported["charge"] != expected_charge or reported["charge"] > reserved_credits:
        raise CreditAccountingError("Provider billed charge does not match returned markets")
    return reported
