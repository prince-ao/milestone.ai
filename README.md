# milestone.ai

## Starting app

```bash
pipenv shell
pipenv install

pnpm install

# start backend
python run.py

# create an output.css file
touch app/static/css/output.css

# start tailwind process
pnpm runtailwind
```

## Notes

- You must create a `.env` file, use the `.env.example` as the model or ask prince-ao.
- create a file called output.css in `app/static/css/output.css` (this is where the css output from tailwind will be stored.)
- when you're working on the frontend run `pnpm runtailwind` before you start, so the tailwind process can start

## Starting Scraper

```bash
# installation
pipenv install seleniumbase

# get chrome driver
sbase install chromedriver latest

# start scraper (can add other options to remove popup browser, and remove the print statements)
pytest -s scraper.py
```
