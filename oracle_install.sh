# Installing Oracle Instant Client on Ubuntu
# September 05, 2019
# Now that Oracle has enabled us to download instant client without any click through for accepting the license, I wanted to revisit a seamless install of the instant client on a new set up.

# Ubuntu has the documentation about installing the instant client here: https://help.ubuntu.com/community/Oracle%20Instant%20Client.

# First - because Oracle provides their releases in RPM archive format (or a tarball), in order to have an installer you need to create a DEB archive. There is a package in the archives, alien, which aids this process.

# This gives the start of the script:

#!/bin/bash
# Install dependencies
sudo apt install alien


# The 3 packages the Ubuntu documentation tells us to retrieve are:

# - devel
# - basic (I opt for basiclite instead)
# - sqlplus

# So, over at the downloads page: https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html we can grab the link.

# Download files. Example specific to 19.3 
# Some links were not correct on the downloads page
# (still pointing to a license page), but easy enough to
# figure out from working ones 
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-basiclite-19.3.0.0.0-1.x86_64.rpm
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-devel-19.3.0.0.0-1.x86_64.rpm
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm

Next, install the RPM's using alien

sudo alien -i oracle-instantclient19.3-*.rpm

sqlplus will more than likely require libaio package, so install that dependency

sudo apt install libaio1

Set the environment up:

# Create Oracle environment script
sudo -s

printf "\n\n# Oracle Client environment\n \
export LD_LIBRARY_PATH=/usr/lib/oracle/19.3/client64/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export ORACLE_HOME=/usr/lib/oracle/19.3/client64\n" > /etc/profile.d/oracle-env.sh

exit

So, just to have that in the full script, it should look like:

#!/bin/bash
printf "Automated installer of oracle client for Ubuntu" 
# Install dependencies
sudo apt updatesudo apt install -y alien

# Download files. Example specific to 19.3 
# Some links were not correct on the downloads page
# (still pointing to a license page), but easy enough to
# figure out from working ones 
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-basiclite-19.3.0.0.0-1.x86_64.rpm
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-devel-19.3.0.0.0-1.x86_64.rpm
wget https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm 

# Install all 3 RPM's downloaded 
sudo alien -i oracle-instantclient19.3-*.rpm

# Install SQL*Plus dependency  
sudo apt install -y libaio1

# Create Oracle environment script
printf "\n\n# Oracle Client environment\n \
export LD_LIBRARY_PATH=/usr/lib/oracle/19.3/client64/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export ORACLE_HOME=/usr/lib/oracle/19.3/client64\n" | sudo tee /etc/profile.d/oracle-env.sh > /dev/null

. /etc/profile.d/oracle-env.sh

printf "Install complete. Please verify"

Finally,

We verify we're all set up by launching sqlplus

sqlplus /nolog
