# final-project-2025

## Setup

Clone the repo to download it from GitHub. Perhaps onto the Desktop.

Navigate to the repo using the command line.

```sh
cd ~/Desktop/final-project-2025
```

Create a virtual environment:

```sh
conda create -n final-project-2025 python=3.11
```

Activate the virtual environment:

```sh
conda activate final-project-2025
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

The stocks functionality requires an AlphaVantage API key. Obtain a premium AlphaVantage API Key (using the [form](https://www.alphavantage.co/support/#api-key) or shared by the prof).

Create a local ".env" file and store your environment variable in there:

```sh
# this is the ".env" file...

ALPHAVANTAGE_API_KEY="______________"
```

## Usage

#game of rock, paper, scissors:

```sh
python app/drinks.py

```

## Web app
Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS: all of it
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing

Run tests:

```sh
pytest
```


