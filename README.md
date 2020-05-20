# Data Model
## 
```rest

```

# Import Data Files
## Product Data: `product_data.json`
### Format
```json
[
  {"Sku": 1241,"Price": 1099.0},
  ...
]
```
Maps a SKU to a price. 
### Issues
- From comparison to `sales_two_data.csv`, it seems price is in 'p', despite it's being expressed with a 
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
Provides info for each store.
### Issues
- The `Name` and `Postcode` fields seem to be repeated within the `Address` field.
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
List staff ids associated with each store.
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
Provides sales records.
### Issues
- `Id` can be null.
- It's possible to find duplicate sales records.
- `SoldAtUtc`, it's name indicates, is a UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.

## Sales Two Data: `sales_two_data.csv`
### Format
```csv
Id,Sku,SoldFor,StaffId,Timestamp,StoreId,Discounted
2039393795,4325,39.99,15482,14/05/2020 10:55:00,8,False
...
```
Provides sales records.
### Issues
- Some `SoldFor` amounts are 0. This is an error.
- Some `Timestamp`s are `01/01/0001 00:00:00`. This is an error.
- `Timestamp`, appears to be UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.