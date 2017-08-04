from .Test import TestCase
from . import ApprovalTests

from pprint import pformat

class ApprovalsTestCase(TestCase):
    Approvals = ApprovalTests.Approvals()

    def reprCalls(self, calls):
        '''
        Reformat mock.mock_calls deterministically
        '''
        return pformat([self.reprCall(c) for c in calls])

    def _format_call_signature(self, name, args, kwargs):
        message = '%s(%%s)' % name
        formatted_args = ''
        args_string = ', '.join([repr(arg) for arg in args])
        kwargs_string = ', '.join([
            '%s=%r' % (key, kwargs[key]) for key in sorted(kwargs.keys())
        ])
        if args_string:
            formatted_args = args_string
        if kwargs_string:
            if formatted_args:
                formatted_args += ', '
            formatted_args += kwargs_string

        return message % formatted_args

    def reprCall(self, call):
        if len(call) == 2:
            name = 'call'
            args, kwargs = call
        else:
            name, args, kwargs = call
            if not name:
                name = 'call'
            elif not name.startswith('()'):
                name = 'call.%s' % name
            else:
                name = 'call%s' % name
        return self._format_call_signature(name, args, kwargs)

    def verify(self,data):
        self.Approvals.verify(self,data)
