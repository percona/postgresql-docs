# Documentation contributing guide

This guide explains how to contribute to the Percona Distribution for PostgreSQL documentation.

We welcome contributors from all users and the community. By contributing, you agree to the [Percona Community code of conduct](https://github.com/percona/community/blob/main/content/contribute/coc.md).

If you want to contribute code, see the [Code contribution guide](https://github.com/percona/postgres/blob/PSP_REL_18_STABLE/.github/CONTRIBUTING.md).

You can contribute to documentation in the following ways:

1. Request documentation changes through Jira:

- Open the [Jira issue tracker](https://jira.percona.com/projects/PG/issues) for the project.
- Sign in (create a Jira account if you don’t have one).
- Click **Create** to create an issue.
- (Optional but recommended) Search if the issue you want to report is already reported.
- Select **PostgreSQL PG** in the Project dropdown and the work type.
- Describe the issue in the Summary and Description fields. Optionally, you can also fill in the Steps To Reproduce and Affects Version fields.

2. [Contribute to documentation on GitHub](#contribute-directly-on-github).

To contribute to the documentation, basic familiarity with the following tools is useful:

- [Markdown](https://www.markdownguide.org/basic-syntax/). The documentation is written in Markdown.
- [MkDocs](https://www.mkdocs.org/getting-started/) documentation generator. We use it to convert source ``.md`` files to html and PDF documents.
- [git](https://git-scm.com/) and [GitHub](https://guides.github.com/activities/hello-world/)

## Contribute directly on GitHub

There are several active versions of the documentation. Each version derives from the major version of PostgreSQL, included in the distribution.

Each documentation branch is named after the PostgreSQL major version (for example: `11`(EOL), `12`(EOL), `13`(EOL), `14`, `15`, `16`, `17`, `18`).

The source .md files are in the ``postgresql-docs/docs`` directory.

To start contributing:

1. Select **Edit this file**.

> **NOTE**
> If you haven’t worked with the repository before, GitHub creates a [fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) of it for you.

2. Add your changes. You can see how your edit looks in the **Preview** tab.

3. Commit your changes.

- Describe the changes you have made
- Select the **Create a new branch for this commit** and name your branch
- Click **Propose changes** to create the pull request

4. GitHub creates a branch and a commit for your changes. It loads a new page on which you can open a pull request to Percona. The page shows the base branch - the one you offer your changes for, your commit message and a diff - a visual representation of your changes against the original page.  This allows you to make last-minute changes. When you are ready, click the **Create pull request** button.

5. Your changes will be reviewed and merged into the documentation.

### Edit documentation locally

If you want to work on your computer locally, follow these steps:

1. Fork this repository
2. Clone the repository on your machine:

```sh
git clone git@github.com:<my_name>/postgresql-docs.git
cd postgresql-docs
```

3. Add the upstream (Percona) repository as a remote:

```sh
git remote add upstream git@github.com:percona/postgresql-docs.git
```

4. Pull the latest changes

```sh
git fetch upstream
git merge upstream/<branch>
```

Make sure you merge changes from the same documentation branch you are working on. For example, if you are on branch ``14``, merge from ``upstream/14``.

5. Create a separate branch for your changes. If you work on a Jira issue, please follow this pattern for a branch name: `<PG-123>-short-description`:

```sh
git checkout -b <PG-123>-short-description upstream/<target-branch>
```

6. Make a commit mentioning the Jira issue in the commit message if any:

```sh
git add .
git commit -m "PG-123-<my_fixes>"
git push -u origin <my_branch_name>
```

7. Open a pull request to Percona

### Building the documentation using MkDocs

To verify how your changes look, generate the static site with the documentation. This process is called *building*.

> **NOTE**
> Learn more about the documentation structure in the [Repository structure](#repository-structure) section.

To verify how your changes look, you can generate a static site locally:

1. Install [pip](https://pip.pypa.io/en/stable/installing/)
2. Install [MkDocs](https://www.mkdocs.org/getting-started/#installation).
3. Install all the required dependencies:

```sh
pip install -r requirements.txt
```

4. While in the root directory of the documentation project, run the following command to build the documentation:

```sh
mkdocs build 
```

5. Go to the ``site`` directory and open the ``index.html`` file in your web browser to see the documentation.
6. To automatically rebuild the documentation and reload the browser as you make changes, run the following command:

```sh
mkdocs serve 
```

7. To build the PDF documentation, do the following:
   - Install [mkdocs-print-site-plugin](https://timvink.github.io/mkdocs-print-site-plugin/index.html)
   - Run the following command

   ```sh
    mkdocs build
   ```

This creates a single HTML page for the whole doc project. You can find the page at `site/print_page.html`.

8. Open the `site/print_page.html` in your browser and save as PDF. Depending on the browser, you may need to select the Export to PDF, Print - Save as PDF or just Save and select PDF as the output format.

You can also view the site at <http://127.0.0.1:8000>.

## Repository structure

The repository includes the following directories and files:

- `mkdocs-base.yml` - the base configuration file. It includes general settings and documentation structure.
- `mkdocs.yml` - configuration file. Contains the settings for building the documentation on Percona website
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