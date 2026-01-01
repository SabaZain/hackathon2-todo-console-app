import pytest
from application.services.id_generator import IDGenerator


class TestIDGenerator:
    """Test cases for IDGenerator service."""

    def test_id_generator_initial_value(self):
        """Test that ID generator starts with ID 1."""
        generator = IDGenerator()
        first_id = generator.generate_id()
        assert first_id == 1

    def test_id_generator_sequential_generation(self):
        """Test that ID generator produces sequential IDs."""
        generator = IDGenerator()

        first_id = generator.generate_id()
        second_id = generator.generate_id()
        third_id = generator.generate_id()

        assert first_id == 1
        assert second_id == 2
        assert third_id == 3

    def test_id_generator_unique_ids(self):
        """Test that ID generator produces unique IDs."""
        generator = IDGenerator()

        ids = set()
        for i in range(10):
            new_id = generator.generate_id()
            assert new_id not in ids  # Each ID should be unique
            ids.add(new_id)

        assert len(ids) == 10  # Should have 10 unique IDs

    def test_id_generator_positive_integers(self):
        """Test that ID generator produces positive integers."""
        generator = IDGenerator()

        for i in range(5):
            new_id = generator.generate_id()
            assert isinstance(new_id, int)
            assert new_id > 0