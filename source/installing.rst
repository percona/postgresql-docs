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

Make sure to run |percona-release| as root or via |sudo|. For convenience, all
commands that require elevated priviges start with |sudo|.

.. code-block:: bash

   $ sudo percona-release enable experimental ppg-11

.. seealso::

   Documentation of |percona-release|
      https://www.percona.com/doc/percona-repo-config/percona-release.html

The next steps depend on the installation package format that your operating
system supports.

Using the |deb| Format
================================================================================

Start by updating the list of available packages. After this command completes,
the |percona-postgresql| package is ready to be installed.

.. code-block:: bash

   $ sudo apt update

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

.. important::

   If you intend to install |pdp| on |rhel| v8, disable the `postgresql` module:

   .. code-block:: bash

      $ dnf module disable postgresql

Next, install the |percona-platform-postgresql-11| using |yum-install|.

.. code-block:: bash

   $ sudo yum install percona-postgresql-11

.. admonition:: Supported platforms

   The following platforms are supported

   .. include:: .res/list.supported-platform.rpm.txt

.. include:: .res/replace.txt
