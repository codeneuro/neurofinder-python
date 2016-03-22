import os

def init(force):
    """
    This command initializes a folder with the typical contents of a Python package.
    After running this and writing your code, you should be ready to publish your package.
    """
    echo('\nThis utility will help you set up a new python module for publishing on PyPi!\n')
    echo('After answering a few questions, it will create a few files.')
    echo('\nPress ^C at any time to bail!\n')

    remap = {
        'entry': 'entry point',
        'package': 'package name'
    }
    d = _defaults()
    for k, v in d.items():
        d[k] = prompt.query('%s:' % remap.get(k, k), default=v)

    echo('\nReady to create the following files:')

    with indent(4, quote='  -'):
        puts('setup.py')
        puts('setup.cfg')
        puts('MANIFEST.in')
        puts(d['package'] + '/' + '__init__.py')
        puts(d['package'] + '/' + d['entry'])
        puts('requirements.txt')

    finalize = prompt.yn('\nSound like a plan?', default='y')

    if finalize:
        echo('')
        _make_package(d, force)
        echo('')

    success('Your package is initialized!')
