from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='strawberry_venn_generator',
      version='0.2',
      description='A venn diagram generator that creates an image.',
      long_description=readme(),
      #url='http://github.com/Tabea-K',
      author='Tabea Kischka',
      author_email='tabea.kischka@gmail.com',
      license='MIT',
      packages=['strawberry_venn_generator'],
      test_suite='nose.collector',
      tests_require=['nose'],
      package_data={'strawberry_venn_generator': ['img/empty_venn.svg',
                                                  'README.rst',
                                                  'tests/test_files/file1.txt',
                                                  'tests/test_files/file2.txt',
                                                  'tests/test_files/file3.txt',
                                                  'tests/test_files/correct_venn_diagram.svg']},
      include_package_data=True,
      entry_points={
          'console_scripts': ['strawberry-venn-generator=strawberry_venn_generator.venn_generator:main'],
      },
      zip_safe=False)
