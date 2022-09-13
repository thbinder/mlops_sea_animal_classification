#!/usr/bin/env bash
set -e 

# un/comment this if you want to enable/disable multiple Python versions
PYTHON_VERSIONS="${PYTHON_VERSIONS-3.8 3.9 3.10}"

export SETUPTOOLS_USE_DISTUTILS=stdlib # Workaround to deal with this kind of issue: https://github.com/readthedocs/readthedocs.org/issues/8775

install_with_pipx() {
    if ! command -v "$1" &>/dev/null; then
        if ! command -v pipx &>/dev/null; then
            for python in python3.8 python3 python; do
                echo "Trying to install pipx with ${python}..."
                ${python} -m pip install --user pipx && break
                echo "pipx correctly installed."
            done
        fi
        echo "Trying to install "$1"..."
        pipx install "$1"
        echo ""$1" correctly installed."
    else
    echo ""$1" already installed."
    fi
}

install_with_pipx pdm

if [ -n "${PYTHON_VERSIONS}" ]; then
    for python_version in ${PYTHON_VERSIONS}; do
        if pdm use -f "${python_version}" &>/dev/null; then
            echo "> Using python ${python_version} environement"
            pdm install
        else
            echo "> pdm use -f ${python_version}: Python version not available?" >&2
        fi
    done
else
    pdm install
fi

echo "Setup done."
