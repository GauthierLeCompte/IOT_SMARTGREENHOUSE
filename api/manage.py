from flask.cli import FlaskGroup
import pandas as pd
from src import create_app, db
from src.database.models import Measurement

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("success")

@cli.command()
def add_test():
    t = Measurement(0, 16.5, 20.4, 68.4, 1, 1)
    db.session.add(t)
    db.session.commit()

@cli.command()
def pull_test():
    q = Measurement.query.all()
    print(q)

@cli.command()
def fill_db():
    # resources
    resources = pd.read_csv('data/resources.csv')
    resources.drop(columns=['id', 'drain_water'], axis=1, inplace=True)
    resources.to_sql('resources', if_exists='append', con=db.engine, index=False)

    # conditions
    conditions = pd.read_csv('data/conditions.csv')
    conditions.drop(columns=['outside_temp'], axis=1, inplace=True)
    conditions.to_sql('conditions', if_exists='append', con=db.engine, index=False)


    db.session.commit()

if __name__ == '__main__':
    cli()