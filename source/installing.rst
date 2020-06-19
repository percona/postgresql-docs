.. _pdp.installing:

Installing |pdp|
********************************************************************************

Using repositories provided by |percona| is the recommended way of installing
|pdp|. 

There are two repositories available for |pdp|. We recommend to install |pdp|  from the *Major Release repository* (e.g. ``ppg-11``) as it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you're using have been tested and verified by |percona|. 

The *Minor Release repository* includes a particular minor release of the database and all of the packages that were tested and verified to work with that minor release (e.g. ``ppg-11.8``). You may choose to install |pdp| from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you'll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.

The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.

-------

Like many other |percona| products, |pdp| is installed from |Percona| repositories by using the |percona-release| utility.

.. important::

   Before you attempt to install |pdp|, update |percona-release| to
   its latest version. `See the documentation
   <https://www.percona.com/doc/percona-repo-config/percona-release.html#percona-release-update-latest-version>`_
   of |percona-release| for details.

As soon as |percona-release| is up-to-date, *set up* the
|pdp| product (``ppg-11`). 

.. code-block:: bash

   $ sudo percona-release setup ppg-11

.. hint::

   The command to set up a minor version product is the following:

   .. code-block:: bash
   
      $ sudo percona-release setup ppg-11.8
 
Install |pdp| using the commands of your package manager (the procedure differs
depending on the package manager of your operating system).

Using the |deb| Format
================================================================================

.. include:: .res/important.postgresql.uninstall.txt

The following platforms are supported:

.. include:: .res/list.supported-platform.deb.txt

.. admonition:: Platform Specific Notes

   On Debian 9 (stretch), you need to `enable the llvm repository
   <https://apt.llvm.org/>`_

Install the |percona-platform-postgresql-11| package using |apt-install|.

.. code-block:: bash

   $ sudo apt install percona-postgresql-11

Note that this package will not install the components. To install these
components use the appropriate packages:

.. code-block:: bash
   
   $ # To install pg_repack
   $ sudo apt-get install percona-postgresql-11-repack
   $ # To Install pgaudit
   $ sudo apt-get install percona-postgresql-11-pgaudit
   $ # To install pgBackRest
   $ sudo apt-get install percona-pgbackrest
   $ # To install Patroni
   $ sudo apt-get install percona-patroni
   $ # To install PostgreSQL contrib extensions
   $ sudo apt-get install percona-postgresql-contrib


Using the |rpm| Format
================================================================================
The following platforms are supported:

.. include:: .res/list.supported-platform.rpm.txt

.. admonition:: Platform Specific Notes

   If you intend to install |pdp| on |rhel| v8, disable the `postgresql` module:

   .. code-block:: bash

      $ sudo dnf module disable postgresql

   On |centos| 7, you should install the `epel-release` package:

   .. code-block:: bash

      $ sudo yum -y install epel-release
      $ sudo yum repolist

Install the |percona-platform-postgresql-11| package using |yum-install|.

.. code-block:: bash

   $ sudo yum install percona-postgresql11-server

Note that this package will not install the components. To install these
components use the appropriate packages:

.. code-block:: bash

   $ # To install pg_repack
   $ sudo yum install percona-pg_repack11
   $ # To Install pgaudit
   $ sudo yum install percona-pgaudit
   $ # To install pgBackRest
   $ sudo yum install percona-pgbackrest
   $ # To install Patroni
   $ sudo yum install percona-patroni
   $ # To install PostgreSQL contrib extensions
   $ sudo yum install percona-postgresql11-contrib

.. admonition:: Starting the service

   |pdp| is not automatically started after the installation. To start |pdp|, initialize the cluster using the following command:

   .. code-block:: bash

      /usr/pgsql-11/bin/postgresql-11-setup initdb

   Start the |postgresql| service:

   .. code-block:: bash

      $ sudo systemctl start postgresql-11 

.. include:: .res/replace.txt
