# Data Import
## Product Data
`product_data.json`
```json
[
{"Sku": 1241,"Price": 1099.0}
]
```
Maps a SKU to a price. 

### Notes
- From comparison to `sales_two_data.csv`, it seems price is in units of pence, despite it's being expressed with a 
decimal point. This could be the result of the common practice of encoding currency data with integers and a 
subsequent, unintentional casting to float in the process of generating this file.

## Stores Data
`store_data.json`
```json
[
  {
    "Id": 1,
    "Name": "Cambridge",
    "Postcode": "CB1 2BT",
    "Address": "1 High Street, Cambridge,CB1 2BT"
  }
]
```
### Notes
- The `Name` and `Postcode` fields seem to be repeated within the `Address` field.

## Staff Data
`staff_data.json`
```json
[
  {
    "StoreName": "Cambridge",
    "StaffIds": [
      543,
      241,
      33
    ]
  }
]
```

## Sales Data
### Sales One Data
`sales_one_data.json`
```json
[
  {
    "Id": "3902e58b-a9ba-4102-b88b-2a6d4d5adabe",
    "Sku": 2536,
    "DiscountPercent": 0,
    "StaffId": 10390,
    "SoldAtUtc": "2020-05-14T12:24:00Z",
    "Store": "Norwich"
  }
]
```
#### Notes
- `Id` can be null.
- It's possible to find duplicate sales records.
- `SoldAtUtc`, it's name indicates, is a UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.

### Sales Two Data
`sales_two_data.csv`
```csv
Id,Sku,SoldFor,StaffId,Timestamp,StoreId,Discounted
2039393795,4325,39.99,15482,14/05/2020 10:55:00,8,False
```
#### Notes
- Some `SoldFor` amounts are 0. This is an error.
- Some `Timestamp`s are `01/01/0001 00:00:00`. This is an error.
- `Timestamp`, appears to be UTC time. However, this file reports sales over the course of a day
that can start at `23:00:00` UTC during British Summer Time.