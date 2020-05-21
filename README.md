# Sales Data and Analysis
## Requirements
- python version 3.7+
- pip
- SQLite
## Installation
In the terminal, the following commands install the app.
```commandline
cd <this_directory>
pip install .
```
## Running
Once installed, the tool's help can be seen in the command line. 
```commandline
$ import-sales --help
```
```commandline
Usage: import-sales [OPTIONS] [%Y-%m-%d] OUTPUT

Options:
  -p, --products FILENAME  The products file.  [default: product_data.json]
  -s, --stores FILENAME    The stores file.  [default: store_data.json]
  -s1, --sales-1 FILENAME  The sales one file.  [default: sales_one_data.json]
  -s2, --sales-2 FILENAME  The sales two file.  [default: sales_two_data.csv]
  --help                   Show this message and exit.
```
There are two arguments, the business date from which the sales were recorded, and the output file to which the
database is saved in [SQLite](https://www.sqlite.org/index.html) format.

Additionally, there are four optional parameters to override the default files to be imported and/or updated by the tool.
As such, special care should be taken that this tool is run within the same directory as these files if defaults are used.
If defaults are overridden, special care should be exercised to ensure that these files are correctly referenced.

## Data Model
The model persisted by this tool consists of three tables, `Products`, `Stores`, and `Sales`.

Although there is also a file `staff_data.json` that maps staff to specific stores, at present this is not necessary 
for the purposes of the current model. The main reason this is so is that staff ids are recorded on each sale 
along with the store where that sale occurred. On the assumption that it is possible that a staff member may work from 
time to time in more than one store, it is safer to keep `store_id` in the `Sales` table and not infer this from 
`staff_id` with any mapping of staff to specific stores. If we allow for the possibility that staff will work in 
multiple stores, then the staff to store mapping will only express a staff member's 'home' store and this 
administrative information doesn't concern us.

The three tables of the data model are as follows.

### `Products`
| Column | Type | Attributes |
| --- | --- | --- |
| Date | Date | primary key |
| SKU | Integer | primary key |
| Price | Numeric(scale=2, precision=9) | not_null |

This is basically the data imported from `product_data.json` with the addition of a `Date` column. Over the course of time,
prices may change and SKUs may be added and removed. Each day, when a new product file is imported, the date for which the
prices were in effect is also recorded as one part of the table's primary key.

### `Stores`
| Column | Type | Attributes |
| --- | --- | --- |
| Id | Integer | primary_key |
| Name | String(40) | primary_key |
| Postcode | String(8) | not_null |
| Address | String(160) | not_null |

This, again, is basically the data imported. This time it is from `store_data.json`. Each day, when data is imported, this table
will remain small, where each stores info will simply be replaced if any information changes. As such, there is an 
assumption that, if a store is closed, it's id will be retired. Also, if a store is renamed, or has a change in postcode,
this change will simply result in an update to that store's row. Although there is considerable redundancy in each store's
entry, this is of little impact on memory, since the table will only have a number of rows equal to those stores past and
present.

### `Sales`
| Column | Type | Attributes |
| --- | --- | --- |
| Id | Integer | primary_key, auto_incrementing |
| SKU | Integer | not_null, foreign_key -> Products.SKU |
| BusinessDate | Date | not_null, foreign_key -> Products.Date |
| SoldFor | Numeric(scale=2, precision=9) | not_null |
| StaffId | Integer | not_null |
| Timestamp | DateTime | not_null |
| StoreId | Integer | not_null, foreign_key -> Store.Id |

The data which populates this table comes from two sources, `sales_one_data.json` and `sales_two_data.csv`. In addition
to the data found here, a `BusinessDate` column is added to match SKU prices on the business day when sales are 
recorded. The `Timestamp` column is UTC, but the period of time that the sales files cover will change in UTC during 
British Summer Time (BST). It's easier to add this field than infer local dates from UTC DateTimes.

## Querying
Once the data has been imported for the trading days of interest, or over such a period of time, the database
can be loaded and queried as anyone would normally in an SQLite client, or a Jupyter notebook, etc.

The source code to this tool, however, also contains a helpful class that uses the 
[SQLAlchemy](https://www.sqlalchemy.org/) python library to support common queries of the sales data.
### Total Sales
#### ... by Postcode in Cambridgeshire
In the following example, total sales in all postcodes of Cambridgeshire, which begin 'CB', can be queried as follows.

```python
result = SalesQuery \
    .of_total_sales_by_postcode() \
    .with_postcode_pattern(pattern='CB%') \
    .run(session=session)
```
... with the output.

```python
result = {'CB1 2BT': (Decimal('971.78'),)}
```
In addition to this query, there are a range of other total sale queries that should be of interest.
#### ... by Store
Rather than total sales in a Shire, total sales by actual store should be of interest.
```python
result = SalesQuery \
    .of_total_sales_by_store_name() \
    .run(session=session)
```
```python
result = {
 'Bury St Edmunds': (Decimal('586.83'),),
 'Cambridge': (Decimal('971.78'),),
 'Chelmsford': (Decimal('1019.96'),),
 'Norwich': (Decimal('589.11'),),
 'Peterborough': (Decimal('499.92'),),
 'Royston': (Decimal('731.16'),),
 'St Ives': (Decimal('592.53'),),
 'Stevenage': (Decimal('502.86'),)
}
```
#### ... by Staff ID
Or better yet, total sales by staff member should be useful for performance based metrics, etc.
```python
result = SalesQuery \
    .of_total_sales_by_staff_id() \
    .run(session=session)
```
```python
result = {
 5: (Decimal('682.44'),),
 33: (Decimal('213.62'),),
 39: (Decimal('81.75'),),
 198: (Decimal('233.62'),),
 241: (Decimal('516.22'),),
 346: (Decimal('152.64'),),
 437: (Decimal('171.96'),),
 543: (Decimal('241.93'),),
 544: (Decimal('149.86'),),
 678: (Decimal('10.99'),),
 689: (Decimal('59.29'),),
 978: (Decimal('175.32'),),
 1023: (Decimal('282.93'),),
 1734: (Decimal('443.57'),),
 3556: (Decimal('731.16'),),
 5839: (Decimal('59.29'),),
 7489: (Decimal('169.28'),),
 9765: (Decimal('360.92'),),
 10390: (Decimal('419.83'),),
 15482: (Decimal('337.52'),)
}
```
#### ... by SKU
There's also total sales broken down by SKU, but this would be more meaningful if there was information on the
margin associated with each unit of a SKU.
```python
result = SalesQuery \
    .of_total_sales_by_sku() \
    .run(session=session)
```
```python
result = {
 1241: (Decimal('205.51'),),
 1546: (Decimal('1616.85'),),
 2536: (Decimal('1209.51'),),
 4325: (Decimal('591.85'),),
 5345: (Decimal('1739.65'),),
 7653: (Decimal('130.78'),)
}
```
### Average Sold For and SKU Price
In addition to total sales, the degree of discount applied to those sales should be of interest.
#### ... by Staff ID
For example and in those cases where staff members may have discretion in offering a discount to make a sale, it
would be good to analyze who may be doing so excessively.
```python
result = SalesQuery \
    .of_average_sold_for_and_sku_price_by_staff_id() \
    .run(session=session)
```
```python
result = {
 5: (10, 68.24409999999999, 70.047),
 33: (4, 53.40575, 57.3875),
 39: (5, 16.3502, 16.79),
 198: (5, 46.7244, 50.11),
 241: (8, 64.5275, 65.0275),
 346: (3, 50.88033333333333, 52.85666666666666),
 437: (4, 42.989999999999995, 42.989999999999995),
 543: (5, 48.38680000000001, 52.386),
 544: (3, 49.95366666666667, 50.32),
 678: (1, 10.99, 10.99),
 689: (1, 59.29, 59.29),
 978: (4, 43.83025000000001, 45.31250000000001),
 1023: (6, 47.155, 47.155),
 1734: (7, 63.36757142857143, 67.07142857142858),
 3556: (10, 73.11600000000001, 74.11600000000001),
 5839: (1, 59.29, 59.29),
 7489: (2, 84.64, 84.64),
 9765: (6, 60.153333333333336, 61.98666666666667),
 10390: (7, 59.97571428571428, 59.97571428571428),
 15482: (8, 42.190125, 42.690000000000005)
}
```
In this output, for each `staff_id`, there are three numbers, the number of sales, the average of the "sold_for" 
amount of each sale, and the average SKU price on the day of the sale. This information can be used in a variety 
of ways for the organization, the store, or the individual staff member, assuming they're engaged in the sales process
and not just running the till.
#### ... by SKU
These averages can also be broken down by SKU. This may indicate which SKUs are dependent on discounting and psychological 
framing to move off the shelf. This may also be useful if information on each SKU's margin is known.
```python
result = SalesQuery \
    .of_average_sold_for_and_sku_price_by_sku() \
    .run(session=session_with_products_and_stores_and_sales_imported)
```
```python
result = {
 1241: (19, 10.816421052631583, Decimal('10.99')),
 1546: (15, 107.79013333333334, Decimal('109.99')),
 2536: (21, 57.59595238095236, Decimal('59.29')),
 4325: (15, 39.45673333333333, Decimal('39.99')),
 5345: (18, 96.64711111111112, Decimal('99.98')),
 7653: (12, 10.898333333333332, Decimal('10.99'))
}
```
### Filtering
All of the previous query's support additional filtering. For example, if you wanted to see staff id 33's total
sales broken down by SKU, you have.
```python
result = SalesQuery \
    .of_total_sales_by_sku() \
    .with_staff_ids(33) \
    .run(session=session)
```
```python
result = {
 2536: (Decimal('112.65'),),
 5345: (Decimal('89.98'),),
 7653: (Decimal('10.99'),)
}
```
... or to see if a specific store is offering too much of a discount on specific SKUs ...
```python
result = SalesQuery \
    .of_average_sold_for_and_sku_price_by_sku() \
    .with_store_names('Cambridge') \
    .run(session=session)
```
```python
result = {
 1241: (1, 10.99, Decimal('10.99')),
 1546: (3, 109.99, Decimal('109.99')),
 2536: (3, 57.31366666666667, Decimal('59.29')),
 4325: (4, 38.99, Decimal('39.99')),
 5345: (3, 89.98200000000001, Decimal('99.98')),
 7653: (3, 10.99, Decimal('10.99'))
}
```
In additional to filtering on stores or staff ids, sales can also be filtered according to the following.

- Postcode patterns, as was done in the Cambridgeshire example above
- A range of business dates, expressed with a start and/or a finish
- Particular SKUs 

## Data File Importation and Issues Confronted
### Product Data: `product_data.json`
#### Format
```json
[
  {"Sku": 1241,"Price": 1099.0},
  ...
]
```
From comparison to `sales_two_data.csv`, it seems price is in 'p', despite it's being expressed with a 
decimal point. This could be the result of the common practice of encoding currency data with integers and a 
subsequent, unintentional casting to float in the process of generating this file.

### Stores Data: `store_data.json`
#### Format
```json
[
  {
    "Id": 1,
    "Name": "Cambridge",
    "Postcode": "CB1 2BT",
    "Address": "1 High Street, Cambridge,CB1 2BT"
  },
  ...
]
```
The `Name` and `Postcode` fields seem to be repeated within the `Address` field. As mentioned earlier, we don't really
care about this as the table is very small.
### Staff Data: `staff_data.json`
#### Format
```json
[
  {
    "StoreName": "Cambridge",
    "StaffIds": [
      543,
      241,
      33
    ]
  },
  ...
]
```
List staff ids associated with each store. As mentioned earlier, we don't need and don't persist this information.
### Sales One Data: `sales_one_data.json`
#### Format
```json
[
  {
    "Id": "3902e58b-a9ba-4102-b88b-2a6d4d5adabe",
    "Sku": 2536,
    "DiscountPercent": 0,
    "StaffId": 10390,
    "SoldAtUtc": "2020-05-14T12:24:00Z",
    "Store": "Norwich"
  },
  ...
]
```
- `Id` can be null.
- It's possible to find duplicate sales records.
- `SoldAtUtc`, as it's name indicates, is a UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.

### Sales Two Data: `sales_two_data.csv`
#### Format
```csv
Id,Sku,SoldFor,StaffId,Timestamp,StoreId,Discounted
2039393795,4325,39.99,15482,14/05/2020 10:55:00,8,False
...
```
- Some `SoldFor` amounts are 0. This is an error. If there is `Discounted` is False, we can replace this value with the
SKU price.
- Some `Timestamp`s are `01/01/0001 00:00:00`. This is an error. We basically replace the date part of this timestamp with
the business day of the sales that the file is reporting.
- `Timestamp`, appears to be UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.

## Uninstallation
Once you feel you've exhausted the entertainment possibilities of this tool, you may uninstall it as follows.
```commandline
yes | pip uninstall sales
```