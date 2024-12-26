1. Install the `curl` download utility if it's not installed already:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    $ sudo apt install curl 
    ```

2. Download the `percona-release` repository package:

    ```{.bash data-prompt="$"}
    $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    ```

3. Install the downloaded repository package and its dependencies using `apt`:

    ```{.bash data-prompt="$"}
    $ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
    ```

4. Refresh the local cache to update the package information:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```