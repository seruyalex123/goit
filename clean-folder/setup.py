from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version= '0.0.1',
    description='program which sorte your folders for suff_files',
    author='Oleksandr Soryi',
    author_email='seruyalex@gmail.com',
    url='https://github.com/seruyalex123/goit/blob/main/dz_sort_goit.py',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    packages=find_namespace_packages(),
    entry_points={'console_skripts': [
        'startgame=clean_folder.clean:sort_func']}
)