# System imports
import os
from os.path import join

# 3rd party libs
from nose.tools import *
from git import *

# PyGitup imports
from PyGitUp.git_wrapper import GitError
from tests import basepath, write_file, init_master, capture

test_name = 'fetch-all'
testfile_name = 'file'

repo_path = join(basepath, test_name + os.sep)


def setup():
    master_path, master = init_master(test_name)
    master_path2, master2 = init_master(test_name + '2')

    # Prepare master repo
    master.git.checkout(b=test_name)

    # Clone to test repo
    path = join(basepath, test_name)

    master.clone(path, b=test_name)
    repo = Repo(path, odbt=GitCmdObjectDB)

    assert repo.working_dir == path

    # Configure git up
    repo.git.config('git-up.fetch.all', 'true')

    # Add second master repo to remotes
    repo.git.remote('add', test_name, master_path2)


def test_ahead_of_upstream():
    """ Run 'git up' with result: ahead of upstream """
    os.chdir(repo_path)

    from PyGitUp.gitup import GitUp
    gitup = GitUp()

    with capture() as [stdout, stderr]:
        gitup.run(testing=True)

    stdout = stdout.getvalue()

    assert_true('origin' in stdout)
    assert_true(test_name in stdout)
