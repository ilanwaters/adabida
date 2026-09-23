from datetime import datetime, timezone


def ara_utc():
    """Data i hora actual en UTC, naive (compatible amb columnes DateTime sense timezone)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)