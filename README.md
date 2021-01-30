# Analysing $STAKE transfer events

## Prerequisites

- Jupyter Notebook
- At least Python 3.8.7

# How to run?

1. Clone the repo
2. Create your virtual env e.g. `python3 -m venv venv`
3. Activate it e.g. `source venv/bin/activate`
4. Install the packages `pip3 install -r requirements.txt`
5. Run the following command to setup virtual env for jupyter notebook `python3 -m ipykernel install --user --name=venv`
6. Run `jupyter notebook` to start Jupyter Notebook, open the `Analysis.ipynb` file and run all to see the charts. 

# How to get latest transfers?
1. Create a .env file and add your infura or alchemy api keys e.g.
```
INFURA_KEY=123451234512345123451234512345
ALCHEMY_KEY=abcdeabcdeabcdeabcdeabcde
```
2. If you want to get the latest transfer events, run `python3 query.py`