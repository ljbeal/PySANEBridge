from bridge.connection.connection import Connection


def test_userhost():
    """Test generating a Connection with user@host"""
    assert Connection("test@host").userhost == "test@host"


def test_host_only():
    """Test generating a Connection with only user"""
    assert Connection("host").userhost == "host"
