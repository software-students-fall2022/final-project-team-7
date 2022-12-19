import pytest
import sys
## import the module to test, converOpenAI
sys.path.append('../ml-client')
from converOpenAI import openAI

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
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"

    def test_openAI(self):
        ## Should return string
        prompt = "Hi, I'm a bot. What's your name?"
        jsonOutput = openAI(prompt)
        assert type(jsonOutput) is str, "Expected file to be json!"
    
    def test_openAI_NoParam(self):
        ## Missing parameter
        try: 
            jsonOutput = openAI()
        except TypeError:
            assert True, "Expected TypeError!"
        