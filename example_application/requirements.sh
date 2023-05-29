#!/bin/bash

# List of required packages
required_packages=(
    flask
    requests
    matplotlib
    numpy
    pycrypto
)

# Check if a package is installed
package_installed() {
    if pip3 show "$1" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Install a package
install_package() {
    if pip3 install "$1"; then
        echo "Installed $1"
    else
        echo "Failed to install $1"
    fi
}

# Check and install required packages
for package in "${required_packages[@]}"; do
    if ! package_installed "$package"; then
        echo "$package is not installed. Installing..."
        install_package "$package"
    else
        echo "$package is already installed."
    fi
done
