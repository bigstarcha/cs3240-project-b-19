# Off-Grounds Housing

Django app to help students find off-grounds housing

## Citations

For a complete list of citations for all major libraries and tutorials used in this project, see [citations.md](citations.md).

## Setup

### Virtual Environment

Start by [creating and activating a virtual environment](https://docs.python.org/3/library/venv.html):

```
python -m venv env

# to activate on Unix:
source env/bin/activate

# to activate on Windows:
.\env\Scripts\activate
```

### Dependencies

Next, install dependencies from `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### Environment Variables

Create a new `.env` file based on the contents of `.env.example` and complete with the necessary Cloudinary + Google OAuth credentials.

### pre-commit

You can now install [pre-commit](https://pre-commit.com/) for automatic formatting on commit:

```bash
pre-commit install
```

Test it by editing a Python / JavaScript / CSS / HTML file (for example, add some messy whitespace) and run the following:

```bash
pre-commit run --all-files
```

You should see an output like this:

```
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted housing/settings.py
All done! ✨ 🍰 ✨
1 file reformatted, 9 files left unchanged.

prettier.............................................(no files to check)Skipped
js-beautify..............................................................Passed
```

## Usage

To start the dev server:

```bash
python manage.py runserver
```

## VS Code Configuration

If you happen to be using VS Code as your editor, here are some settings that may be helpful for your workflow.

### Python environment

It's a good idea to [point VS Code to your created virtual environment](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment) so it can provide features like Intellisense. You can do so by running the "Python: Select Interpreter" command and picking the `env` folder in the project directory.

With this enabled, integrated terminals opened in VS Code (Control + `) should automatically activate your virtual environment.

### Formatting

Here's some settings for configuring VS Code to format your files as you work rather than relying on pre-commit.

Install these extensions:

- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django) - syntax highlighting + file association for Django templates
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - Black formatting for Python files
- [Beautify](https://marketplace.visualstudio.com/items?itemName=HookyQR.beautify) - js-beautify formatting for Django templates
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) - Prettier formatting for JavaScript + CSS

Next, add these options to your [settings JSON file](https://code.visualstudio.com/docs/getstarted/settings). You can put them in User settings to make them global or Workspace settings to keep them scoped to this project:

```js
{
  // Optional, can manually run the "Format Document" command
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  // If your environment is correctly configured, it should use the
  // existing local Black installation from the virtual environment
  "python.formatting.provider": "black",
  "[django-html]": {
    "editor.defaultFormatter": "HookyQR.beautify"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  // Enabling django-html support for js-beautify
  "beautify.language": {
    "html": ["htm", "html", "django-html"]
  },
  "files.associations": {
    // Treat any HTML file in a template directory as a Django template
    "**/templates/**/*.html": "django-html"
  }
}
```

## Test data

Rather than manually creating listings for usage while developing, we can import (borrow?) real listing data from [UVA's off grounds housing site](https://offgroundshousing.student.virginia.edu/). There's a script available to automate the process:

```bash
python manage.py scrape-uva
```

If you'd prefer to use a consistent data set rather than pulling live data, you can also use a prepared local fixture available in this repo:

```bash
python manage.py loaddata uva-scraped-listings.json
```

You can also create mock reviews for all existing listings:

```bash
python manage.py seed-reviews
```

## Deployment

Deploys are performed automatically through Heroku. The latest commit to the `main` branch will be deployed to the [production environment](https://off-grounds-housing-b-19.herokuapp.com).

Additionally, commits to the `staging` branch will be deployed to the [staging environment](https://off-grounds-housing-b-19-dev.herokuapp.com/). This branch can be freely committed to for testing without the need for a pull request (though it's likely a good idea to ensure it's not actively being used). If you want to deploy a specific branch:

```bash
# go to the staging branch
git checkout staging
# forcefully reset it to exactly match what you want to deploy
git reset --hard your-branch
# forcefully update the remote to match this new local staging branch
# make sure you're on staging before you do this!
git push --force
```
