# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re
import time
import shutil
import fnmatch

import pyminifier.minification as minification


BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
SOURCE_DIR = os.path.normpath(os.path.join(BASE_DIR, 'backend'))
TARGET_CLEAN_DIR = os.path.join(BASE_DIR, 'compiler', 'clean')


def run():
    shutil.rmtree(TARGET_CLEAN_DIR)
    time.sleep(0)
    os.makedirs(TARGET_CLEAN_DIR)

    for root, dirnames, filenames in os.walk(SOURCE_DIR):
        for filename in fnmatch.filter(filenames, '*.py'):
            pathname = os.path.normpath(os.path.join(root, filename))

            head, tail = os.path.split(pathname)
            parent = head.replace(SOURCE_DIR, '')
            if parent.startswith('\\'):
                parent = parent[1:]

            if parent == 'scripts':
                continue
            elif parent == 'settings' and filename == 'player.py':
                continue
            else:
                targetDirectory = os.path.join(TARGET_CLEAN_DIR, parent)
                try:
                    os.makedirs(targetDirectory)
                except OSError:
                    pass

                with open(pathname, 'rb') as fp:
                    script = fp.read()

                if parent == 'identifier' and filename == '__init__.py':
                    key = re.search(r"THEMOVIEDB_API_KEY = '([^']+)'", script).groups()[0].encode('rot13')
                    param = 'api_key'.encode('rot13')
                    algo = "(str(255-0xe0)+'tor')[::-1]"
                    script = re.compile(r"'api_key': THEMOVIEDB_API_KEY").sub("'%s'.decode(%s): '%s'.decode(%s)" % (param, algo, key, algo), script)
                    script = re.compile(r"THEMOVIEDB_API_KEY = '([^']+)'").sub('', script)

                if script.find("'User-Agent': ENTROPY_SEED") != -1:
                    param = 'User-Agent'.encode('rot13')
                    algo = "(str(255-0xe0)+'tor')[::-1]"
                    script = re.compile(r"'User-Agent': ENTROPY_SEED").sub("'%s'.decode(%s): ENTROPY_SEED" % (param, algo), script)

                script = re.compile(r'from settings import DEBUG').sub('', script)
                script = re.compile(r'if DEBUG:.*?# END if DEBUG', re.M | re.DOTALL).sub('', script)
                script = re.compile(r'if (True|False): # DEBUG.*?# END if DEBUG', re.M | re.DOTALL).sub('', script)
                script = re.compile(r'if DEBUG and .*?# END if DEBUG', re.M | re.DOTALL).sub('', script)
                script = re.compile(r'if DEBUG or ').sub('if ', script)
                script = re.compile(r'return DEBUG or ').sub('return ', script)
                script = re.compile(r'(debug=DEBUG)').sub('()', script)
                script = re.compile(r' and not DEBUG').sub('', script)
                script = re.compile(r'DEBUG = (True|False)').sub('', script)

                script = minification.remove_comments_and_docstrings(script)

                script = script.strip()

                script = re.compile(r"__author__ = '[^']+'").sub('', script)
                script = re.compile(r"__copyright__ = '[^']+'").sub('', script)

                script = script.strip()

                script = minification.remove_blank_lines(script)

                script = script.strip()


                script = minification.dedent(script, use_tabs=False)

                script = script.strip()

                if parent == 'updater':
                    script = '# coding: iso-8859-1\n' + script
                else:
                    script = '# coding: utf-8\n' + script

                with open(os.path.join(TARGET_CLEAN_DIR, parent, filename), 'wb') as fp:
                    fp.write(script)


if __name__ == '__main__':
    run()
