# Sales Data Import
## Product Data
`product_data.json`
```json
[
{"Sku": 1241,"Price": 1099.0}
]
```
Maps a SKU to a price. 

### Notes
From comparison to `sales_two_data.csv`, it seems price is in units of pence, despite it's being expressed with a 
decimal point. This could be the result of the common practice of encoding currency data with integers and a 
subsequent, unintentional casting to float in the process of generating this file.