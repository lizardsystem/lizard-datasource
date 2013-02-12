from setuptools import setup

version = '0.5.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'lizard-map >= 4.0a1',
    'lizard-ui >= 4.0a1',
    'lizard-security',
    'django-nose',
    'setuptools',
    'mock',
    'south',
    'pandas',
    'django-colorful',
    'factory_boy'
    ],

tests_require = [
    ]

setup(name='lizard-datasource',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='Remco Gerlich',
      author_email='remco.gerlich@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_datasource'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ],
          'lizard_datasource': [
            'dummy_datasource = lizard_datasource.dummy_datasource:factory',
       'augmented_datasource = lizard_datasource.augmented_datasource:factory',
            ],
          }
      )
