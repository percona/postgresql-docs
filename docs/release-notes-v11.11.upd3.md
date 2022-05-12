# Percona Distribution for PostgreSQL 11.11 Third Update (2021-06-10)



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

This update of Percona Distribution for PostgreSQL includes `llvm` packages for  Red Hat Enterprise Linux 8 / CentOS 8. This fixes compatibility issues with LLVM from upstream. To use ``llvm`` packages supplied by us, disable the upstream ``llvm-toolset`` module before the installation:

```
sudo dnf module disable llvm-toolset
```