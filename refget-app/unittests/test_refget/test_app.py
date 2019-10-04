from app import *

def test_app():
    assert hasattr(get_sequence, "__call__")
    assert hasattr(get_metadata, "__call__")
    assert hasattr(get_service_info, "__call__")
