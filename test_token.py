from session_token import SessionToken
import yaml

def test_token_serialization():
    token = SessionToken(
        name="dragon_slaying",
        ritual="light candle",
        energy_cost=5,
        boundaries={"inbox_pause": True}
    )
    print("YAML Output:", token.to_yaml())
    print("Boundary Check:", token.check_boundaries())

if __name__ == "__main__":
    test_token_serialization()