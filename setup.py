from setuptools import setup, find_packages

setup(
        name="mide",
        version="0.1",
        packages=find_packages(),
        install_requires=['dask==2.14.0',
            'dask-image==0.2.0',
            'h5py==2.10.0',
            'imageio==2.8.0',
            'imagesize==1.2.0',
            'ipykernel==5.1.4',
            'ipython==7.13.0',
            'ipython-genutils==0.2.0',
            'jupyter-client==5.3.4',
            'jupyter-core==4.6.3',
            'matplotlib==3.1.3',
            'napari==0.2.12',
            'numpy==1.16.2',
            'numpydoc==0.9.2',
            'pandas==0.24.2',
            'pickleshare==0.7.5',
            'Pillow==7.0.0',
            'pyqtgraph==0.10.0',
            'qtconsole==4.7.1',
            'QtPy==1.9.0',
            'scikit-image==0.16.2',
            'scikit-learn==0.20.3',
            'scipy==1.2.1',
            'vispy==0.6.4'
            ],
)
