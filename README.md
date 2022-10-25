#
# tfdnsgen.py
### Overview

Generate a Terraform script to create all of the DNS entries within an exported Azure DNS csv file. Copy the DNS entries from Azure and paste them into a CSV file for usage.

* Only A and CNAME records are implemented.
* Alias resource type and Alias target are not implemented

### Usage
```
python3 tfdnsgen --zone <zone name> --rg <resource group> --cssvfile <input> --tffile <output>
```

### CSV File Format
| Name      | Type      | TTL   | Value             | Alias resource type   | Alias target  |
| ----      | ----      | ---   | -----             | -------------------   | ------------  |
| @         | A         | 3600  | 127.0.0.1         |                       |               |
| foo       | CNAME     | 3600  | bar.cloudapps.net |                       |               |


### Parameters
| Parameter     | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| --help        | Help                                                                  |
| --zone        | The name of the Azure DNS zone                                        |
| --rg          | The name of the resource group for the zone                           |
| --csvfile     | The path to the output file of the Terrform file you want to create   |
| --tffile      | The path to the csv file that contains the Azure DNS records          |

<br>

---
# update-appinsights-dailycap.ps1
set the daily ingestion cap for all AI instance in every resource group