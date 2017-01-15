# -*- coding: utf-8 -*-
"""
Display the current window title.

Configuration parameters:
    cache_timeout: How often we refresh this module in seconds (default 0.5)
    format: display format for window_title (default '{title}')
    max_width: If width of title is greater, shrink it and add '...'
        (default 120)

Requires:
    i3-py: (https://github.com/ziberna/i3-py)
        `pip install i3-py`

If payload from server contains wierd utf-8
(for example one window have something bad in title) - the plugin will
give empty output UNTIL this window is closed.
I can't fix or workaround that in PLUGIN, problem is in i3-py library.

@author shadowprince
@license Eclipse Public License
"""

import i3


def find_focused(tree):
    if type(tree) == list:
        for el in tree:
            res = find_focused(el)
            if res:
                return res
    elif type(tree) == dict:
        if tree['focused']:
            return tree
        else:
            return find_focused(tree['nodes'] + tree['floating_nodes'])


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 0.5
    format = '{title}'
    max_width = 120

    def __init__(self):
        self.title = ''

    def window_title(self):
        window = find_focused(i3.get_tree())

        if not window or window.get('name') is None or window.get('type') == 'workspace':
            window = {'name': ''}

        transformed = False

        if window and 'name' in window and window['name'] != self.title:
            self.title = (len(window['name']) > self.max_width and
                          u"...{}".format(window['name'][-(self.max_width - 3):]) or
                          window['name'])
            transformed = True

        return {
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': self.py3.safe_format(self.format, {'title': self.title}),
            'transformed': transformed
        }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
