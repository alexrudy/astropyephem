# -*- coding: utf-8 -*-


def test_attribute_passthrough():
    """Test simple attribute passthrough."""
    from ..targets import FixedBody
    name = "TEST_NAME_HERE"
    o = FixedBody()
    o.name = name
    assert o.name == name
    assert o.__wrapped_instance__.name == name
