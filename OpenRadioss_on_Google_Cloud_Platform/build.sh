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
# Let's try LAPACK and ScaLAPACK from repo
#sudo apt-get install liblapack-dev
#sudo apt-get install libscalapack-dev
# Let's try MUMPS from repo
sudo apt-get install libmumps-ptscotch-dev
# Untar downloads
#wget https://github.com/Reference-LAPACK/lapack/archive/refs/tags/v3.11.0.tar.gz
#wget https://github.com/Reference-ScaLAPACK/scalapack/archive/refs/tags/v2.2.0.tar.gz
#wget http://ftp.mcs.anl.gov/pub/petsc/externalpackages/MUMPS_5.5.1.tar.gz
#tar -xvzf v2.2.0.tar.gz 
#tar -xvzf v3.11.0.tar.gz
#tar -xvzf MUMPS_5.5.1.tar.gz

# Make LAPACK
#cd lapack-3.11.0
#mv make.inc.example make.inc
#make

# Make SCALAPACK
#cd $HOME/OpenRadioss/extlib/mumps
#cd scalapack-2.2.0
#cp SLmake.inc.example SLmake.inc


# Modify the following lines in SLmake.inc:
#line 29 and 30,31,32
#FC = /opt/openmpi/bin/mpif90
#CC = /opt/openmpi/bin/mpicc
#NOOPT         = -O0 -fallow-argument-mismatch
#FCFLAGS       = -O3 -fallow-argument-mismatch

#line 57 and 58
#BLASLIB       = ~/OpenRadioss/extlib/mumps/lapack-3.11.0/librefblas.a
#LAPACKLIB     = ~/OpenRadioss/extlib/mumps/lapack-3.11.0/liblapack.a

#make

## Make MUMPS:
#cd $HOME/OpenRadioss/extlib/mumps
#cd MUMPS_5.5.1
#cp Make.inc/Makefile.debian.PAR Makefile.inc

# Modify lines in Makefile.inc to the following:
#line 31 
#ORDERINGSF  = -Dpord

#line 34 36
#LORDERINGS = $(LPORD)
#IORDERINGSC = $(IPORD)

#line 50 51 52
#CC = /opt/openmpi/bin/mpicc
#FC = /opt/openmpi/bin/mpif90
#FL = /opt/openmpi/bin/mpif90

#line 55 56
#LAPACK = ~/OpenRadioss/extlib/mumps/lapack-3.11.0/liblapack.a
#SCALAP = ~/OpenRadioss/extlib/mumps/scalapack-2.2.0/libscalapack.a

#line 65
#LIBBLAS = ~/OpenRadioss/extlib/mumps/lapack-3.11.0/librefblas.a

#line 72
#OPTF    = -O -fopenmp -fallow-argument-mismatch

#make

# Modify lines in /CMake_Compilers/cmake_linux64_gf.txt to the following

#Remove -Dmentis flag(line 90)
#set(mumps_flag "-Dpord -Dthr_all -DMUMPS5 -DAdd_")
 
#add -fallow-argument-mismatch (line 138)
#set ( opt_flag "  ${wo_linalg} -DCOMP_GFORTRAN=1 -ffp-contract=off -frounding-math -fopenmp -fallow-argument-mismatch " )

#Change -Werror=array-bounds to -Warray-bounds line146
#set( strict " -Werror=aliasing -Werror=unused-dummy-argument -Werror=do-subscript -Warray-bounds -Werror=tabs -Werror=surprising ")

sed -e 's/-Dmetis //;s/-frounding-math \$[{]OPENMP[}]/-frounding-math \${OPENMP} -fallow-argument-mismatch/;s///' < cmake_linux64_gf.txt > cmake_linux64_gf.txt.tmp
