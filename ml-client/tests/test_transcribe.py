import os
import pytest
import json
import sys
import string
import random
## import the module to test, processSpeech
sys.path.append('../ml-client')
from processSpeech import query

class Tests:
    #
    # Test functions
    #

    def test_sanity_check(self):
        """
        Test debugging... making sure that we can run a simple test that always passes.
        Note the use of the example_fixture in the parameter list - any setup and teardown in that fixture will be run before and after this test function executes
        From the main project directory, run the `python3 -m pytest` command to run all tests.
        """
        expected = True  # the value we expect to be present
        actual = True  # the value we see in reality
        assert actual == expected, "Expected True to be equal to True!"

    def test_speechfile_nofile(self):
        ## Use random file name
        fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        fileName = fileName + ".m4a"
        try: 
            query(fileName)
        except FileNotFoundError:
            assert True, "Expected file to be not found!"
    
    def test_speechfile_wrongformat(self):
        ## Use wrong file format
        fileName = "command.txt"
        try:
            query(fileName)
        except ValueError:
            assert True, "Expected file to be wrong format!"
    
    def test_speechfile(self):
        ## Use correct file template, should return json
        fileName = "testsample.m4a"
        jsonOutput = query(fileName)
        assert type(jsonOutput) is dict, "Expected file to be json!"
