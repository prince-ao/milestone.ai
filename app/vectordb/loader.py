from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup, SoupStrainer
import requests

def get_html_sitemap(url):
    response = requests.get(url, timeout=5)

    soup = BeautifulSoup(response.content, "xml")

    links = []

    locations = soup.find_all("loc")

    for location in locations:
        url = location.get_text()
        links.append(url)

    return links

def load(url, collection):

    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=SoupStrainer(["h1", "h3", "p", "a"])
        ),
    )

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    Qdrant.from_documents(documents=splits, collection_name=collection, embedding=OpenAIEmbeddings(), metadata={"path": url})

def load_gitbook():
    sitemap = "https://csi-cs-department.gitbook.io/internship-handbook/sitemap.xml"
    collection = "gitbook1"
    
    links = get_html_sitemap(sitemap)

    for link in links:
        load(link, collection)

if __name__ == "__main__":
    load_gitbook()