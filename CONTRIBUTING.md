# Documentation contributing guide

Thank you for deciding to contribute and help us improve Percona Distribution for PostgreSQL documentation!

We welcome contributors from all users and community. By contributing, you agree to the [Percona Community code of conduct](https://github.com/percona/community/blob/main/content/contribute/coc.md).

If you want to contribute code, see the [Code contribution guide](https://github.com/percona/postgres/blob/PSP_REL_18_STABLE/.github/CONTRIBUTING.md).

You can contribute to documentation in the following ways:

1. Request a doc change through Jira:

- Open the [Jira issue tracker](https://jira.percona.com/projects/PG/issues) for the project.
- (Optional but recommended) Search if the issue you want to report is already reported.
- Sign in (create a Jira account if you don’t have one) and click **Create** to create an issue.
- Select **PostgreSQL PG** in the Project dropdown and the work type **Story**.
- Describe the issue you have detected in the Summary, Description, Steps To Reproduce and Affects Version fields.

2. [Contribute to documentation on GitHub](#contribute-to-the-documentation-online-via-github).

To contribute to the documentation, you should be familiar with the following technologies:

- [Markdown](https://www.markdownguide.org/basic-syntax/). The documentation is written in Markdown.
- [MkDocs](https://www.mkdocs.org/getting-started/) documentation generator. We use it to convert source ``.md`` files to html and PDF documents.
- [git](https://git-scm.com/) and [GitHub](https://guides.github.com/activities/hello-world/)
- [Docker](https://docs.docker.com/get-docker/). It allows you to run MkDocs in a virtual environment instead of installing it and its dependencies on your machine.

## Contribute to the documentation online via GitHub

There are several active versions of the documentation. Each version derives from the major version of PostgreSQL, included in the distribution.

Each version has a branch in the repository named accordingly:

- 11 (EOL)
- 12 (EOL)
- 13 (EOL)
- 14
- 15
- 16
- 17
- 18

The source .md files are in the ``postgresql-docs/docs`` directory.

To start contributing:

1. Click the **Edit this file** icon.

[!NOTE]
If you haven’t worked with the repository before, GitHub creates a [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) of it for you.

2. Add your changes. You can see how your edit looks like in the **Preview** tab.

3. Commit your changes.

- Describe the changes you have made
- Select the **Create a new branch for this commit** and name your branch
- Click **Propose changes** to create the pull request

4. GitHub creates a branch and a commit for your changes. It loads a new page on which you can open a pull request to Percona. The page shows the base branch - the one you offer your changes for, your commit message and a diff - a visual representation of your changes against the original page.  This allows you to make a last-minute changes. When you are ready, click the **Create pull request** button.

5. Your changes will be reviewed and merged into the documentation.

### Edit documentation locally

This option is for users who prefer to work from their computer and / or have the full control over the documentation process.

The steps are the following:

1. Fork this repository
2. Clone the repository on your machine:

```sh
git clone git@github.com:percona/postgresql-docs.git
```

3. Change the directory to ``postgresql-docs`` and add your local repository:

```sh
git remote add <my-repo-name> git@github.com:<my_name>/postgresql-docs.git
```

4. Pull the latest changes

```sh
git fetch origin
git merge origin/<branch>
```

Make sure that your local branch and the branch you merge changes from are the same. So if you are on the ``18`` branch, merge changes from ``origin/18``.

5. Create a separate branch for your changes

```sh
git checkout -b <my_branch_name>
```

6. Make a commit mentioning the Jira issue in the commit message if any:

   ```
   git add .
   git commit -m "<my_fixes>"
   git push -u origin <my_branch_name>
   ```

7. Open a pull request to Percona

### Building the documentation using MkDocs

To verify how your changes look, generate the static site with the documentation. This process is called *building*.

[!NOTE]
Learn more about the documentation structure in the [Repository structure](#repository-structure) section.

To verify how your changes look, you can generate a static site locally:

1. Install [pip](https://pip.pypa.io/en/stable/installing/)
2. Install [MkDocs](https://www.mkdocs.org/getting-started/#installation).
3. Install all the required dependencies:

```
pip install -r requirements.txt
```

3. While in the root directory of the doc project, run the following command to build the documentation:

```sh
mkdocs build 
```
4. Go to the ``site`` directory and open the ``index.html`` file in your web browser to see the documentation.
5. To automatically rebuild the documentation and reload the browser as you make changes, run the following command:

```sh
mkdocs serve 
```

6. To build the PDF documentation, do the following:
   - Install [mkdocs-print-site-plugin](https://timvink.github.io/mkdocs-print-site-plugin/index.html)
   - Run the following command

   ```sh
    mkdocs build
   ```

This creates a single HTML page for the whole doc project. You can find the page at `site/print_page.html`. 

7. Open the `site/print_page.html` in your browser and save as PDF. Depending on the browser, you may need to select the Export to PDF, Print - Save as PDF or just Save and select PDF as the output format.

## Repository structure

The repository includes the following directories and files:

- `mkdocs-base.yml` - the base configuration file. It includes general settings and documentation structure.
- `mkdocs.yml` - configuration file. Contains the settings for building the docs on Percona website
- `mkdocs-pdf.yml` - configuration file. Contains the settings for building the PDF docs.
- `docs`:
  - `*.md` - Source markdown files.
  - `_images` - Images, logos and favicons
  - `css` - Styles
  - `js` - Javascript files
  - `templates`:
     - `pdf_cover_page.tpl` - The PDF cover page template
- `_resourcepdf`:
   - `overrides` - The directory with customized layout templates for PDF
- `.github`:
   - `workflows`:
      - `main.yml` - The workflow configuration for building documentation with a GitHub action. (The documentation is built with `mike` tool to a dedicated `publish` branch)
- `snippets` - The folder with pieces of documentation used in multiple places
- `site` - This is where the output HTML files are put after the build
