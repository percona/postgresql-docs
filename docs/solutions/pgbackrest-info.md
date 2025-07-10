# pgBackRest

`pgBackRest` is an advanced backup and restore tool designed specifically for PostgreSQL databases. `pgBackRest` emphasizes simplicity, speed, and scalability. Its architecture is focused on minimizing the time and resources required for both backup and restoration processes.

`pgBackRest` uses a custom protocol, which allows for more flexibility compared to traditional tools like `tar` and `rsync` and limits the types of connections that are required to perform a backup, thereby increasing security. `pgBackRest` is a simple, but feature-rich, reliable backup and restore system that can seamlessly scale up to the largest databases and workloads.

## Key features of `pgBackRest`

1. **Full, differential, and incremental backups (at file or block level)**: `pgBackRest` supports various types of backups, including full, differential, and incremental, providing efficient storage and recovery options. Block-level backups save space by only copying the parts of files that have changed.

2. **Point-in-Time recovery (PITR)**: `pgBackRest` enables restoring a PostgreSQL database to a specific point in time, crucial for disaster recovery scenarios. 

3. **Parallel backup and restore**: `pgBackRest` can perform backups and restores in parallel, utilizing multiple CPU cores to significantly reduce the time required for these operations.

4. **Local or remote operation**: A custom protocol allows `pgBackRest` to backup, restore, and archive locally or remotely via TLS/SSH with minimal configuration. This allows for flexible deployment options.

5. **Backup rotation and archive expiration**:  You can set retention policies to manage backup rotation and WAL archive expiration automatically.

6. **Backup integrity and verification**: `pgBackRest` performs integrity checks on backup files, ensuring they are consistent and reliable for recovery.

7. **Backup resume**: `pgBackRest` can resume an interrupted backup from the point where it was stopped. Files that were already copied are compared with the checksums in the manifest to ensure integrity. This operation can take place entirely on the repository host, therefore, it reduces load on the PostgreSQL host and saves time since checksum calculation is faster than compressing and retransmitting data.

8. **Delta restore**: This feature allows pgBackRest to quickly apply incremental changes to an existing database, reducing restoration time. 

9. **Compression and encryption**: `pgBackRest` offers options for compressing and encrypting backup data, enhancing security and reducing storage requirements.

## How `pgBackRest` works

`pgBackRest` supports a backup server (or a dedicated repository host in `pgBackRest` terminology). This repository host acts as the centralized backup storage. Multiple PostgreSQL clusters can use the same repository host.

In addition to a repository host with `pgBackRest` installed, you also need `pgBackRest` agents running on the database nodes. The backup server has the information about a PostgreSQL cluster, where it is located, how to back it up and where to store backup files. This information is defined within a configuration section called a *stanza*. 

The storage location where `pgBackRest` stores backup data and WAL archives is called the repository. It can be a local directory, a remote server, or a cloud storage service like AWS S3, S3-compatible storages or Azure blob storage. `pgBackRest` supports up to 4 repositories, allowing for redundancy and flexibility in backup storage. 

When you create a stanza, it initializes the repository and prepares it for storing backups. During the backup process, `pgBackRest` reads the data from the PostgreSQL cluster and writes it to the repository. It also performs integrity checks and compresses the data if configured.

Similarly, during the restore process, `pgBackRest` reads the backup data from the repository and writes it to the PostgreSQL data directory. It also verifies the integrity of the restored data.

## Next step

[How components work together :material-arrow-right:](ha-components.md){.md-button}