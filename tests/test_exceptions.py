from unittest.mock import mock_open, patch

from lib import exceptions


def test_get_os_version_unknown_platform_uses_generic_fallback():
    with patch("lib.exceptions.sys.platform", "freebsd"), \
            patch("lib.exceptions.platform.system", return_value="FreeBSD"), \
            patch("lib.exceptions.platform.release", return_value="14.0"):
        assert exceptions.get_os_version() == "FreeBSD 14.0"


def test_get_os_version_linux_reads_pretty_name():
    release_data = 'NAME="Ubuntu"\nPRETTY_NAME="Ubuntu 24.04 LTS"\n'

    with patch("lib.exceptions.sys.platform", "linux"), \
            patch("lib.exceptions.glob", return_value=["/etc/os-release"]), \
            patch("builtins.open", mock_open(read_data=release_data)):
        assert exceptions.get_os_version() == "Ubuntu 24.04 LTS"


def test_get_os_version_linux_without_pretty_name_uses_fallback():
    release_data = 'NAME="Ubuntu"\nVERSION_ID="24.04"\n'

    with patch("lib.exceptions.sys.platform", "linux"), \
            patch("lib.exceptions.glob", return_value=["/etc/os-release"]), \
            patch("builtins.open", mock_open(read_data=release_data)), \
            patch("lib.exceptions.platform.system", return_value="Linux"), \
            patch("lib.exceptions.platform.release", return_value="6.8.0"):
        assert exceptions.get_os_version() == "Linux 6.8.0"


def test_get_os_version_macos_subprocess_failure_uses_fallback():
    with patch("lib.exceptions.sys.platform", "darwin"), \
            patch("lib.exceptions.subprocess.run", side_effect=OSError), \
            patch("lib.exceptions.platform.system", return_value="Darwin"), \
            patch("lib.exceptions.platform.release", return_value="23.6.0"):
        assert exceptions.get_os_version() == "Darwin 23.6.0"
