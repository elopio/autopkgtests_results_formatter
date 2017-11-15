# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from urllib import request

from autopkgtest_results_formatter import errors


_BASE_RESULTS_URL = (
    'https://objectstorage.prodstack4-5.canonical.com/v1/'
    'AUTH_77e2ada1e7a84929a74ba3b87153c0ac')


class ResultsIndex():
    """The index of a PPA autopkgtest results for distro version.

    It must be used as a context manager.
    """

    def __init__(
            self, *, distro, ppa_user, ppa_name,
            base_results_url=_BASE_RESULTS_URL):
        """Index constructor.

        :param str distro: The name of the distro, for example: xenial.
        :param str ppa_user: The name of the owner of the PPA. A Launchpad user
            or team, without the `~`.
        :param str ppa_name: The name of the PPA.
        :param str base_results_url: The URL where the index is stored. Default
            is the URL to Canonical's prodstack server where Ubuntu autopkgtest
            results are stored. autopkgtest-{distro}-{ppa_user}-{ppa_name} will
            be appended to this string to form the complete URL to the results
            index.
        """
        super().__init__()
        self._distro = distro
        self._ppa_user = ppa_user
        self._ppa_name = ppa_name
        self._base_results_url = base_results_url
        self._index_file_path = None

    def __enter__(self):
        self._index_file_path = self._download_index()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        request.urlcleanup()

    def _download_index(self):
        """Download the index file.

        :return str: The path to a local file with the results index.
        """
        url = '{base_url}/autopkgtest-{distro}-{ppa_user}-{ppa_name}'.format(
            base_url = self._base_results_url, distro=self._distro,
            ppa_user=self._ppa_user, ppa_name=self._ppa_name)
        return request.urlretrieve(url)[0]

    def read(self):
        """Return the contents of the index.

        :return str: The full contents of the index.
        :raises errors.ResultsIndexNotDownloadedError: If a method is called
            before the index has been downloaded.
        """
        if not self._index_file_path:
            raise errors.ResultsIndexNotDownloadedError(action='read index')
        with open(self._index_file_path, 'r') as index_file:
            return index_file.read()