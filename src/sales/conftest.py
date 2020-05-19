import json
import textwrap
from datetime import date
from os import PathLike
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from . import schema


@pytest.fixture
def db_path(tmpdir: PathLike) -> PathLike:
    return Path(tmpdir) / 'sales.db'


@pytest.fixture
def engine(db_path: PathLike) -> Engine:
    path = 'sqlite:///' + str(db_path)
    return create_engine(path)


@pytest.fixture
def good_product_json_data() -> str:
    return json.dumps([
        {
            "Sku": 1241,
            "Price": 1099.0
        },
        {
            "Sku": 4325,
            "Price": 3999.0
        },
        {
            "Sku": 1546,
            "Price": 10999.0
        },
        {
            "Sku": 7653,
            "Price": 1099.0
        },
        {
            "Sku": 2536,
            "Price": 5929.0
        },
        {
            "Sku": 5345,
            "Price": 9998.0
        }
    ])


@pytest.fixture
def good_store_json_data() -> str:
    return json.dumps([
        {
            "Id": 1,
            "Name": "Cambridge",
            "Postcode": "CB1 2BT",
            "Address": "1 High Street, Cambridge,CB1 2BT"
        },
        {
            "Id": 2,
            "Name": "Peterborough",
            "Postcode": "PE1 4HG",
            "Address": "1 High Street, Peterborough,PE1 4HG"
        },
        {
            "Id": 3,
            "Name": "St Ives",
            "Postcode": "PE27 3AB",
            "Address": "1 High Street, St Ives,PE27 3AB"
        },
        {
            "Id": 4,
            "Name": "Stevenage",
            "Postcode": "SG2 6BG",
            "Address": "1 High Street, Stevenage,SG2 6BG"
        },
        {
            "Id": 5,
            "Name": "Royston",
            "Postcode": "SG8 5RY",
            "Address": "1 High Street, Royston,SG8 5RY"
        },
        {
            "Id": 6,
            "Name": "Bury St Edmunds",
            "Postcode": "IP32 6AD",
            "Address": "1 High Street, Bury St Edmunds,IP32 6AD"
        },
        {
            "Id": 7,
            "Name": "Norwich",
            "Postcode": "NR1 5BT",
            "Address": "1 High Street, Norwich,NR1 5BT"
        },
        {
            "Id": 8,
            "Name": "Chelmsford",
            "Postcode": "CM3 8TU",
            "Address": "1 High Street, Chelmsford,CM3 8TU"
        }
    ])


@pytest.fixture
def sales_one_data_json():
    return json.dumps([
        {
            "Id": "3902e58b-a9ba-4102-b88b-2a6d4d5adabe",
            "Sku": 2536,
            "DiscountPercent": 0,
            "StaffId": 10390,
            "SoldAtUtc": "2020-05-14T12:24:00Z",
            "Store": "Norwich"
        },
        {
            "Id": "4cd66057-b83a-4650-a692-57c1ce112868",
            "Sku": 1546,
            "DiscountPercent": 0,
            "StaffId": 15482,
            "SoldAtUtc": "2020-05-14T14:11:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "1f452fa2-1628-4c28-be4f-f30cd7ab436f",
            "Sku": 5345,
            "DiscountPercent": 10,
            "StaffId": 33,
            "SoldAtUtc": "2020-05-14T06:33:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "1f452fa2-1628-4c28-be4f-f30cd7ab436f",
            "Sku": 5345,
            "DiscountPercent": 10,
            "StaffId": 33,
            "SoldAtUtc": "2020-05-14T06:33:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "700a3817-82b9-4968-937c-a94b535b5dae",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T21:24:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "dfd7af0a-15a0-45e5-947f-2c1568d76856",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 241,
            "SoldAtUtc": "2020-05-14T22:43:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": None,
            "Sku": 2536,
            "DiscountPercent": 0,
            "StaffId": 33,
            "SoldAtUtc": "2020-05-14T11:07:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "5ff28831-a9c0-490a-836a-f2ed84c6045b",
            "Sku": 1241,
            "DiscountPercent": 10,
            "StaffId": 544,
            "SoldAtUtc": "2020-05-14T09:58:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "d7f81de6-8d3e-4a1a-808c-75fa82e65771",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 1734,
            "SoldAtUtc": "2020-05-14T03:40:00Z",
            "Store": "Stevenage"
        },
        {
            "Id": "9c9f670c-5e6e-43c9-bacb-7c11ad4c3e9b",
            "Sku": 2536,
            "DiscountPercent": 10,
            "StaffId": 198,
            "SoldAtUtc": "2020-05-14T04:14:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "0adafec5-3857-4e53-9a2b-0d8f8d524dbf",
            "Sku": 5345,
            "DiscountPercent": 10,
            "StaffId": 543,
            "SoldAtUtc": "2020-05-14T18:50:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "600399dd-35e1-42eb-a33b-955b6b650e61",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 1734,
            "SoldAtUtc": "2020-05-14T01:25:00Z",
            "Store": "Stevenage"
        },
        {
            "Id": "e162c0b5-6860-4676-a43a-c91dbec803d7",
            "Sku": 2536,
            "DiscountPercent": 10,
            "StaffId": 978,
            "SoldAtUtc": "2020-05-14T11:58:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "0c102626-802c-413f-b942-4ff574d28bb3",
            "Sku": 2536,
            "DiscountPercent": 10,
            "StaffId": 1734,
            "SoldAtUtc": "2020-05-14T17:20:00Z",
            "Store": "Stevenage"
        },
        {
            "Id": "9a8d020a-bb47-462d-af9b-00c1ed9a4701",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 3556,
            "SoldAtUtc": "2020-05-14T18:41:00Z",
            "Store": "Royston"
        },
        {
            "Id": "ebba9202-74eb-4aba-8342-5c8223ae2b7a",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 543,
            "SoldAtUtc": "2020-05-14T21:15:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "779c5076-ea34-4494-bde1-4deb05a9a8df",
            "Sku": 5345,
            "DiscountPercent": 10,
            "StaffId": 543,
            "SoldAtUtc": "2020-05-14T02:34:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "cd766584-ee9b-41ad-bf9c-c40614e484f6",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 15482,
            "SoldAtUtc": "2020-05-14T12:40:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "59fda437-09f7-4ccc-9934-d99d055d648c",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 33,
            "SoldAtUtc": "2020-05-14T05:45:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "feec22bc-145a-4324-96da-447f8e73c8e2",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T11:09:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "46153072-22ab-4577-a440-6f5daa4dc2e1",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 39,
            "SoldAtUtc": "2020-05-14T01:29:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "74ceb8ed-b39c-4bf0-83e1-807076b21fc9",
            "Sku": 1546,
            "DiscountPercent": 0,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T18:56:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "bd85bcd1-0e80-49cc-abf5-9153aa2132be",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 437,
            "SoldAtUtc": "2020-05-14T22:55:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "3abeede0-193f-40bd-b31c-d68910adeb58",
            "Sku": 1241,
            "DiscountPercent": 10,
            "StaffId": 39,
            "SoldAtUtc": "2020-05-14T11:23:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "f6ea9cb6-c90a-48f9-ad36-eba16238e825",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 3556,
            "SoldAtUtc": "2020-05-14T12:48:00Z",
            "Store": "Royston"
        },
        {
            "Id": "28f19c79-8292-461d-a53b-aa4fa3534de4",
            "Sku": 2536,
            "DiscountPercent": 0,
            "StaffId": 15482,
            "SoldAtUtc": "2020-05-14T10:35:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "821868bc-fe46-4729-a157-2926c4a1b055",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 437,
            "SoldAtUtc": "2020-05-13T23:28:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "54eb7c8b-40e2-4bf1-9a13-996e2bd624d8",
            "Sku": 2536,
            "DiscountPercent": 10,
            "StaffId": 346,
            "SoldAtUtc": "2020-05-14T22:06:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "ab5d5ed8-c84f-4e29-b697-5176169c5e12",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 1023,
            "SoldAtUtc": "2020-05-14T17:31:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "ab5d5ed8-c84f-4e29-b697-5176169c5e12",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 1023,
            "SoldAtUtc": "2020-05-14T17:31:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "f94a1809-4fe0-41c5-afa3-a9ec1ed11aa3",
            "Sku": 1546,
            "DiscountPercent": 10,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T02:10:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "f94a1809-4fe0-41c5-afa3-a9ec1ed11aa3",
            "Sku": 1546,
            "DiscountPercent": 10,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T02:10:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "ee76dd5f-0ba9-41b2-8027-b07f0466e565",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T07:27:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "b825a277-0046-478d-9d36-c7a894661a10",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 1023,
            "SoldAtUtc": "2020-05-14T12:57:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "59e52966-1874-482d-b7ff-48add0a3650b",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 437,
            "SoldAtUtc": "2020-05-14T12:25:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "b48c398a-2eb3-4a0c-afcf-88fd447fd4f9",
            "Sku": 1546,
            "DiscountPercent": 0,
            "StaffId": 241,
            "SoldAtUtc": "2020-05-14T20:24:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "be553596-cb60-4e84-b167-42f3ea5453ec",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 9765,
            "SoldAtUtc": "2020-05-14T10:47:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "a56a2161-54e9-451a-a53f-a22c9d296762",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 39,
            "SoldAtUtc": "2020-05-13T23:02:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "a56a2161-54e9-451a-a53f-a22c9d296762",
            "Sku": 4325,
            "DiscountPercent": 0,
            "StaffId": 39,
            "SoldAtUtc": "2020-05-13T23:02:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "f99c7657-b1d8-4f6e-be3b-a5d2616d99b7",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 978,
            "SoldAtUtc": "2020-05-14T00:30:00Z",
            "Store": "Peterborough"
        },
        {
            "Id": "9be115ba-641a-4c91-bfed-f35fe6bbc080",
            "Sku": 2536,
            "DiscountPercent": 10,
            "StaffId": 33,
            "SoldAtUtc": "2020-05-14T04:47:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "61ddd335-586b-43a4-881d-427398418fe6",
            "Sku": 5345,
            "DiscountPercent": 10,
            "StaffId": 1734,
            "SoldAtUtc": "2020-05-14T07:10:00Z",
            "Store": "Stevenage"
        },
        {
            "Id": "0d6a7c60-4cff-4904-bd20-80db4d3a3b74",
            "Sku": 1546,
            "DiscountPercent": 10,
            "StaffId": 198,
            "SoldAtUtc": "2020-05-14T13:58:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "aec95c05-62d1-41ca-82c6-26d5a40621f8",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 3556,
            "SoldAtUtc": "2020-05-14T15:07:00Z",
            "Store": "Royston"
        },
        {
            "Id": "629920d1-fab7-46a6-8ac8-f0dc6cb80cfb",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 9765,
            "SoldAtUtc": "2020-05-14T11:59:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "11c0dac0-a27f-4c30-8c87-b51647fb672c",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 1023,
            "SoldAtUtc": "2020-05-14T18:12:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "c2aed43c-3840-4ecd-821f-c7a77aeadbeb",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 9765,
            "SoldAtUtc": "2020-05-14T03:55:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "42caa4a7-6b84-4993-a4a6-ee5a66fe0c1b",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 10390,
            "SoldAtUtc": "2020-05-14T01:51:00Z",
            "Store": "Norwich"
        },
        {
            "Id": "9a1727cc-e094-4e11-b163-1527f5517510",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 198,
            "SoldAtUtc": "2020-05-14T09:59:00Z",
            "Store": "Bury St Edmunds"
        },
        {
            "Id": "e807e515-ba30-42af-bdde-bc6e8fe1f2d5",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 543,
            "SoldAtUtc": "2020-05-14T05:08:00Z",
            "Store": "Cambridge"
        },
        {
            "Id": "fcfea63d-b5bf-4c73-a8b3-fdb0b79e119f",
            "Sku": 1241,
            "DiscountPercent": 0,
            "StaffId": 1734,
            "SoldAtUtc": "2020-05-14T11:43:00Z",
            "Store": "Stevenage"
        },
        {
            "Id": "e8aec393-53b6-43cc-9fea-a38f7826849d",
            "Sku": 4325,
            "DiscountPercent": 10,
            "StaffId": 15482,
            "SoldAtUtc": "2020-05-14T19:15:00Z",
            "Store": "Chelmsford"
        },
        {
            "Id": "b90aa9b2-6fb3-4998-b4fb-9e36e5754a23",
            "Sku": 7653,
            "DiscountPercent": 0,
            "StaffId": 9765,
            "SoldAtUtc": "2020-05-14T14:54:00Z",
            "Store": "St Ives"
        },
        {
            "Id": "813c57e4-8988-443e-b54b-f86426396abe",
            "Sku": 5345,
            "DiscountPercent": 0,
            "StaffId": 5,
            "SoldAtUtc": "2020-05-14T10:12:00Z",
            "Store": "Chelmsford"
        }
    ])


@pytest.fixture
def sales_two_data_csv() -> str:
    return textwrap.dedent(
        '''
        Id,Sku,SoldFor,StaffId,Timestamp,StoreId,Discounted
        2039393795,4325,39.99,15482,14/05/2020 10:55:00,8,False
        1264635157,4325,39.99,346,14/05/2020 07:38:00,2,False
        1317732669,2536,59.29,10390,14/05/2020 12:41:00,7,False
        1272914388,2536,59.29,10390,14/05/2020 00:56:00,7,False
        137011527,7653,10.99,15482,14/05/2020 22:38:00,8,False
        1231427396,1241,10.99,39,14/05/2020 04:22:00,3,False
        1620937926,1241,10.99,978,14/05/2020 03:12:00,2,False
        1781345168,1241,10.99,978,14/05/2020 08:36:00,2,False
        1304501388,1241,10.99,9765,14/05/2020 18:03:00,3,False
        1622992670,4325,39.99,241,14/05/2020 16:17:00,1,False
        1670740127,1546,109.99,241,14/05/2020 15:47:00,1,False
        908728293,2536,59.29,1734,14/05/2020 08:49:00,4,False
        1983439359,2536,59.29,3556,14/05/2020 22:48:00,5,False
        951818410,1241,10.99,3556,01/01/0001 00:00:00,5,False
        976543949,7653,9.89,39,14/05/2020 01:15:00,3,True
        1504850437,5345,99.98,1023,14/05/2020 18:34:00,6,False
        826096302,5345,99.98,3556,14/05/2020 11:30:00,5,False
        1564877310,1546,98.99,9765,14/05/2020 11:51:00,3,True
        1667452904,1546,109.99,241,01/01/0001 00:00:00,1,False
        1548582968,5345,99.98,3556,14/05/2020 00:30:00,5,False
        507128316,4325,35.99,241,14/05/2020 14:23:00,1,True
        1147100110,2536,59.29,15482,13/05/2020 23:24:00,8,False
        1199492356,4325,39.99,241,14/05/2020 13:45:00,1,False
        2131187468,2536,53.36,5,14/05/2020 15:19:00,8,True
        2002135001,7653,10.99,543,14/05/2020 01:35:00,1,False
        1989271024,2536,59.29,5,14/05/2020 06:01:00,8,False
        1216169468,1546,109.99,7489,14/05/2020 15:07:00,7,False
        44976786,1546,109.99,1023,14/05/2020 10:11:00,6,False
        1946278125,1241,9.89,5,14/05/2020 02:43:00,8,True
        2010811996,5345,89.98,1734,14/05/2020 08:01:00,4,True
        1683653781,4325,39.99,1023,14/05/2020 06:33:00,6,False
        1038170219,1241,10.99,678,14/05/2020 02:26:00,6,False
        1874444639,1546,0,437,14/05/2020 16:11:00,2,False
        294879635,1241,10.99,5,14/05/2020 10:13:00,8,False
        635844809,1546,109.99,3556,14/05/2020 00:45:00,5,False
        324437303,1546,109.99,3556,14/05/2020 05:22:00,5,False
        25199017,1546,109.99,10390,01/01/0001 00:00:00,7,False
        475005533,2536,59.29,241,14/05/2020 03:02:00,1,False
        1348420419,7653,10.99,15482,14/05/2020 00:14:00,8,False
        559974869,2536,59.29,346,14/05/2020 22:07:00,2,False
        1463613423,2536,59.29,5839,14/05/2020 01:34:00,6,False
        483032126,7653,0,10390,14/05/2020 18:48:00,7,False
        470491747,1241,10.99,198,14/05/2020 05:36:00,6,False
        751825281,5345,99.98,544,01/01/0001 00:00:00,3,False
        34422625,4325,39.99,544,14/05/2020 17:37:00,3,False
        32343440,5345,89.98,3556,14/05/2020 00:25:00,5,True
        493186766,2536,59.29,689,14/05/2020 00:49:00,4,False
        857087382,2536,59.29,198,14/05/2020 02:02:00,6,False
        745100260,1546,109.99,10390,14/05/2020 21:37:00,7,False
        536799568,2536,59.29,7489,14/05/2020 16:06:00,7,False
        '''
    ).strip()


@pytest.fixture
def sales_date() -> date:
    return date(2020, 5, 14)


@pytest.fixture
def engine_with_tables(engine: Engine):
    schema.create_tables(engine=engine)
    return engine


@pytest.fixture
def session(engine_with_tables: Engine) -> Session:
    return sessionmaker(bind=engine_with_tables)()
