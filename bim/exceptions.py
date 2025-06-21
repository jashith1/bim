class BreakException(Exception):
    """Exception used to implement break statements"""
    pass

class ContinueException(Exception):
    """Exception used to implement continue statements"""
    pass

class ReturnException(Exception):
    """Exception used to implement return statements"""
    def __init__(self, value=None):
        self.value = value