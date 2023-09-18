from bs4 import BeautifulSoup
import requests

# site to get a random paragraph
endpoint = "https://randomword.com/paragraph"


def get_paragraph():
    response = requests.get(url=endpoint)
    response.raise_for_status()
    contents = response.text

    soup = BeautifulSoup(contents, "html.parser")
    random_paragraph = soup.find(name="div", id="random_word_definition").get_text()

    # parse the paragraph to ensure it will fit in the Tkinter text box
    word_count = len(random_paragraph.split())
    if word_count > 35:
        random_paragraph = ' '.join(random_paragraph.split()[:35])
        if random_paragraph[-1] == ",":
            pass
        elif random_paragraph[-1] != ".":
            random_paragraph = random_paragraph + "."

    # return the paragraph string
    return random_paragraph
