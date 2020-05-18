import setuptools

from eso_addon_manager import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="anonymous person", # Replace with your own username
    version=__version__,
    description="Manage your ESO add ons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'eso_addons = eso_addon_manager.main:cli_main',
            'eso_addons_gui = eso_addon_manager.main:gui_main'
        ],
    },
    install_requires=[
        'pyyaml',
        'requests',
        'colorama',
        'pyqt5',
        'qdarkstyle',
        'qtpy',
        'pyinstaller'
    ]
)