from flask.cli import FlaskGroup
import pandas as pd
from src import create_app, db
from src.model import train_model, test_model
from src.preprocessing import preprocess_data
from os import path

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def train():
    print("starting training process")
    if not path.isfile("/usr/src/app/data/data_pp.csv"):
        print("data not preprocessed, starting preprocessing ...")
        preprocess_data()
        print("preprocessing completed")
    print('training ...')
    train_model()
    print("training successfully completed")

@cli.command()
def test():
    print("Testing model ...")
    test_model()
    print("Testing completed")


@cli.command()
def preprocess():
    print("starting preprocessing ...")
    preprocess_data()
    print("preprocessing completed")


@cli.command()
def view():
    if path.isfile("/usr/src/app/data/data_pp.csv"):
        df = pd.read_csv("/usr/src/app/data/conditions_pp.csv")
        print(df.head(5))
        print(df.describe())
    else:
        print("Error: no preprocessed data found, try preprocessing first")

if __name__ == '__main__':
    cli()