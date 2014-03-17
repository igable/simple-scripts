#!/usr/bin/env sh

#
# This script recursively downloads the perfSonar wlcg configuration file
#
# Author: Ian Gable <igable@uvic.ca>
#
# The top level directory where the downloaded files will be put.
# Note that the whole directory structure will be created but only
# those files below the URL will actually be downloaded.
#  
OUTPUTDIR=/var/www/html/psmirror

# URL to mirror
PSURL=https://grid-deployment.web.cern.ch/grid-deployment/wlcg-ops/perfsonar/conf/central/

cd ${OUTPUTDIR}
wget --recursive -e robots=off --no-parent --no-host-directories --reject "index.html*" ${PSURL}
