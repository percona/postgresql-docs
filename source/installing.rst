.. _pdp.installing:

Installing |pdp|
********************************************************************************

Using repositories provided by |percona| is the recommended way of installing
|pdp|. Installation packages are available in the |rpm| format for Red Hat,
CentOS, and Amazon Linux AMI as well as in the |deb| format for |ubuntu| and
|debian| distributions). |pdp| is only available for the x86_64 platform (also
known as amd64).

Like many other |percona| products, |pdp| is installed by using the
|percona-release| utility. As soon as it is ready, enable |pdp| and then install
using the commands of your package manager.

.. important::

   Before you attempt to install |pdp|, update |percona-release| to its latest
   version. For the steps described in this section to succeed,
   |percona-release| must be version 1.0.12 or later.

   .. seealso::

      Documentation of |percona-release|
         https://www.percona.com/doc/percona-repo-config/percona-release.html


Make sure to run |percona-release| as root or via |sudo|. For the sake of convenience, all
commands that require elevated priviges start with |sudo| in the following procedures.

.. code-block:: bash

   $ sudo percona-release enable ppg-11 experimental 

The next steps depend on the installation package format that your operating
system supports.

Using the |deb| Format
================================================================================

Start by updating the list of available packages. After this command completes,
the |percona-postgresql| package is ready to be installed.

.. code-block:: bash

   $ sudo apt update

.. admonition:: Platform Specific Notes

   On Debian 9 (stretch), you need to `enable the llvm repository
   <https://apt.llvm.org/>`_

Install the |percona-platform-postgresql-11| using |apt-install|.

.. code-block:: bash

   $ sudo apt install percona-postgresql-11

.. admonition:: Supported platforms

   The following platforms are supported

   .. include:: .res/list.supported-platform.deb.txt

.. include:: .res/list.supported-platform.deb.txt

Using the |rpm| Format
================================================================================

Start by updating the list of available packages. After this command completes,
the |percona-postgresql| package is ready to be installed.

.. code-block:: bash

   $ sudo yum update

.. admonition:: Platform Specific Notes

   If you intend to install |pdp| on |rhel| v8, disable the `postgresql` module:

   .. code-block:: bash

      $ sudo dnf module disable postgresql

   On |centos| 7, you should install the `epel-release` package:

   .. code-block:: bash

      $ sudo yum -y install epel-release
      $ sudo yum repolist

Next, install the |percona-platform-postgresql-11| using |yum-install|.

.. code-block:: bash

   $ sudo yum install percona-postgresql-11

.. admonition:: Supported platforms

   The following platforms are supported

   .. include:: .res/list.supported-platform.rpm.txt

.. include:: .res/replace.txt
