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

# Data Model
The model consists of three tables, `Products`, `Stores`, and `Sales`.

Although there is also a file `staff_data.json` that maps staff to specific stores, at present this is not necessary 
for the purposes of the current model. The main reason this is so is that staff ids are recorded on each sale 
along with the store where that sale occurred. On the assumption that it is possible that a staff member may work from 
time to time in more than one store, it is safer to keep `store_id` in the `Sales` table and not infer this from 
`staff_id` with any mapping of staff to specific stores. If we allow for the possibility that staff will work in 
multiple stores, then the staff to store mapping will only express a staff member's 'home' store and this 
administrative information doesn't concern us.

The three tables of the data model are as follows.

## `Products`
| Column | Type | Attributes |
| --- | --- | --- |
| Date | Date | primary key |
| SKU | Integer | primary key |
| Price | Numeric(scale=2, precision=9) | not_null |

This is basically the data imported from `product_data.json`, with the addition of a `Date` column. Over the course of time,
prices may change and SKUs may be added and removed. Each day, when a new product file is imported, the date for which the
prices were in effect is also recorded as one part of the table's primary key.

## `Stores`
| Column | Type | Attributes |
| --- | --- | --- |
| Id | Integer | primary_key |
| Name | String(40) | primary_key |
| Postcode | String(8) | not_null |
| Address | String(160) | not_null |

This, again, is basically the data imported. This time, from `store_data.json`. Each day, when data is imported, this table
will remain small, where each stores info will simply be replaced if any information changes. As such, there is an 
assumption that, if a store is closed, it's id will be retired. Also, if a store is renamed, or has a change in postcode,
this change will simply result in an update to that store's row. Although there is considerable redundancy in each store's
entry, this is of little impact on memory, since the table will only have a number of rows equal to those stores past and
present.

## `Sales`
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

# Data File Importation and Issues Confronted
## Product Data: `product_data.json`
### Format
```json
[
  {"Sku": 1241,"Price": 1099.0},
  ...
]
```
From comparison to `sales_two_data.csv`, it seems price is in 'p', despite it's being expressed with a 
decimal point. This could be the result of the common practice of encoding currency data with integers and a 
subsequent, unintentional casting to float in the process of generating this file.

## Stores Data: `store_data.json`
### Format
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
## Staff Data: `staff_data.json`
### Format
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
## Sales One Data: `sales_one_data.json`
### Format
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

## Sales Two Data: `sales_two_data.csv`
### Format
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