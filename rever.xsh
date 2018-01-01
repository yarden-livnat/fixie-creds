$PROJECT = $GITHUB_REPO = 'fixie-creds'
$GITHUB_ORG = 'ergs'

$ACTIVITIES = ['pytest', 'version_bump', 'changelog', 'tag', 'push_tag', 'pypi', 'ghrelease']

$VERSION_BUMP_PATTERNS = [
    ('setup.py', 'VERSION\s*=.*', "VERSION = '$VERSION'"),
    ('fixie_creds/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'

$DOCKER_CONDA_DEPS = ['xonsh', 'cerberus', 'pytest', 'tornado', 'pytest-tornado', 'pip']
$DOCKER_INSTALL_COMMAND = 'git clean -fdx && pip install fixie && ./setup.py install'
