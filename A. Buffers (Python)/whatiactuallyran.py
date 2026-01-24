# --------------------------------------------------------------------------------------------
# This script processes the clen glebas csv from STATA and merges overlapping polygons to 
# create new farm IDs (buffer 0). Two shapefiles of b0 are saved, one to folder NF_BUFFERS
# and another to 100M_BUFFERS. Disjoint polygons are kept as separate features.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------


















# Path and buffer list definitions
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/"
protected = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/Brazil_UCS/brazil_UCS_fixed.shp"
buffers = [
    "b0",
    "b100",
    "b200",
    "b300",
    "b400",
    "b500",
    "b600",
    "b700",
    "b800",
    "b900",
    "b1000",
    "b1100",
    "b1200",
    "b1300",
    "b1400",
    "b1500",
    "b1600",
    "b1700",
    "b1800",
    "b1900",
    "b2000"
]


# --------------------------------------------------------------------------------------------
# Clean buffers
# --------------------------------------------------------------------------------------------

# Protected area geometry fix
protected_src = QgsProcessingFeatureSourceDefinition(
    protected,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)

# Difference
for b in buffers:

    input_vector = (
        f"{cd}{b}/{b}.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring.shp"
    )

    fixed_vector = (
        f"{cd}{b}/{b}_fixed.shp" if b == "b0"
        else f"{cd}{b}/{b}_fixed_ring.shp"
    )
    
    output_vector = (
        f"{cd}{b}/{b}_prot.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring_prot.shp"
    )

    # Cleanup old outputs
    for s in [fixed_vector, output_vector]:
        delete_shapefile(s)

    # Fix buffer/ring geometry
    processing.run("native:fixgeometries", {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
    })

    fixed_src = QgsProcessingFeatureSourceDefinition(
        fixed_vector,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # Remove protected areas
    processing.run("native:difference", {
        'INPUT': fixed_src,
        'OVERLAY': protected_src,
        'OUTPUT': output_vector
    })

    # Delete temp file
    delete_shapefile(fixed_vector)


# Path and buffer definitions
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
protected = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/SHAPEFILES/Brazil_UCS/brazil_UCS_fixed.shp"
buffers = [
    "b0",
    "b250",
    "b500_1",
    "b500_2",
    "b750",
    "b1000_1",
    "b1000_2",
    "b1500",
    "b2000"
]


# --------------------------------------------------------------------------------------------
# Clean buffers
# --------------------------------------------------------------------------------------------

# Protected area geometry fix
protected_src = QgsProcessingFeatureSourceDefinition(
    protected,
    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
)

# Difference
for b in buffers:

    input_vector = (
        f"{cd}{b}/{b}.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring.shp"
    )

    fixed_vector = (
        f"{cd}{b}/{b}_fixed.shp" if b == "b0"
        else f"{cd}{b}/{b}_fixed_ring.shp"
    )
    
    output_vector = (
        f"{cd}{b}/{b}_prot.shp" if b == "b0"
        else f"{cd}{b}/{b}_ring_prot.shp"
    )

    # Remove old outputs
    for s in [fixed_vector, output_vector]:
        delete_shapefile(s)

    # Fix buffer/ring geometry
    processing.run("native:fixgeometries", {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
    })

    fixed_src = QgsProcessingFeatureSourceDefinition(
        fixed_vector,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # Remove protected areas
    processing.run("native:difference", {
        'INPUT': fixed_src,
        'OVERLAY': protected_src,
        'OUTPUT': output_vector
    })

    # Remove temp file
    delete_shapefile(fixed_vector)


# Create variables to set working directory, year, and buffer lists
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/"
years = range(2016, 2025)
buffers = [
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "1000",
    "1100",
    "1200",
    "1300",
    "1400",
    "1500",
    "1600",
    "1700",
    "1800",
    "1900",
    "2000"
]


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for all buffers > 0
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Fix geometries
    input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/b{b}/b{b}_ring_prot.shp"
    fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/b{b}/b{b}_ring_prot_fixed.shp"

    # Delete old fixed shapefile if it exists
    if os.path.exists(fixed_vector):
        os.remove(fixed_vector)

    processing.run(
        "native:fixgeometries",
        {
            'INPUT': input_vector,
            'METHOD': 1,
            'OUTPUT': fixed_vector
        }
    )
    
    # Zonal histogram for each year
    for y in years:
        input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
        output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/100M_BUFFERS/b{b}/b{b}_cover{y}_prot.csv"

        # Delete old csv if it exists
        if os.path.exists(output_csv):
            os.remove(output_csv)

        processing.run(
            "native:zonalhistogram",
            {
                'INPUT_RASTER': input_raster,
                'RASTER_BAND': 1,
                'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                    fixed_vector,
                    selectedFeaturesOnly=False,
                    featureLimit=-1,
                    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
                ),
                'COLUMN_PREFIX': 'HISTO_',
                'OUTPUT': output_csv
            }
        )
    
    # Remove helper fixed vector file
    delete_shapefile(fixed_vector)


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for buffer = 0
# --------------------------------------------------------------------------------------------

# Fix geometries
input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/b0/b0_prot.shp"
fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/b0/b0_prot_fixed.shp"

# Delete old fixed shapefile if it exists
if os.path.exists(fixed_vector):
    os.remove(fixed_vector)

# Fix
processing.run(
    "native:fixgeometries",
        {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
        }
)
    
# Zonal histogram for each year
for y in years:
    input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
    output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/100M_BUFFERS/b0/b0_cover{y}_prot.csv"

    # Delete old CSV if it exists
    if os.path.exists(output_csv):
        os.remove(output_csv)

    processing.run(
        "native:zonalhistogram",
        {
            'INPUT_RASTER': input_raster,
            'RASTER_BAND': 1,
            'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                fixed_vector,
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
            ),
            'COLUMN_PREFIX': 'HISTO_',
            'OUTPUT': output_csv
        }
    )
            
# Delete helper file
delete_shapefile(fixed_vector)



# Create variables to set working directory, year, and buffer lists
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/"
years = range(2016, 2025)
buffers = ["250", "500_1", "500_2", "1000_1", "750", "1500", "1000_2", "2000"]


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for all buffers > 0
# --------------------------------------------------------------------------------------------

for b in buffers:
    # Fix geometries
    input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b{b}/b{b}_ring_prot.shp"
    fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b{b}/b{b}_ring_prot_fixed.shp"

    # Delete old fixed shapefile if it exists
    if os.path.exists(fixed_vector):
        os.remove(fixed_vector)

    processing.run(
        "native:fixgeometries",
        {
            'INPUT': input_vector,
            'METHOD': 1,
            'OUTPUT': fixed_vector
        }
    )
    
    # Zonal histogram for each year
    for y in years:
        input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
        output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/NF_BUFFERS/b{b}/b{b}_cover{y}_prot.csv"

        # Delete old csv if it exists
        if os.path.exists(output_csv):
            os.remove(output_csv)

        processing.run(
            "native:zonalhistogram",
            {
                'INPUT_RASTER': input_raster,
                'RASTER_BAND': 1,
                'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                    fixed_vector,
                    selectedFeaturesOnly=False,
                    featureLimit=-1,
                    flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                    geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
                ),
                'COLUMN_PREFIX': 'HISTO_',
                'OUTPUT': output_csv
            }
        )
    
    # Remove helper fixed vector file
    delete_shapefile(fixed_vector)


# --------------------------------------------------------------------------------------------
# Fix geometries and calculate histogram for buffer = 0
# --------------------------------------------------------------------------------------------

# Fix geometries
input_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0/b0_prot.shp"
fixed_vector = f"{cd}DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/b0/b0_prot_fixed.shp"

# Delete old fixed shapefile if it exists
if os.path.exists(fixed_vector):
    os.remove(fixed_vector)

# Fix
processing.run(
    "native:fixgeometries",
        {
        'INPUT': input_vector,
        'METHOD': 1,
        'OUTPUT': fixed_vector
        }
)
    
# Zonal histogram for each year
for y in years:
    input_raster = f"{cd}DATA_RAW/DEFORESTATION/Mapbiomas/{y}_cover.tif"
    output_csv = f"{cd}DATA_CLEAN/DEFORESTATION/FARMS/NF_BUFFERS/b0/b0_cover{y}_prot.csv"

    # Delete old CSV if it exists
    if os.path.exists(output_csv):
        os.remove(output_csv)

    processing.run(
        "native:zonalhistogram",
        {
            'INPUT_RASTER': input_raster,
            'RASTER_BAND': 1,
            'INPUT_VECTOR': QgsProcessingFeatureSourceDefinition(
                fixed_vector,
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
            ),
            'COLUMN_PREFIX': 'HISTO_',
            'OUTPUT': output_csv
        }
    )
            

delete_shapefile(fixed_vector)