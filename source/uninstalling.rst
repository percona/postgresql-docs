.. _pdp.uninstalling:

Uninstalling |pdp|
********************************************************************************

To uninstall |pdp|, remove all the installed packages and data / configuration files. 

.. note::

   Should you need the data files later, back up your data before uninstalling |pdp|.


Using the |deb| format
================================================================================
  
.. warning::

   On Debian 10, deletion of only main |percona-postgresql| packages is not supported. To avoid an error, delete both the main packages and the components.  

To uninstall |pdp| on platforms that use |apt| package manager such as Debian
or Ubuntu, follow these steps.

Run all commands as root or via |sudo|.

1. Stop the |postgresql| service.

   .. code-block:: bash

      $ sudo systemctl stop postgresql.service

#. Remove the |percona-postgresql| packages.

   .. code-block:: bash

      $ sudo apt-get remove percona-postgresql-11* percona-pgbackrest percona-patroni
 
#. Remove configuration and data files.         

   .. code-block:: bash

      $ rm -rf /etc/postgresql/11/main

Using the |rpm| format
================================================================================

To uninstall |pdp| on platforms that use |yum| package manager such as 
|rhel| or |centos|, follow these steps.

Run all commands as root or via |sudo|.

1. Stop the |pdp| service.

   .. code-block:: bash

      $ sudo systemctl stop postgresql-11

#. Remove the |percona-postgresql| packages

   .. code-block:: bash
 
      $ sudo yum remove percona-postgresql11*

#. Remove configuration and data files

   .. code-block:: bash

      $ rm -rf /var/lib/pgsql/11/data    



.. include:: .res/replace.txt 