.. _pdp.installing:

Installing |pdp|
********************************************************************************

Using repositories provided by |percona| is the recommended way of installing
|pdp|. Installation packages are available in the |rpm| format for Red Hat,
CentOS, and Amazon Linux AMI as well as in the |deb| format for |ubuntu| and
|debian| distributions). |pdp| is only available for the x86_64 platform (also
known as amd64).

Like many other |percona| products, |pdp| is installed by using the
|percona-release| utility.

.. important::

   Before you attempt to install |pdp|, reinstall |percona-release| to get its latest
   version. 

   .. seealso::

      Documentation of |percona-release|: Installation 
         https://www.percona.com/doc/percona-repo-config/percona-release.html

As soon as |percona-release| is ready, *set up* the |pdp| product (``ppg-11``).

.. code-block:: bash

   $ sudo percona-release setup ppg11

Make sure to run |percona-release| as root or via |sudo|. For the
sake of convenience, all commands that require elevated priviges start with
|sudo| in the following procedures.

.. hint::

   You can also make the packages related to |pdp| available by enabling the
   dedicated repository:

   .. code-block:: bash

      $ sudo percona-release enable ppg-11 release

Install |ppd| using the commands of your package manager (the precedure differs
depending on the package manager of your operating system).

Using the |deb| Format
================================================================================

.. include:: .res/important.postgresql.uninstall.txt

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

The following platforms are supported:

.. include:: .res/list.supported-platform.deb.txt

.. admonition:: Platform Specific Notes

   On Debian 9 (stretch), you need to `enable the llvm repository
   <https://apt.llvm.org/>`_

Using the |rpm| Format
================================================================================

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


.. include:: .res/replace.txt
