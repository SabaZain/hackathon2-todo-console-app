class IDGenerator:
    """Service for generating unique task IDs."""

    def __init__(self):
        """Initialize the ID generator with starting value of 0."""
        self._current_id = 0

    def generate_id(self) -> int:
        """Generate and return the next unique ID."""
        self._current_id += 1
        return self._current_id