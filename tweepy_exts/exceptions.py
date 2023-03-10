

class BaseTweepyExtException(Exception):
    pass


class MaxRulesLimitReached(BaseTweepyExtException):
    """Max number of rules has been created"""
