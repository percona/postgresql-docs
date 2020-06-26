.. _minor-upgrade: 

********************************************************************************
Minor Upgrade of |pdp|
********************************************************************************

Minor releases of |postgresql| include bug fixes and feature enhancements. We recommend that you keep your |pdp| updated to the latest minor version.

Though minor upgrades do not change the behavior, we recommend you to back up your data first, in order to be on the safe side. 

Minor upgrade of |pdp| includes the following steps:

1. Stopping the ``postgresql`` cluster;
2. Installing new version packages;
3. Restarting the ``postgresql`` cluster.

.. note::

   These steps apply if you installed |pdp| from the Major Release repository. In this case, you are always upgraded to the latest available release.

   If you installed |pdp| from the Minor Release repository, you will need to enable a new version repository to upgrade. 

   For more information about |percona| repositories, refer to :ref:`pdp.installing`.

Before the upgrade, update the |percona-release| utility to the latest version. This is required to install the new version packages of |pdp|. Refer to `Percona Software Repositories Documentation <https://www.percona.com/doc/percona-repo-config/percona-release.html#updating-percona-release-to-the-latest-version>`_ for update instructions. 

.. important::

   Run all commands as root or via |sudo|.

1. Stop the ``postgresql`` service.

   * On Debian / Ubuntu:
   
     .. code-block:: bash
	   
	    $ sudo systemctl stop postgresql.service

   * On |RHEL| / |centos|:
	   
	 .. code-block:: bash
	         
	    $ sudo systemctl stop postgresql-11      

#. Install new version packages. See :ref:`pdp.installing`.

#. Restart the ``postgresql`` service.
   
   * On Debian / Ubuntu:
   
	 .. code-block:: bash
	   
	    $ sudo systemctl start postgresql.service

   * On |RHEL| / |centos|:
	   
	 .. code-block:: bash
	         
	    $ sudo systemctl start postgresql-11  

If you wish to upgrade |pdp| to the major version, refer to `Upgrading Percona Distribution for PostgreSQL from 11 to 12 <https://www.percona.com/doc/postgresql/12/major-upgrade.html>`_. 

.. include:: .res/replace.txt