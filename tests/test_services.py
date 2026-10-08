from app.services import target_range, parse_public_link

def test_target_range():
    assert target_range(100, 80) == (80, 100)

def test_public_link():
    assert parse_public_link("https://t.me/example/123") == ("example", 123)
