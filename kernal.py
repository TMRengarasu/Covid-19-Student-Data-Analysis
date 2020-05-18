# Name: kernal.py
# Description: Kernel Interpolation with Barriers is a moving window predictor
#   that uses non-Euclidean distances.
# Requirements: Geostatistical Analyst Extension

# Import system modules
import arcpy
# Use half of the cores on the machine
arcpy.env.parallelProcessingFactor = "66%"

arcpy.env.coincidentPoints = "MAX"

print("import arcpy")
# Set environment settings
arcpy.env.workspace = "F:/Backup/E/localgis/trunk/Science Faculty/Fulldata/New File Geodatabase.gdb"

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True


print("Set environment settings done!!")
# Set local variables
inPointFeatures = "Student_Data_Mobitel"
zField = "InterNet_Full_Code"
outLayer = "outKIWB1"
outRaster = "Out_Mobitel"
cellSize = 250.00
inBarrier = "Barrier_simplified"
kernelFunction = "GAUSSIAN"
bandwidth = "3500"
power = ""
ridgeParam = "50"
outputType = "PREDICTION"
print("parameters set")
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
print("CheckOut GeoStats Extension Successful")
# Execute KernelInterpolationWithBarriers
arcpy.KernelInterpolationWithBarriers_ga(inPointFeatures, zField, outLayer, outRaster,
                                         cellSize, inBarrier, kernelFunction, bandwidth,
                                         power, ridgeParam, outputType)
                                         
print("Done 1")



# Set local variables
in_geostat_layer = outLayer
contour_type = "Filled_contour"
out_feature_class = "Mobitel_1"
contour_quality = "Presentation"
classification_type = "Manual"
classes_count = ""
classes_breaks = [-3,-2,-1,0,1,2,100]

# Execute GALayerToContour
arcpy.GALayerToContour_ga(in_geostat_layer, contour_type, out_feature_class,
                          contour_quality, classification_type, classes_count,
                          classes_breaks)

print("Done 2")

in_features=out_feature_class
clip_features="Join_Output_full_selection"
clip_out_feature_class="F:/Backup/E/localgis/trunk/Science Faculty/Fulldata/Mobitel/Mobitel1/Mobitel1_Clip.shp"
cluster_tolerance=""


# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Mobitel5_Clip", "Join_Output_full selection"
arcpy.Clip_analysis(in_features, clip_features, clip_out_feature_class, cluster_tolerance)


print("Done Clip_analysis")
