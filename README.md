# milestone.ai

## Documentation

[click here](https://github.com/prince-ao/milestone.ai/blob/main/ARCHITECTURE.md)

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

- You must create a `.env` file, use the `.env.example` as the model or contact prince-ao.
- create a file called output.css in `app/static/css/output.css` (this is where the css output from tailwind will be stored.)
- when you're working on the frontend run `pnpm runtailwind` before you start, so the tailwind process can start

## Starting Scraper

```bash
# install seleniumbase and chrome driver

pipenv install seleniumbase

sbase install chromedriver latest

# run (can add options for removing pop up browser, and remove -s to stop print statements)

pytest -s scraper.py
```

## Running the scrapper

```bash
# you must start qdrant before

cd app/vectordb

python loader.py

cd

sudo docker run -p 6333:6333 \
    -v $(pwd)/temp:/qdrant/storage \
    qdrant/qdrant
```
