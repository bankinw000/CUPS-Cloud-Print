#    CUPS Cloudprint - Print via Google Cloud Print
#    Copyright (C) 2011 Simon Cadman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
import pytest
import logging
import sys
sys.path.insert(0, ".")

from cloudprintrequestor import CloudPrintRequestor

global requestor


def teardown_function(function):
    logging.shutdown()
    reload(logging)


def setup_function(function):
    global requestor
    requestor = CloudPrintRequestor()


def test_requestor():
    global requestor
    requestor.setAccount('testdetails')
    assert requestor.getAccount() == 'testdetails'


def test_request():
    global requestor
    assert requestor.doRequest(
        path="test",
        testResponse=json.dumps("randomstring1233")) == "randomstring1233"
    with pytest.raises(ValueError):
        assert requestor.doRequest(path="test", testResponse="")

    assert requestor.doRequest(
        path="test",
        testResponse=json.dumps("randomstring1233"),
        endpointurl=requestor.CLOUDPRINT_URL) == "randomstring1233"
    with pytest.raises(ValueError):
        assert requestor.doRequest(
            path="test",
            testResponse="",
            endpointurl=requestor.CLOUDPRINT_URL)

    # test doing actual requests, not supplying test reponse data
    # we expect them to fail due to missing auth data
    with pytest.raises(ValueError):
        requestor.doRequest(path="printers")
    with pytest.raises(ValueError):
        requestor.doRequest(path="submit", data="test")
