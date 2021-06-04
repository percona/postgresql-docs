.. _pdp.installing:

Installing |pdp|
********************************************************************************

.. contents::
   :local:

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
======================

There are two repositories available for |pdp|. We recommend installing |pdp|  from the *Major Release repository* (e.g. ``ppg-13``) as it includes the latest version packages. Whenever a package is updated, the package manager of your operating system detects that and prompts you to update. As long as you update all Distribution packages at the same time, you can ensure that the packages you're using have been tested and verified by |percona|.

The *Minor Release repository* includes a particular minor release of the database and all of the packages that were tested and verified to work with that minor release (e.g. ``ppg-13.1``). You may choose to install |pdp| from the Minor Release repository if you have decided to standardize on a particular release which has passed rigorous testing procedures and which has been verified to work with your applications. This allows you to deploy to a new host and ensure that you'll be using the same version of all the Distribution packages, even if newer releases exist in other repositories.

The disadvantage of using a Minor Release repository is that you are locked in this particular release. When potentially critical fixes are released in a later minor version of the database, you will not be prompted for an upgrade by the package manager of your operating system. You would need to change the configured repository in order to install the upgrade.

.. _install-percona-release:

Install |percona-release|
===========================
Install |percona-release| utility. If you have installed it before, update it to the latest version. Refer to `Percona repositories documentation <https://www.percona.com/doc/percona-repo-config/percona-release.html>`_ for installation / update instructions.

.. _enable-repo:

Enable the repository
=====================

As soon as |percona-release| is installed or up-to-date, enable the repository for |pdp| (``ppg-13``). We recommend using the *set up* command as it enables the specified repository and updates the platform's package manager database.

To install the *latest* version of |pdp|, enable the Major Release repository using the following command:

.. code-block:: bash

   $ sudo percona-release setup ppg-13

To install a *specific minor version* of |pdp|, enable the Minor release repository. For example, to install |pdp| 13.1, enable the ``ppg-13.1``  repository using the following command:

.. code-block:: bash

   $ sudo percona-release setup ppg-13.1

Install |pdp| packages
======================

After you've :ref:`installed percona-release <install-percona-release>` and :ref:`enabled the desired repository <enable-repo>`, install |pdp| using the commands of your package manager (the procedure differs
depending on the package manager of your operating system).

On Debian and Ubuntu using ``apt``
------------------------------------

.. note::

   On Debian and other systems that use the ``apt`` package manager, such as Ubuntu,
   components of Percona Distribution for PostgreSQL 13 can only be installed
   together with the server shipped by Percona (percona-postgresql-13). If you
   wish to use Percona Distribution for PostgreSQL, uninstall the PostgreSQL
   package provided by your distribution (postgresql-13) and then install the
   chosen components from Percona Distribution for PostgreSQL.

.. note:: Platform Specific Notes

   On Debian 9 (stretch), you need to `enable the llvm repository
   <https://apt.llvm.org/>`_

Install the |percona-platform-postgresql-13| package using |apt-get-install|.

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-13

Note that this package will not install the components. Use the following commands to install components' packages:

Install ``pg_repack``:

.. code-block:: bash

    $ sudo apt-get install percona-postgresql-13-repack

Install ``pgAudit``:

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-13-pgaudit

Install ``pgBackRest``:

.. code-block:: bash

   $ sudo apt-get install percona-pgbackrest

Install ``Patroni``:

.. code-block:: bash

   $ sudo apt-get install percona-patroni

Install ``pg_stat_monitor``:

.. code-block:: bash

   $ sudo apt-get install percona-pg-stat-monitor13

.. include:: .res/note-pg_stat_config-required.txt

Install ``PgBouncer``:

.. code-block:: bash

   $ sudo apt-get install percona-pgbouncer

Install ``pgAudit-set_user``:

.. code-block:: bash
 
   $ sudo apt-get install percona-pgaudit13-set-user

Install ``pgBadger``:

.. code-block:: bash

   $ sudo apt-get install percona-pgbadger

Install ``wal2json``:

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-13-wal2json

Install PostgreSQL contrib extensions:

.. code-block:: bash

   $ sudo apt-get install percona-postgresql-contrib


.. admonition:: Starting the service

   The installation process automatically initializes the default database. Thus, to start |pdp|, use the following command:

   .. code-block:: bash

      $ sudo pg_ctlcluster 13 main start

Next steps: :ref:`connect to PostgreSQL <server-connect>`.

On |rhel| and CentOS using ``yum``
----------------------------------------

.. note:: Platform Specific Notes

   If you intend to install |pdp| on |rhel| v8, disable the `postgresql` module:

   .. code-block:: bash

      $ sudo dnf module disable postgresql

   On |centos| 7, you should install the `epel-release` package:

   .. code-block:: bash

      $ sudo yum -y install epel-release
      $ sudo yum repolist

Install the |percona-platform-postgresql-13| package using |yum-install|.

.. code-block:: bash

   $ sudo yum install percona-postgresql13-server

Note that this package will not install the components. Use the following commands to install components' packages:

Install ``pg_repack``:

.. code-block:: bash

   $ sudo yum install percona-pg_repack13

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

   $ sudo yum install percona-pg-stat-monitor13

.. include:: .res/note-pg_stat_config-required.txt

Install ``PgBouncer``:

.. code-block:: bash

   $ sudo yum install percona-pgbouncer

Install ``pgAudit-set_user``:

.. code-block:: bash
 
   $ sudo yum install percona-pgaudit13_set_user

Install ``pgBadger``:

.. code-block:: bash

   $ sudo yum install percona-pgbadger

Install ``wal2json``:

.. code-block:: bash

   $ sudo yum install percona-wal2json13

Install PostgreSQL contrib extensions:

.. code-block:: bash

   $ sudo yum install percona-postgresql13-contrib


Some extensions require additional setup in order to use them with |pdp|. For more information, refer to :ref:`enabling`.

.. admonition:: Starting the service


   After the installation, the default database storage is not automatically initialized. To complete the installation and start |pdp|, initialize the database using the following command:

   .. code-block:: bash

      /usr/pgsql-13/bin/postgresql-13-setup initdb

   Start the |postgresql| service:

   .. code-block:: bash

      $ sudo systemctl start postgresql-13

.. _enabling:

Enabling extensions
-------------------

Some extensions require additional configuration before using them with |pdp|. This sections provides configuration instructions per extension.

**pgBadger**

Enable the following options in `postgresql.conf` configuration file before starting the service:

.. code-block:: guess

   log_min_duration_statement = 0
   log_line_prefix = '%t [%p]: '
   log_checkpoints = on
   log_connections = on
   log_disconnections = on
   log_lock_waits = on
   log_temp_files = 0
   log_autovacuum_min_duration = 0
   log_error_verbosity = default

For details about each option, see `pdBadger documentation <https://github.com/darold/pgbadger/#POSTGRESQL-CONFIGURATION>`_.

**pgAudit set-user**

Add the ``set-user`` to ``shared_preload_libraries`` in postgresql.conf. The recommended way is to  use the `ALTER SYSTEM <https://www.postgresql.org/docs/13/sql-altersystem.html>`_ command. :ref:`Connect to psql <server-connect>` and use the following command:

.. code-block:: bash

      $ ALTER SYSTEM SET shared_preload_libraries = 'set-user';

Start/restart the server to apply the configuration.

You can fine-tune user behavior with the `custom parameters <https://github.com/pgaudit/set_user#configuration-options>`_ supplied with the extension.

**wal2json**

After the installation, enable the following option in :file:`postgresql.conf` configuration file before starting the service:

.. code-block:: guess

   wal_level = logical

.. _server-connect:

Connect to the PostgreSQL server
=================================

By default, ``postgres`` user and ``postgres`` database are created in PostgreSQL upon its installation and initialization. This allows you to connect to the database as the ``postgres`` user.

.. code-block:: bash

   $ sudo su postgres

Open the PostgreSQL interactive terminal:

.. code-block:: bash

   $ psql

.. note::

   You can connect to ``psql`` as the ``postgres`` user in one go:

   .. code-block:: bash

      $ sudo su postgres psql

To exit the ``psql`` terminal, use the following command:

.. code-block:: bash

   $ \q


.. include:: .res/replace.txt
