# Contributing Guide

Thank you for deciding to contribute and help us improve Percona Distribution for PostgreSQL documentation!

We welcome contributors from all users and community. By contributing, you agree to the [Percona Community code of conduct](https://github.com/percona/community/blob/main/content/contribute/coc.md).

You can contribute to documentation in the following ways:

1. **Request a doc change through a Jira issue**. If you’ve spotted a doc issue (a typo, broken links, inaccurate instructions, etc.) but don’t have time nor desire to fix it yourself - let us know about it.

	- Click the **Submit DOC bug** link on the sidebar. This opens the [Jira issue tracker](https://jira.percona.com/projects/DISTPG/issues) for the doc project.
	- Sign in (create a Jira account if you don’t have one) and click **Create** to create an issue.
	- Describe the issue you have detected in the Summary, Description, Steps To Reproduce, Affects Version fields.

2. **[Contribute to documentation yourself](#contribute-to-documentation-yourself)**. There is the **Edit this page** link that leads you to the source file of the page on GitHub. There you make changes, create a pull request that we review and add to the doc project. For details how to do it, read on.

![PPG links](docs/_images/PPG_links.png)

## Contribute to documentation yourself

To contribute to the documentation, you should be familiar with the following technologies:
- [Markdown](https://www.markdownguide.org/basic-syntax/) markup language. It is used to write the documentation.
- [MkDocs](https://www.mkdocs.org/getting-started/) documentation generator. We use it to convert source ``.md`` files to html and PDF documents.
- [git](https://git-scm.com/) and [GitHub](https://guides.github.com/activities/hello-world/)
- [Docker](https://docs.docker.com/get-docker/). It allows you to run MkDocs in a virtual environment instead of installing it and its dependencies on your machine.

There are several active versions of the documentation. Each version derives from the major version of PostgreSQL, included in the distribution. 

- 11
- 12
- 13

The source .md files are in the ``docs`` directory. 

### Edit documentation online via GitHub

1. Click the **Edit this page** link on the sidebar. The Markdown file of the page opens in GitHub editor in your browser. If you haven’t worked with the repository before, GitHub creates a [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) of it for you.

2. Edit the page. You can check your changes on the **Preview** tab.

3. Commit your changes.

	 - In the *Commit changes* section, describe your changes.
	 - Select the **Create a new branch for this commit and start a pull request** option
	 - Click **Propose changes**.

4. GitHub creates a branch and a commit for your changes. It loads a new page on which you can open a pull request to Percona. The page shows the base branch - the one you offer your changes for, your commit message and a diff - a visual representation of your changes against the original page.  This allows you to make a last-minute review. When you are ready, click the **Create pull request** button.
5. Someone from our team reviews the pull request and if everything is correct, merges it into the documentation. Then it gets published on the site.

### Edit documentation locally

This option is for users who prefer to work on a local copy of the documentation files and / or have the full control over the documentation process.

The steps are the following:

1. Fork this repository
2. Clone the repository on your machine:

```sh
git clone git@github.com:percona/postgresql-docs.git
```

3. Change the directory to ``postgresql-docs`` and add your local repository:

```sh
git remote add <yourrepo-name> git@github.com:<your_name>/postgresql-docs.git
```

4. Pull the latest changes 

```sh
git fetch origin
git merge origin/<branch>
```
Make sure that your local branch and the branch you merge changes from are the same. So if you are on ``11`` branch, merge changes from ``origin/11``.

5. Create a separate branch for your changes

```sh
git checkout -b <my_changes>
```

6. Make changes
7. Commit your changes
8. Open a pull request to Percona

### Building the documentation

To verify how your changes look, generate the static site with the documentation. This process is called *building*. You can do it in these ways:
- [use Docker](#use-docker)
- [install MkDocs and build locally](#install-mkdocs-and-build-locally)

Learn more about the documentation structure in the [Repository structure](#repository-stucture) section.


#### Use Docker

1. [Get Docker](https://docs.docker.com/get-docker/)
2. We use [this Docker image](https://github.com/Percona-Lab/percona-doc-docker) to build documentation. Run the following command:

```sh
docker run --rm -v $(pwd):/docs perconalab/pmm-doc-md -f mkdocs-netlify.yml
```
   If Docker can't find the image locally, it first downloads the image, and then runs it to build the documentation.

3. Go to the ``site`` directory and open the ``index.html`` file to see the documentation.
4. To view your changes as you make them, run the following command:

``` sh
docker run --rm -p 8000:8000 -v $(pwd):/docs perconalab/pmm-doc-md mkdocs serve -f mkdocs-netlify.yml -a 0.0.0.0:8000
```

5. To create a PDF version of the documentation, run the following command:

```sh
docker run --rm -v $(pwd):/docs perconalab/pmm-doc-md -f mkdocs-pdf.yml
```

The PDF document is in the ``site/pdf`` folder.

#### Install MkDocs and build locally

1. Install [pip](https://pip.pypa.io/en/stable/installing/)
2. Install [MkDocs](https://www.mkdocs.org/getting-started/#installation).
3. While in the root directory of the doc project, run the following command to build the documentation:

```sh
mkdocs build -f mkdocs-netlify.yml
```
4. Go to the ``site`` directory and open the ``index.html`` file in your web browser to see the documentation.
5. To automatically rebuild the documentation and reload the browser as you make changes, run the following command:

```sh
mkdocs serve -f mkdocs-netlify.yml
```
6. To build the PDF documentation, do the following:
   - Install [mkdocs-with-pdf plugin](https://pypi.org/project/mkdocs-with-pdf/)
   - Run the following command

   ```sh
   mkdocs build -f mkdocs-pdf.yml
   ```

The PDF document is in the ``site/pdf`` folder.

## Repository structure

The repository includes the following directories and files:

- `mkdocs.yml` (default) - configuration file. Contains the settings for building the docs on Percona website
- `mkdocs-netlify.yml` - configuration file. Contains the settings for building the docs with Material theme.
- `mkdocs-pdf.yml` - configuration file. Contains the settings for building the PDF docs.
- `docs`:
  - `*.md` - Source markdown files.
  - `_images` - Images, logos and favicons
  - `css` - Styles
  - `js` - Javascript files
- `_resource`:
   - `templates`:
     - ``styles.scss`` - Styling for PDF documents
   - `theme`:
      - `main.html` - The layout template for hosting the documentation on Percona website
- `.github`:
   - `workflows`:
      - `main.yml` - The workflow configuration for building documentation with a GitHub action. (The documentation is built with `mike` tool to a dedicated `netlify` branch)
- `site` - This is where the output HTML files are put after the build

