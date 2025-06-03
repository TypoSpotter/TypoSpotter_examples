#!/bin/bash

# This should be run by a Google Cloud VM to install everything needed to run OpenRadioss (including MUMPS)
# Developed for e2-micro with x86/64 architecture running Ubuntu 24.04.2 LTS

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential gfortran cmake perl
sudo apt-get install python3 python-is-python3 git-lfs

# Install Open MPI
# OpenMPI from the Ubuntu repo seems to work fine
sudo apt-get install openmpi-common openmpi-bin
# This is the process to download, configure, make and install according to guide:
# https://github.com/orgs/OpenRadioss/discussions/2117
#wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.0.tar.gz
#tar -xvzf openmpi-5.0.0.tar.gz
#cd openmpi-5.0.0
#./configure --prefix=/opt/openmpi
#make
#sudo make install

# Download OpenRadioss
wget https://github.com/OpenRadioss/OpenRadioss/archive/refs/tags/latest-20250522.tar.gz
tar -xvzf latest-20250522.tar.gz
cd OpenRadioss-latest-20250522

# Download mumps
mkdir extlib
cd extlib
mkdir mumps
cd mumps
# Download LAPACK, ScaLAPACK and MUMPS
# Untar downloads
