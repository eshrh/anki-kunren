import setuptools
import os
with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
      name='anki-kunren',
      version='1.3.0',
      description='Anki practice tool to drill japanese kanji stroke order and practice writing.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      package_data={
          'anki_kunren': ['data/*.svg'],
      },
      python_requires='>=3.7',
      install_requires=['pygame','svg.path'],
      author='esrh',
      author_email='esrh@netc.eu',
      keywords='japanese anki kanji stroke order writing',
      url='https://github.com/eshrh/anki-kunren',
      entry_points={'console_scripts': ['kunren=anki_kunren.kunren:main']}
     )
