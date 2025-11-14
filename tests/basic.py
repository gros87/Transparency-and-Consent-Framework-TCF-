from . import SessionToken

def test_basic_serialization():
    token = SessionToken(
        name="test_token",
        ritual="light candle",
        energy_cost=5,
        boundaries={"inbox_pause": True}
    )
    yaml_str = token.to_yaml()
    deserialized = SessionToken.from_yaml(yaml_str)
    assert deserialized.name == "test_token"
    assert deserialized.energy_cost == 5

# 2. **Empty Boundaries Test**
def test_empty_boundaries():
    token = SessionToken(
        name="no_boundaries",
        ritual="no ritual",
        energy_cost=0,
        boundaries={}
    )
    yaml_str = token.to_yaml()
    deserialized = SessionToken.from_yaml(yaml_str)
    assert deserialized.boundaries == {}

# 3. **Hierarchical Tokens Test**
def test_hierarchical_tokens():
    parent = SessionToken(
        name="parent",
        ritual="parent ritual",
        energy_cost=10,
        child_tokens=["child1", "child2"]
    )
    yaml_str = parent.to_yaml()
    deserialized = SessionToken.from_yaml(yaml_str)
    assert deserialized.child_tokens == ["child1", "child2"]
    assert deserialized.parent_token is None  # Test default value

# 4. **Default Values Test**
def test_default_values():
    minimal_token = SessionToken(
        name="minimal",
        ritual=None,
        energy_cost=1
    )
    yaml_str = minimal_token.to_yaml()
    deserialized = SessionToken.from_yaml(yaml_str)
    assert deserialized.ritual is None
    assert deserialized.duration_minutes == 90
    assert deserialized.energy_units == "bananas"

# 5. **Edge Case with Nested Tokens**
def test_nested_tokens():
    grandparent = SessionToken(
        name="grandparent",
        ritual="grandparent ritual",
        energy_cost=20,
        child_tokens=["parent"]
    )
    parent = SessionToken(
        name="parent",
        ritual="parent ritual",
        energy_cost=10,
        parent_token="grandparent",
        child_tokens=["child1", "child2"]
    )
    # This would require more complex handling in serialization
    # Might need a separate test for full hierarchical serialization