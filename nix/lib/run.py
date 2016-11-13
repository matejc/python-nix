#!/usr/bin/env python3

from subprocess import Popen, PIPE, TimeoutExpired
from threading import Thread

import random
import json
import logging

log = logging.getLogger(__name__)


def uniqueid():
    random.seed()
    return '{0:0>6x}'.format(random.getrandbits(24))


def stderr_reader(identity, pipe):
    with pipe:
        for line in iter(pipe.readline, ''):
            line = line.rstrip()
            log.info('{0}-err> {1}'.format(identity, line))


def _run(identity, executable, args, inputText=None, timeout=600):
    with Popen(
        [executable] + args,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            bufsize=1) as p:
        try:
            log.info('{0}-run> {1} {2}'.format(identity, executable, ' '.join(
                args)))
            err_thread = Thread(
                target=stderr_reader, args=[identity, p.stderr])
            err_thread.start()
            if inputText:
                p.stdin.write(inputText)
                p.stdin.close()
            out_lines = []
            with p.stdout as pipe:
                for line in iter(pipe.readline, ''):
                    line = line.rstrip()
                    out_lines += [line]
                    log.info('{0}-out> {1}'.format(identity, line))
            p.wait(timeout=timeout)
            err_thread.join()
            log.info('{0}-returncode> {1}\n'.format(identity, p.returncode))
            return p.returncode, out_lines
        except TimeoutExpired as e:
            p.kill()
            raise e
        except Exception as e:
            raise e


def nixEnv(args):
    return _run(uniqueid(), 'nix-env', args)


def nixInstantiate(args, inputText=None):
    return _run(uniqueid(), 'nix-instantiate', args, inputText)


def nixBuild(args):
    return _run(uniqueid(), 'nix-build', args)
