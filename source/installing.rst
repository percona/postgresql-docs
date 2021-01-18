.. _pdp.installing:

Installing |pdp|
********************************************************************************

.. contents::
   :local:

This document provides installation instructions for |pdp| 11. For how to install one of the latest major versions of |pdp|, see the following guidelines:

- `Installing Percona Distribution for PostgreSQL 12 <https://www.percona.com/doc/postgresql/12/installing.html>`_ or 
- `Installing Percona Distribution for PostgreSQL 13 <https://www.percona.com/doc/postgresql/13/installing.html>`_.

Percona provides installation packages in ``DEB`` and ``RPM`` format for 64-bit Linux distributions. Find the full list of supported platforms on the `Percona Software and Platform Lifecycle page <https://www.percona.com/services/policies/percona-software-support-lifecycle#pgsql>`_.
     
Like many other |percona| products, we recommend installing |pdp| from Percona repositories by using the |percona-release| utility. The |percona-release| utility automatically enables the required repository for you so you can easily install and update |pdp| packages and their dependencies through the package manager of your operating system.

The installation process includes the following steps:

1. Install |percona-release|
2. Enable the repository
3. Install the packages
4. Start the ``postgresql`` service
5. Connect to the server

.. _repo-overview:

Repositories overview
=====================

There are two repositories available for |pdp|. We recommend installing |pdp|  from the *Major Release repository* (e.g. ``ppg-11``) as it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you're using have been tested and verified by |percona|. 

The *Minor Release repository* includes a particular minor release of the database and all the packages that were tested and verified to work with that minor release (e.g. ``ppg-11.8``). You may choose to install |pdp| from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you'll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.

The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.

.. _install-percona-release:

Install |percona-release|
==========================

Install |percona-release| utility. If you have installed it before, update it to the latest version. Refer to `Percona repositories documentation <https://www.percona.com/doc/percona-repo-config/percona-release.html>`_ for installation / update instructions.

.. _enable-repo:

Enable the repository
=====================

As soon as |percona-release| is installed or up-to-date, enable the repository for |pdp| (``ppg-11``). We recommend using the *set up* command as it enables the specified repository and updates the platform's package manager database. 

To install the *latest* version of |pdp|, enable the Major release repository using the following command: 

.. code-block:: bash

   $ sudo percona-release setup ppg-11

To install a *specific minor version* of |pdp|, enable the Minor release repository. For example, to install |pdp| 11.10, enable the ``ppg-11.10``  repository using the following command:

.. code-block:: bash
   
   $ sudo percona-release setup ppg-11.10
 
Install |pdp| packages 
=======================

After you've :ref:`installed percona-release <install-percona-release>` and :ref:`enabled the desired repository <enable-repo>`, install |pdp| using the commands of your package manager (the procedure differs
depending on the package manager of your operating system).

.. important::

   Run all the commands in the following sections as root or using the :command:`sudo` command.

On Debian and Ubuntu using ``apt``
------------------------------------

.. important::

   On Debian and other systems that use the ``apt`` package manager, such as Ubuntu,
   components of Percona Distribution for PostgreSQL 11 can only be installed
   together with the server shipped by Percona (percona-postgresql-11). If you
   wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL
   package provided by your distribution (postgresql-11) and then install the
   chosen components from Percona Distribution for PostgreSQL.

.. admonition:: Platform Specific Notes

   On Debian 9 (stretch), you need to `enable the llvm repository
   <https://apt.llvm.org/>`_

Install the |percona-platform-postgresql-11| package using the following command.

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-11

Note that this package will not install the components. Use the following commands to install components' packages:

Install ``pg_repack``:

.. code-block:: bash  

    $ sudo apt-get install percona-postgresql-11-repack

Install ``pgaudit``:

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-11-pgaudit

Install ``pgBackRest``:

.. code-block:: bash

   $ sudo apt-get install percona-pgbackrest

Install ``Patroni``:
 
.. code-block:: bash
   
   $ sudo apt-get install percona-patroni
   
Install ``pg_stat_monitor``:

.. code-block:: bash

   $ sudo apt-get install percona-pg-stat-monitor11

.. include:: .res/note-pg_stat_config-required.txt

Install PostgreSQL contrib extensions:

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-contrib

.. admonition:: Starting the service

   The installation process automatically initializes the default database. Thus, to start |pdp|, use the following command:

   .. code-block:: bash
   
      $ sudo pg_ctlcluster 11 main start

Next steps: :ref:`connect to PostgreSQL <server-connect>`.

On |rhel| and CentOS using ``yum``
----------------------------------------

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

Note that this package will not install the components. Use the following commands to install components' packages:

Install ``pg_repack``:

.. code-block:: bash

   $ sudo yum install percona-pg_repack11

Install ``pgaudit``:
   
.. code-block:: bash

   $ sudo yum install percona-pgaudit

Install ``pgBackRest``:
   
.. code-block:: bash

   $ sudo yum install percona-pgbackrest

Install ``Patroni``:
   
.. code-block:: bash

   $ sudo yum install percona-patroni

Install ``pg_stat_monitor``:

.. code-block:: bash

   $ sudo yum install percona-pg-stat-monitor11

.. include:: .res/note-pg_stat_config-required.txt

Install PostgreSQL contrib extensions:

.. code-block:: bash

   $ sudo yum install percona-postgresql11-contrib

.. admonition:: Starting the service

   After the installation, the default database storage is not automatically initialized. To complete the installation and start |pdp|, initialize the database using the following command:

   .. code-block:: bash

      /usr/pgsql-11/bin/postgresql-11-setup initdb

   Start the |postgresql| service:

   .. code-block:: bash

      $ sudo systemctl start postgresql-11 

.. _server-connect:

Connect to the PostgreSQL server
=================================

By default, ``postgres`` user and ``postgres`` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the ``postgres`` user. 

.. code-block:: bash

   $ sudo su postgres

Open the PostgreSQL interactive terminal:

.. code-block:: bash

   $ psql

.. hint:: 

   You can connect to ``psql`` as the ``postgres`` user in one go:

   .. code-block:: bash
   
      $ sudo su postgres psql

To exit the ``psql`` terminal, use the following command:

.. code-block:: bash 

   $ \q

.. include:: .res/replace.txt
