import os
from invoke import task
from sys import platform

def islinux():
    if platform == 'linux' or platform == 'linux2':
        return True

@task
def clean(ctx):
    # for item in os.listdir('dist'):
    #     os.remove(os.path.join('dist', item))
    import shutil
    shutil.rmtree('qbtrade.egg-info', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('.pytest_cache', ignore_errors=True)
    os.makedirs('dist', exist_ok=True)
    if islinux():
        cmd = "find . -name '*.pyc' -exec rm {} \\;"
        ctx.run(cmd)


@task(pre=[clean])
def build(ctx):
    ctx.run('python setup.py sdist bdist_wheel && cd dist')
    for item in os.listdir('dist'):
        if item.endswith('.whl'):
            cmd = f'cd dist && pip install {item}'
            print(cmd)
            ctx.run(cmd)