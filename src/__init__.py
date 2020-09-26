import os
import subprocess
from datetime import date


def get_version(module):
    version = date.today().strftime('%Y-%m')
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).rstrip().decode('utf8')
        git_describe = subprocess.check_output(["git", "describe", "--long"]).rstrip().decode('utf8')
        git_tag = git_describe.split('-')[0]
        git_commits = git_describe.split('-')[1]
        if branch == 'master':
            sep = '.'
        else:
            sep = 'dev'
        print(branch, git_tag, sep, git_commits)
        version = '{}{}{}'.format(git_tag, sep, git_commits)
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open('{}/__init__.py'.format(module), 'w')
        fp.write('__version__ = [{}, {}, "{}"]'.format(git_tag.replace('.', ','), git_commits, sep.replace('.', '')))
        fp.close()
    except Exception:
        print('ERROR opening {}/__init__.py'.format(module), os.curdir)
    return version
