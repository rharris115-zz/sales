import click
from io import TextIOWrapper
from src.sales.import_data import import_products, update_stores, import_sales_data_from_source_one, \
    import_sales_data_from_source_two
from sqlalchemy import create_engine
from src.sales.schema import create_tables
from datetime import datetime
from sqlalchemy.orm import sessionmaker, Session


@click.command()
@click.argument('business-date', type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument('output', type=click.Path(resolve_path=True))
@click.option('--products', '-p', type=click.File('r'), default='product_data.json', show_default=True,
              help='The products file.')
@click.option('--stores', '-s', type=click.File('r'), default='store_data.json', show_default=True,
              help='The stores file.')
@click.option('--sales-1', '-s1', type=click.File('r'), default='sales_one_data.json', show_default=True,
              help='The sales one file.')
@click.option('--sales-2', '-s2', type=click.File('r'), default='sales_two_data.csv', show_default=True,
              help='The sales two file.')
def main(business_date: datetime, output: str,
         products: TextIOWrapper, stores: TextIOWrapper,
         sales_1: TextIOWrapper, sales_2: TextIOWrapper):
    business_date = business_date.date()  # We don't need the time component.

    path = 'sqlite:///' + output  # output will be an absolute path.
    engine = create_engine(path)
    create_tables(engine=engine)

    session: Session = sessionmaker(bind=engine)()

    # Import SKUs and prices for the date.
    import_products(date=business_date, products=products, session=session)

    # Update stores data.
    update_stores(stores=stores, session=session)

    # Import Sales One
    import_sales_data_from_source_one(business_date=business_date, sales_json=sales_1, session=session)

    # Import Sales Two
    import_sales_data_from_source_two(business_date=business_date, sales_csv=sales_2, session=session)


if __name__ == '__main__':
    main()
