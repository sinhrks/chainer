if [ ${TRAVIS_OS_NAME} == "osx" ]; then
    brew tap homebrew/science
    brew install hdf5
    if [ ${PYTHON_VER} == "2.7" ]; then
        wget -O conda.sh https://repo.continuum.io/miniconda/Miniconda-latest-MacOSX-x86_64.sh
    else
        wget -O conda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    fi
else
    sudo apt-get install libhdf5-serial-dev
    if [ ${PYTHON_VER} == "2.7" ]; then
        wget -O conda.sh https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
    else
        wget -O conda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    fi
fi
bash conda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
# Useful for debugging any issues with conda
conda info -a

conda create -n myenv python=${PYTHON_VER}

source activate myenv
conda install numpy cython h5py
python --version
python setup.py install
pip install nose flake8 hacking
nosetests -a '!gpu' tests/chainer_tests || exit -1
flake8 || exit -1