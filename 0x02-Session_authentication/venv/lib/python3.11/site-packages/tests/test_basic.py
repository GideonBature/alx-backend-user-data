"""Automated testing for Basic"""
import os
import string
import random
import pytest

from basic_auth import Auth

AUTH = Auth()


# Create some random values
def random_string(string_length=15):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


KEY = random_string()
VALUE = random_string()


def test_encode():
    """Test encoding credentials"""
    assert AUTH.encode("username",
                       "password") == 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
    assert AUTH.encode(
        "YuEA33Ss*o55uk0!vKc7", "93H20VlU&vyuSr$aS&kJ"
    ) == 'Basic WXVFQTMzU3MqbzU1dWswIXZLYzc6OTNIMjBWbFUmdnl1U3IkYVMma0o='


def test_decode():
    """Test decoding credentials"""
    assert AUTH.decode('Basic dXNlcm5hbWU6cGFzc3dvcmQ=') == "username:password"
    assert AUTH.decode(
        'Basic WXVFQTMzU3MqbzU1dWswIXZLYzc6OTNIMjBWbFUmdnl1U3IkYVMma0o='
    ) == "YuEA33Ss*o55uk0!vKc7:93H20VlU&vyuSr$aS&kJ"


def test_check_config_dir():
    """Test directory related operations"""
    # Check no folder exists already
    assert AUTH.check_config_dir() is False

    # Create directory
    assert AUTH.create_config_directory() is True

    # Verify directory exists
    assert AUTH.check_config_dir() is True

    # Create read only directory
    Auth(config_dir="config/readonly").create_config_directory()
    os.chmod("config/readonly", 444)

    # Test writing to read only
    assert Auth(
        config_dir="config/readonly/test").create_config_directory() is False


def test_check_file_exists():
    """Test file related operations"""
    # Check file doesn't exist
    assert AUTH.check_file_exists('nofile') is False

    # Test a directory
    assert AUTH.check_file_exists("readonly") is False

    # Create file and verify
    AUTH.write_config("", "test.json")
    assert AUTH.check_file_exists('test.json') is True


def test_write_config():
    """Test writing config to files"""
    # Create some dummy data
    data = {}
    data[KEY] = VALUE

    # Overwrite file from previous test with random data
    assert AUTH.write_config(data, "test.json") is True

    # Try to write in a readonly folder
    assert Auth("config/readonly").write_config(data, "test.json") is False

    # Try to create a new folder
    assert Auth("config/newfolder").write_config(data, "test.json") is True

    # Create new folder in read only will sys.exit
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        Auth("config/readonly/newfolder").write_config(data, "test.json")
    assert pytest_wrapped_e.type == SystemExit


def test_read_config():
    """Test opening files"""
    # Try to open a non existant config
    assert AUTH.read_config('nofile.json') is False

    # Try a directory
    assert AUTH.read_config('readonly') is False

    # Try a good file
    assert isinstance(AUTH.read_config("test.json"), dict) is True

    # Try a bad file
    with open("config/bad_file.json", 'w') as outfile:
        outfile.write("Thisisbaddata")
    assert AUTH.read_config("bad_file.json") is False


def test_verify_config():
    """Verify written config"""
    # Verify config written earlier
    assert AUTH.verify_config("test.json", KEY, VALUE) is True

    # Verify config mismatch
    assert AUTH.verify_config("test.json", KEY, "Not value") is False

    # Verify non json data
    assert AUTH.verify_config("bad_file.json", KEY, VALUE) is False
