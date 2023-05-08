# IMDb Top Movies Scraper

This script scrapes the top movies from IMDb and stores the data in a CSV file.

## Installation

1. Create a virtual environment called `.env`:
   ```shell
   python -m venv .env
   ```

2. Activate the virtual environment:
   - Linux/macOS:
     ```shell
     source .env/bin/activate
     ```
   - Windows:
     ```shell
     .env\Scripts\activate
     ```

3. Install the required libraries:
   ```shell
   pip install -r requirements.txt
   ```

## Usage

To run the script, execute the following command:
```shell
python main.py
```

The script will store the data in a CSV file named `top_movies.csv` in the same directory.


## Tests

To run the tests in the `tests` directory, execute the following command:
```shell
pytest
```

Make sure the virtual environment is activated beforehand. You can run this command in the root directory.