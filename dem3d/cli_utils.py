"""Copied from https://blender.stackexchange.com/a/134596 ."""

import argparse
import sys


class ArgumentParserForBlender(argparse.ArgumentParser):
    """ArgumentParser for the blender command line interface.

    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    >>> blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following calls work fine:
    >>> blender --python my_script.py -- -a 1 -b 2
    >>> blender --python my_script.py --
    """

    def _get_argv_after_doubledash(self):
        """Get the args after the double-dash ('--').

        Given the sys.argv as a list of strings, this method returns the
        sublist right after the '--' element (if present, otherwise returns
        an empty list).

        Returns
        -------
        list[str]
        """
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx + 1 :]  # the list after '--'
        except ValueError:  # '--' not in the list:
            return []

    def parse_args(self, *args, **kwargs):
        """Parse command line arguments.

        except that the sys.argv list will be pre-processed using
        _get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.

        Returns
        -------
        Namespace
        """
        return super().parse_args(args=self._get_argv_after_doubledash(), **kwargs)
