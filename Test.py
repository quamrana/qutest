'''
Created on 8 Aug 2013

@author: andreww
'''
import unittest
import inspect

__unittest = True

# from os.path import basename, splitext

def skip(reason='Skip'):
    return unittest.skip(reason)

class parameterize:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, fn):
        def test_wrapped(*args, **kwargs):
            # print(self.kwargs)
            size = len(self.kwargs[list(self.kwargs.keys())[0]])
            #print(size)
            for index in range(size):
                d = {k: self.kwargs[k][index] for k in self.kwargs}
                #print(d)
                fn(*args, **d)

        return test_wrapped


class TestCase(unittest.TestCase):
    def shouldEqual(self, actual, expected, userMsg=None):
        userMsg = self.__getUserMessage(userMsg)
        msg = "%s should be %s" % (userMsg, expected)
        self.assertEqual(actual, expected, msg)

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
        # base = basename(inspect.stack()[0][1])
        # fname = splitext(base)[0]
        # cname = self.__class__.__name__
        # test_case_name = self.id().replace(".", "_")
        stack_level_of_calling_method = 3
        index_to_method_name = 3
        return inspect.stack()[stack_level_of_calling_method][index_to_method_name]
