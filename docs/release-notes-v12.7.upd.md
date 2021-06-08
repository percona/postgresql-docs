# Percona Distribution for PostgreSQL 12.7


<table class="docutils field-list" frame="void" rules="none">
  <colgroup>
    <col class="field-name">
    <col class="field-body">
  </colgroup>
  <tbody valign="top">
    <tr class="field-odd field">
      <th class="field-name">Date:</th>
      <td class="field-body">June 09, 2021</td>
    </tr>
    <tr class="field-even field">
      <th class="field-name">Installation:</th>
      <td class="field-body">
        <a class="reference external" href="https://www.percona.com/doc/postgresql/12/installing.html#">Installing Percona Distribution for PostgreSQL</a></td>
    </tr>
  </tbody>
</table>


This update of Percona Distribution for PostgreSQL includes the following fixes for Red Hat Enterprise Linux 8 / CentOS 8:

- We have added llvm packages to the repository. This fixes compatibility issues with LLVM from upstream. To use llvm packages supplied by us, disable the upstream llvm-toolset module before the installation:

```
sudo dnf module disble llvm-toolset
```

- We have added etcd and python3-python-etcd packages that are not available as rpm packages on RHEL/CentOS 8. These packages are used to set up HA clusters with Patroni.  For how to set up Patroni clusters, see [Patroni documentation](https://patroni.readthedocs.io/en/latest/README.html#running-configuring) 