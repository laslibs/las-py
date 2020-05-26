# Las-py

## las-py is a zero-dependency Python library for parsing .Las file (Geophysical/Canadian well log files).

## Currently supports only version 2.0 of [LAS Specification](https://www.cwls.org/wp-content/uploads/2017/02/Las2_Update_Feb2017.pdf). For more information about this format, see the Canadian Well Logging Society [product page](https://www.cwls.org/products//)

- What's new in 1.1.0

  - Export to csv
  - Export to csv without rows containing null values
  - Bug fixes

- To Install


    ```sh
        $pip insatll las-py
    ```

- Usage


    ```python
        from las_py import Laspy
     ```
    ```python
        my_las = Laspy('path_to_las_file.las')
    ```

- Read data


    ```python
       data = my_las.data
       print(data)
       #[[2650.0, 177.825, -999.25, -999.25], [2650.5, 182.5, -999.25,-999.25], [2651.0,180.162, -999.25, -999.25], [2651.5, 177.825, -999.25, -999.25], [2652.0, 177.825, -999.25, -999.25] ...]
    ```
    ```python
        # get data with rows that has null value stripped
       data = my_las.data_stripped
       print(data)
       #[[2657.5, 212.002, 0.16665, 1951.74597], [2658.0, 201.44, 0.1966, 1788.50696], [2658.5, 204.314, 0.21004, 1723.21204], [2659.0, 212.075, 0.22888, 1638.328], [2659.5, 243.536, 0.22439, 1657.91699]...]
    ```

- Get the log headers


    ```python
        headers = my_las.header
        print(headers)
        # ['DEPTH', 'GR', 'NPHI', 'RHOB']
    ```

- Get the log headers descriptions


    ```python
        hds_and_desc = my_las.header_and_descr
        print(hds_and_desc)
        # {DEPTH': 'DEPTH', 'GR': 'Gamma Ray', 'NPHI': 'Neutron Porosity','RHOB': 'Bulk density'}
    ```

- Get a particular column, say Gamma Ray log


    ```python
        GR = my_las.column('GR')
        print(GR)
        # [-999.25, -999.25, -999.25, -999.25, -999.25, 122.03, 123.14, ...]
    ```
    ```python
        # get column with null values stripped
        GR = my_las.column_stripped('GR')
        print(GR)
        # [61.61, 59.99, 54.02, 50.87, 54.68, 64.39, 77.96, ...]
    ```
    > Note this returns the column, after all the data has been stripped off their null values, which means that valid data in a particular column would be stripped off if there is another column that has a null value at that particular row

- Get the Well Parameters

  ### Presents a way of accessing the details individual well parameters.

  ### The details include the following:

        1. descr - Description/ Full name of the well parameter
        2. units - Its unit measurements
        3. value - Value

  ```python
    start = my_las.well.STRT.value # 1670.0
    stop = my_las.well.STOP.value #  1669.75
    null_value = my_las.well.NULL.value #  -999.25
    # Any other well parameter present in the file, canbe gotten with the same syntax above
  ```

- Get the Curve Parameters

  ### Presents a way of accessing the details individual log columns.

  ### The details include the following:

        1. descr - Description/ Full name of the log column
        2. units - Unit of the log column measurements
        3. value - API value of the log column

  ```python
    NPHI = my_las.curve.NPHI.descr # 'Neutron Porosity'
    RHOB = my_las.curve.RHOB.descr # 'Bulk density'
    # This is the same for all log column present in the file
  ```

- Get the Parameters of the well

  ### The details include the following:

        1. descr - Description/ Full name of the log column
        2. units - Unit of the log column measurements
        3. value - API value of the log column

  ```python
    BHT = my_las.param.BHT.descr # 'BOTTOM HOLE TEMPERATURE'
    BHT_valaue = my_las.param.BHT.value # 35.5
    BHT_units = my_las.param.BHT.units # 'DEGC'
    # This is the same for all well parameters present in the file
  ```

- Get the number of rows and columns


    ```python
        rows = my_las.row_count # 4
        columns = my_las.column_count # 3081
    ```

- Get the version and wrap


    ```python
        version = my_las.version # '2.0'
        wrap = my_las.wrap # 'YES'
    ```

- Get other information

  ```python
      other = my_las.other
      print(other)
      # Note: The logging tools became stuck at 625 metres causing the data
      # between 625 metres and 615 metres to be invalid.
  ```

- Export to CSV

  ### This writes a csv file to the current working directory, with headers of the well and data section only.

  ```python
      my_las.to_csv('result')
      # result.csv has been created Successfully!
  ```

  > result.csv

  | DEPT | RHOB    | GR      | NPHI  |
  | ---- | ------- | ------- | ----- |
  | 0.5  | -999.25 | -999.25 | -0.08 |
  | 1.0  | -999.25 | -999.25 | -0.08 |
  | 1.5  | -999.25 | -999.25 | -0.04 |
  | ...  | ...     | ...     | ...   |
  | 1.3  | -999.25 | -999.25 | -0.08 |

  Or get the version of csv with null values stripped

  ```python
      my_las.to_csv_stripped('clean')
      # clean.csv has been created Successfully!
  ```

  > clean.csv

  | DEPT | RHOB  | GR   | NPHI  |
  | ---- | ----- | ---- | ----- |
  | 80.5 | 2.771 | 18.6 | -6.08 |
  | 81.0 | 2.761 | 17.4 | -6.0  |
  | 81.5 | 2.752 | 16.4 | -5.96 |
  | ...  | ...   | ...  | ...   |
  | 80.5 | 2.762 | 16.2 | -5.06 |

- ## Support
  las-py is an MIT-licensed open source project. You can help it grow by becoming a sponsor/supporter. Donate on [Patreon](https://www.patreon.com/bePatron?u=19152008)
