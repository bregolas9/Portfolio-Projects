from common.item import Item


def test_it_should_set_item_descriptions():
    """Test to make sure the item description setter works correctly."""
    item = Item(
        name="Test Item",
        alias="Test Alias",
        description=["This is a test description."],
        look_at_message={"line1": "a look at message"},
        is_collectible=True,
        discovered=False,
        interactions={},
    )
    item.description = ["updated description"]
    assert item.description == "updated description"
