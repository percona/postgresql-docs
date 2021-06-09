# Percona Distribution for PostgreSQL 11.12 Update


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">June 10, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/11/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table>

This update of Percona Distribution for PostgreSQL includes the following fixes for Red Hat Enterprise Linux 8 / CentOS 8:

- ``llvm`` packages are added to the repository. This fixes compatibility issues with LLVM from upstream. To use ``llvm`` packages supplied by us, disable the upstream ``llvm-toolset`` module before the installation:

```
sudo dnf module disable llvm-toolset
```

- systemd unit file includes the correct path to Patroni configuration file. 
- ``etcd`` and ``python3-python-etcd`` packages are added as ``RPM`` packages to Percona Distribution for PostgreSQL for Red Hat Enterprise Linux / CentOS 8. These packages are used to set up High Availability clusters with Patroni.  For how to set up Patroni clusters, see [Patroni documentation](https://patroni.readthedocs.io/en/latest/README.html#running-configuring) 
