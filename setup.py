from distutils.core import setup
setup(
  name = 'toolsrequests',         # How you named your package folder (MyLib)
  packages = ['toolsrequests'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'requests helpers tools',   # Give a short description about your library
  author = 'Microsoft',                   # Type in your name
  author_email = 'Microsoft@aol.com',      # Type in your E-Mail
  download_url = 'https://github.com/gboacloth/toolsrequests/archive/refs/tags/tools2.tar.gz',    # I explain this later on
  install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4',
      ],
)
