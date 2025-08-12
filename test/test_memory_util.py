import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.memoryvault.services import MemoryManagement, SlideshowModes


@pytest.fixture
def memory_mock():
    mock = MagicMock()
    mock.id = 1
    mock.to_json.return_value = {
        "id": 1,
        "description": "Mock memory",
        "date": "2025-01-01",
        "latitude": 51.00399,
        "longitude": 10.29633,
        "image_uri": "test.jpg",
        "vault_id": 1
    }
    return mock


@patch("src.memoryvault.services.memory_util.db")
@patch("src.memoryvault.services.memory_util.Memory")
@patch("src.memoryvault.services.memory_util.MemoryManagement.save_image")
def test_upload_memory(mock_save_image, MockMemory, mock_db):
    """
    Tests the upload of a memory. Due to the use of the patch module no entry will be added to db.
    """
    mock_save_image.return_value = "test.jpg"
    mock_instance = MagicMock()
    MockMemory.return_value = mock_instance

    MemoryManagement.upload_memory(
        description="Test memory",
        date="2025-01-01",
        latitude=51.00399,
        longitude=10.29633,
        image_file="test.jpg",
        vault_id=1
    )

    MockMemory.assert_called_once()
    mock_db.session.add.assert_called_once_with(mock_instance)
    mock_db.session.commit.assert_called_once()


@patch("src.memoryvault.services.memory_util.Memory")
def test_get_memory_data(MockMemory, memory_mock):
    """
    Tests retieving the data of a memory from the db.
    """
    MockMemory.query.filter_by.return_value.first.return_value = memory_mock
    result = MemoryManagement.get_memory_data(1)
    assert result["id"] == 1
    assert result["description"] == "Mock memory"
    assert result["date"] == "2025-01-01"


@patch("src.memoryvault.services.memory_util.Memory")
def test_get_slideshow_order(MockMemory):
    """
    Tests retrieving the slideshow memory order in different order types.
    """
    mock1 = MagicMock(id=1, date=datetime(2025, 7, 1).date())
    mock2 = MagicMock(id=2, date=datetime(2025, 7, 2).date())
    MockMemory.query.filter_by.return_value\
        .filter.return_value.order_by.return_value.\
        all.return_value = [mock1, mock2]

    ids = MemoryManagement.get_slideshow_order(
        vault_id=1,
        order=SlideshowModes.CHRONOLOGICAL,
        period_start=datetime(2025, 1, 1).date(),
        period_end=datetime(2025, 12, 31).date()
    )
    assert ids == [1, 2]

    ids = MemoryManagement.get_slideshow_order(
        vault_id=1,
        order=SlideshowModes.REVERSE_CHRONOLOGICAL,
        period_start=datetime(2025, 1, 1).date(),
        period_end=datetime(2025, 12, 31).date()
    )
    assert ids == [2, 1]

    ids = MemoryManagement.get_slideshow_order(
        vault_id=1,
        order=SlideshowModes.RANDOM,
        period_start=datetime(2025, 1, 1).date(),
        period_end=datetime(2025, 12, 31).date()
    )
    assert set(ids) == {1, 2}
