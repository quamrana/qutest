import unittest
import inspect

__unittest = True


def skip(reason='Skip'):
    return unittest.skip(reason)


class parameterized:
    '''
    Use this decorator on test methods like this:
    @parameterized(actual=[5,6],expected=[5,6])
    def test3(self, actual, expected):
        self.shouldEqual(actual,expected)

    The example uses parameters actual and expected, but they can be anything you like, as long
    as the parameters match in number and name.
    This decorator uses unittest.TestCase.subTest to separately markup every failing test.
    '''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, fn):
        def test_wrapped(itself):
            size = len(self.kwargs[list(self.kwargs.keys())[0]])
            for index in range(size):
                test_method_parameters = {k: self.kwargs[k][index] for k in self.kwargs}
                with itself.subTest(**test_method_parameters):
                    fn(itself, **test_method_parameters)

        return test_wrapped


class TestCase(unittest.TestCase):
    def shouldEqual(self, actual, expected, userMsg=None):
        userMsg = self.__getUserMessage(userMsg)
        msg = "%s should be %s" % (userMsg, expected)
        self.assertEqual(expected, actual, msg)

    def shouldNotEqual(self, actual, expected, userMsg=None):
        userMsg = self.__getUserMessage(userMsg)
        msg = "%s should not be %s" % (userMsg, expected)
        self.assertNotEqual(expected, actual, msg)

    def shouldBeTrue(self, actual, userMsg=None):
        userMsg = self.__getUserMessage(userMsg)
        msg = "%s should be True" % str(userMsg)
        self.assertTrue(actual, msg)

    def shouldBeFalse(self, actual, userMsg=None):
        userMsg = self.__getUserMessage(userMsg)
        msg = "%s should be False" % str(userMsg)
        self.assertFalse(actual, msg)

    def __getUserMessage(self, userMsg):
        if userMsg is None:
            userMsg = self.__getTestCaseName()
        return userMsg

    def __getTestCaseName(self):
        stack_level_of_calling_method = 3
        index_to_method_name = 3
        return inspect.stack()[stack_level_of_calling_method][index_to_method_name]
