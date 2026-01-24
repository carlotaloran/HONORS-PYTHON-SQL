# --------------------------------------------------------------------------------------------
# This script processes the clen glebas csv from STATA and merges overlapping polygons to 
# create new farm IDs (buffer 0). Two shapefiles of b0 are saved, one to folder NF_BUFFERS
# and another to 100M_BUFFERS. Disjoint polygons are kept as separate features.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------






# Create variables to set working directory, buffer dictionary with buffer names and distance in decimal degrees, and universal input file
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/"
buffers_100 = {
    "100": 0.0009079,
    "200": 0.0018157,
    "300": 0.0027235,
    "400": 0.0036314,
    "500": 0.0045392,
    "600": 0.0054471,
    "700": 0.0063550,
    "800": 0.0072628,
    "900": 0.0081707,
    "1000": 0.0090785,
    "1100": 0.0099864,
    "1200": 0.0108942,
    "1300": 0.0118021,
    "1400": 0.0127099,
    "1500": 0.0136178,
    "1600": 0.0145256,
    "1700": 0.0154335,
    "1800": 0.0163413,
    "1900": 0.0172492,
    "2000": 0.018157
}
input_vector = f"{cd}b0/b0.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers_100:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b{b}/b{b}.shp"
    degrees = buffers_100[b]
    
    # Remove existing buffer file if it exists
    delete_shapefile(output_vector)

    # Make buffer
    processing.run(
        "native:buffer", 
        {
            'INPUT': input_vector,
            'DISTANCE':degrees,
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':False,
            'SEPARATE_DISJOINT':False,
            'OUTPUT': output_vector
        }
    )


# Create variables to set working directory, buffer dictionary with buffer names and distance in decimal degrees, and universal input file
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
buffers_nf = {
    "250": 0.00227,
    "500_1": 0.004539,
    "500_2": 0.004539,
    "750": 0.006809,
    "1000_1": 0.009079,
    "1000_2": 0.009079,
    "1500": 0.013618,
    "2000": 0.018157
}
input_vector = f"{cd}b0/b0.shp"


# --------------------------------------------------------------------------------------------
# Make buffers
# --------------------------------------------------------------------------------------------

for b in buffers_nf:
    # Define output file name and get distance from dictionary
    output_vector = f"{cd}b{b}/b{b}.shp"
    degrees = buffers_nf[b]
    
    # Remove existing buffer file if it exists
    delete_shapefile(output_vector)

    # Make buffer
    processing.run(
        "native:buffer", 
        {
            'INPUT': input_vector,
            'DISTANCE':degrees,
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':False,
            'SEPARATE_DISJOINT':False,
            'OUTPUT': output_vector
        }
    )


# Path and buffer pair definition
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/100M_BUFFERS/"
buffer_pairs = [
    ("b0", "b100"),
    ("b100", "b200"),
    ("b200", "b300"),
    ("b300", "b400"),
    ("b400", "b500"),
    ("b500", "b600"),
    ("b600", "b700"),
    ("b700", "b800"),
    ("b800", "b900"),
    ("b900", "b1000"),
    ("b1000", "b1100"),
    ("b1100", "b1200"),
    ("b1200", "b1300"),
    ("b1300", "b1400"),
    ("b1400", "b1500"),
    ("b1500", "b1600"),
    ("b1600", "b1700"),
    ("b1700", "b1800"),
    ("b1800", "b1900"),
    ("b1900", "b2000")
]


# --------------------------------------------------------------------------------------------
# Make rings
# --------------------------------------------------------------------------------------------
for inner, outer in buffer_pairs:

    inner_path = f"{cd}{inner}/{inner}.shp"
    outer_path = f"{cd}{outer}/{outer}.shp"

    inner_fixed = f"{cd}{inner}/{inner}_fixed.shp"
    outer_fixed = f"{cd}{outer}/{outer}_fixed.shp"

    ring_path = f"{cd}{outer}/{outer}_ring.shp"

    # Clean old files
    for f in [inner_fixed, outer_fixed, ring_path]:
        delete_shapefile(f)

    # Fix geometries
    processing.run("native:fixgeometries", {
        'INPUT': inner_path,
        'METHOD': 1,
        'OUTPUT': inner_fixed
    })

    processing.run("native:fixgeometries", {
        'INPUT': outer_path,
        'METHOD': 1,
        'OUTPUT': outer_fixed
    })

    # Skip any remaining invalid features
    inner_src = QgsProcessingFeatureSourceDefinition(
        inner_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    outer_src = QgsProcessingFeatureSourceDefinition(
        outer_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # b*_ring = b* − b(previous)
    processing.run("native:difference", {
        'INPUT': outer_src,
        'OVERLAY': inner_src,
        'OUTPUT': ring_path
    })

    # Delete helper files
    delete_shapefile(inner_fixed)
    delete_shapefile(outer_fixed)


# Path and buffer pair definition
cd = "/zfs/students/cloranlo/Downloads/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/GLEBAS/FARMS/NF_BUFFERS/"
buffer_pairs = [
    ("b0", "b250"),
    ("b250", "b500_1"),
    ("b0", "b500_2"),
    ("b500_2", "b1000_1"),
    ("b0", "b750"),
    ("b750", "b1500"),
    ("b0", "b1000_2"),
    ("b1000_2", "b2000")
]


# --------------------------------------------------------------------------------------------
# Build rings
# --------------------------------------------------------------------------------------------

for inner, outer in buffer_pairs:

    inner_path = f"{cd}{inner}/{inner}.shp"
    outer_path = f"{cd}{outer}/{outer}.shp"

    inner_fixed = f"{cd}{inner}/{inner}_fixed.shp"
    outer_fixed = f"{cd}{outer}/{outer}_fixed.shp"

    ring_path = f"{cd}{outer}/{outer}_ring.shp"

    # Clean old files
    for f in [inner_fixed, outer_fixed, ring_path]:
        delete_shapefile(f)

    # Fix geometries
    processing.run("native:fixgeometries", {
        'INPUT': inner_path,
        'METHOD': 1,
        'OUTPUT': inner_fixed
    })

    processing.run("native:fixgeometries", {
        'INPUT': outer_path,
        'METHOD': 1,
        'OUTPUT': outer_fixed
    })

    # Skip any remaining invalid features
    inner_src = QgsProcessingFeatureSourceDefinition(
        inner_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    outer_src = QgsProcessingFeatureSourceDefinition(
        outer_fixed,
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid
    )

    # Take difference 
    processing.run("native:difference", {
        'INPUT': outer_src,
        'OVERLAY': inner_src,
        'OUTPUT': ring_path
    })

    # Remove helper files
    delete_shapefile(inner_fixed)
    delete_shapefile(outer_fixed)


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