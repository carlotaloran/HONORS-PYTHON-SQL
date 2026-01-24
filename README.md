# HONORS: PYTHON & SQL PORTION

## BUFFERS FOLDER
This folder contains Python scripts to construct buffers for the 100m and near-far specifications, with and without farm estimates, and compute thier zonal histograms based on land cover rasters. Scripts are designed to be run sequentially and rely on intermediate shapefiles. Running all scripts together may crash (hence why I separated them), and our lab computers need babysitting. Independent files run fine in the lab, but some take several hours.

### SETUP: 
Make sure the relevant paths exist! Below is an outline.

Buffers are constructed from gleba shapefiles, which come from the SICOR. These files were given as wkt geometries in .csv format. I cleaned the raw files in STATA and removed outliers in GIS (see Appendix A). The clean file has unique contract identifier contract_recipient_id. This file is stored in the clean data folder, under CREDIT/GLEBAS/glebas_matched_nomisreported. Land use rasters are stored in the raw data folder, under DEFORESTATION_DATA/Mapbiomas.

The NO_FARMS (G) folder considers the first buffer to be the polt associated with a contract, without taking the union of overlapping geometries. In the FARMS (F) folder, I use a farm estimate of farm area created by dissolving overlapping contract geometries. 

Each folder is self-contained, and script are numbered. The longest sequence of scripts (for my preferred specification) uses the numbering below.


### 1. MAKE BUFFER 0: 
This file makes farm plot shapefiles, which I call buffer 0. It does so by dissolving all geometries that overlap in the clean SICOR gleba files, creating new identifiers, FID. It makes the file twice, one for the near-far specification (NF) and another for the 100m specification (100M). They are saved to folders CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0 and CREDIT/GLEBAS/FARMS/100M_BUFFERS/b0 in the clean data folder, respectively. This takes about 1 hour.

### 2. MATCH FARM TO CONTRACT: 
This script take the b0 file created (which identifies unique farms with ID variable FID) and calculates its overlap with contract polygons to determine how many times a farm received credit and retreive its characteristics. It outputs a .csv file with variables farm_id (which is really the contract ID), FID (which is really the farm ID), and year. Saved as farm_to_contract in the clean data folder, under CREDIT/GLEBAS. This takes about 8 hours... for some cursed reason.

### 3. MAKE BUFFERS: 
Each of these files makes buffers from b0 at different distances for each specification (NF and 100M). They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**. The NF specification makes pairs (250-500, 500-1000, 750-1500, 1000-2000), and the 100M specification makes buffers at multiples of 100m until reaching 2000. One meter is approximated to 9.0785x10^-6 decimal degrees (see Appendix A). This takes 15 minutes for the NF specification, and 30 for the 100M specification.

### 4. MAKE RINGS:
These files convert buffers at all distances into disjoint rings by subtracting inner buffer overlap, for both specifications. They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**_ring. This runs in about 45m for the NF specification and 1.5h for the 100M specification.

### 5. REMOVE PROTECTED AREAS:
These files remove overlap with protected areas from all buffers (including b0), and both specifications. They are saved to folders CREDIT/GLEBAS/FARMS/**specification**_BUFFERS/b**distance** as b**distance**_ring_prot. This runs in about 1h for the NF specification and 1.5h for the 100M specification.

### 6. ZONAL HISTOGRAM 1 (PROT):
These files compute zonal histograms for each buffer–year combination using Mapbiomas rasters. Each new variable represents a pixel count of all unique values from the raster, for each polygon. Output from this script is saved as several .csv files in the clean data folder, under DEFORESTATION/FARMS/**specification**_BUFFERS/b**distance**. This takes about 1.5h for the NF specification and 3h for the 100M specification.

### 7. STUVA CHECK (CROP OVERLAPPING, TREATED BUFFERS): 

### 8. ZONAL HISTOGRAM 2 (STUVA):

### 9. REMOVE PUBLIC LAND:

### 10. ZONAL HISTOGRAM 3 (PRIVATE):

### 11. MAKE CLUSTERS:

### 12. ZONAL HISTOGRAM 4 (CLUSTERS):

### 13. GET FARM CLUSTER:

### 14. GET BUFFER STATE:

### 15. GET FARM CHARACTERISTICS (AREA, DISTANCE TO OTHER FARMS):


### Path outline:
    CREDIT_DEFOREST
        DATA
            DATA_CLEAN
                CREDIT
                    GLEBAS
                        FARMS
                            NF_BUFFERS <-- buffer shapefiles are here, in their own folder each
                            100M_BUFFERS  <-- buffer shapefiles are here, in their own folder each
                            glebas_matched_nomisreported <-- clean gleba .csv lived here
                DEFORESTATION
                    FARMS
                        NF_BUFFERS <-- zonal histogram csv files are saved here!
                        100M_BUFFERS <-- zonal histogram csv files are saved here!
            DATA_RAW
                DEFORESTATION
                    Mapbiomas <-- land use files live here
            SHAPEFILES
                Brazil_UCS <-- protected land shapefiles live here
                

## CLASSIFY CONTRACTS FOLDER
 This folder contains a script to re-classify credit contracts into cost and investment categories (see Theoretical Framework), edited but heavily written by ChatGPT. It uses a stricter definition for cost credit, discussed in the Appendix. The script inputs the contract file 'operacao_gleba_master', cleaned in STATA, and outputs a re-classified file, 'operacao_gleba_master_reclass', mapping contract IDs to the new classification. Both files are found in folder 'CREDIT/OPERACAO_GLEBA'. Run this script on the local terminal.

## (SOME) SUMMARY STATISTICS FOLDER
This folder contains SQL queries to obtain summary statistics included from several rounds of agricultural surveys. 