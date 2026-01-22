# HONORS: PYTHON & SQL PORTION

## BUFFERS FOLDER
This folder contains Python scripts to construct buffers for the 100m and near-far specifications, and compute thier zonal histograms based on land cover rasters. Scripts are designed to be run sequentially and rely on intermediate shapefiles. Running all scripts together may crash, our lab computers need babysitting. Independent files run fine in the lab, but some take several hours.

### SETUP: 
Make sure the relevant paths exist! Below is an outline.

Buffers are constructed from gleba shapefiles, which come from the SICOR. These files were given as wkt geometries in .csv format. I cleaned the raw files in STATA and removed outliers in GIS (see Appendix A). The clean file has unique contract identifier farm_id (which is a poor variable name because, as we will see, contracts do not map to farms uniquely). This file is stored in the clean data folder, under CREDIT_DATA/GLEBAS/glebas_matched_nomisreported. Land use rasters are stored in the raw data folder, under DEFORESTATION_DATA/Mapbiomas.

### 1. MAKE BUFFER 0: 
This file makes farm plot shapefiles, which I call buffer 0. It does so by dissolving all geometries that overlap in the clean SICOR gleba files, creating new identifiers, FID. It makes the file twice, one for the near-far specification (NF) and another for the 100m specification (100M). They are saved to folders CREDIT_DATA/GLEBAS/NF_BUFFERS/b0 and CREDIT_DATA/GLEBAS/100M_BUFFERS/b0 in the clean data folder, respectively. This takes about 1 hour.

### 2. MATCH FARM TO CONTRACT: 
This script take the b0 file created (which identifies unique farms with ID variable FID) and calculates its overlap with contract polygons to determine how many times a farm received credit and retreive its characteristics. It outputs a .csv file with variables farm_id (which is really the contract ID), FID (which is really the farm ID), and year. Saved as farm_to_contract in the clean data folder, under CREDIT_DATA/GLEBAS. This takes about 8 hours... for some cursed reason.

### 3. MAKE BUFFERS: 
Each of these files makes buffers from b0 at different distances for each specification (NF and 100M). They are saved to folders CREDIT_DATA/GLEBAS/**specification**_BUFFERS/b**distance** as b**distance**. The NF specification makes pairs (250-500, 500-1000, 750-1500, 1000-2000), and the 100M specification makes buffers at multiples of 100m until reaching 2000. One meter is approximated to 9.0785x10^-6 decimal degrees (see Appendix A). This takes 15 minutes for the NF specification, and 30 for the 100M specification.

### 4. MAKE RINGS:
These files convert buffers at all distances into disjoint rings by subtracting inner buffer overlap, for both specifications. They are saved to folders CREDIT_DATA/GLEBAS/**specification**_BUFFERS/b**distance** as b**distance**_ring. This runs in about 45m for the NF specification and 1h for the 100M specification.

### 5. REMOVE PROTECTED AREAS:
These files remove overlap with protected areas from all buffers (including b0), and both specifications. They are saved to folders CREDIT_DATA/GLEBAS/**specification**_BUFFERS/b**distance** as b**distance**_ring_prot. This runs in about 1h for the NF specification and 1.5h for the 100M specification.

### 6. ZONAL HISTOGRAM 1 (PROT):
These files compute zonal histograms for each buffer–year combination using Mapbiomas rasters. Each new variable represents a pixel count of all unique values from the raster, for each polygon. Output from this script is saved as several .csv files in the clean data folder, under DEFORESTATION_DATA/**specification**_BUFFERS/b**distance**. This takes about 1.5h for the NF specification and 3h for the 100M specification.

### 7. REMOVE PUBLIC LAND:

### 8. ZONAL HISTOGRAM 2 (PRIVATE):

### 9. STUVA CHECK (CROP OVERLAPPING, TREATED BUFFERS):

### 10. ZONAL HISTOGRAM 3 (STUVA):

### 11. MAKE BLOBS:

### 12. ZONAL HISTOGRAM 4 (BLOB):

### 13. GET FARM BLOB:

### 14. GET BUFFER STATE:

### 15. GET FARM CHARACTERISTICS (AREA, DISTANCE TO OTHER FARMS, TBD DISTANCE TO ROADS, DISTANCE TO URBAN AREAS, SLOPE):


### Path outline:
    CREDIT_DEFOREST
        CREDIT_DFOREST_DATA
            CREDIT_DEFOREST_DATA_CLEAN
                CREDIT_DATA
                    GLEBAS
                        NF_BUFFERS <-- buffer shapefiles are here, in their own folder each
                        100M_BUFFERS  <-- buffer shapefiles are here, in their own folder each
                        glebas_matched_nomisreported <-- clean gleba .csv lived here
                DEFORESTATION_DATA
                    NF_BUFFERS <-- zonal histogram csv files are saved here!
                    100M_BUFFERS <-- zonal histogram csv files are saved here!
            CREDIT_DEFOREST_DATA_RAW
                DEFORESTATION_DATA
                    Mapbiomas <-- land use files live here

## CLASSIFY CONTRACTS FOLDER
 This folder contains a script to re-classify credit contracts into cost and investment categories (see Theoretical Framework), edited but heavily written by ChatGPT. It uses a stricter definition for cost credit, discussed in the Appendix. It re-classifies 771590 contracts. The script inputs the contract file 'operacao_gleba_master', cleaned in STATA, and outputs a re-classified file, 'operacao_gleba_master_reclass'. Both are found in folder 'CREDIT_DATA/OPERACAO_GLEBA'. Run this script on the local terminal.

## (SOME) SUMMARY STATISTICS FOLDER
This folder contains SQL queries to obtain summary statistics included in Table 1 from several rounds of agricultural surveys. 