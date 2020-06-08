# Name: KernelInterpolationWithBarriers_Example_02.py
# Description: Kernel Interpolation with Barriers is a moving window predictor
#   that uses non-Euclidean distances.
# Requirements: Geostatistical Analyst Extension

# Import system modules
import arcpy, os,shutil
# Use half of the cores on the machine
arcpy.env.parallelProcessingFactor = "66%"

arcpy.env.coincidentPoints = "MAX"

print("import arcpy")
# Set environment settings
arcpy.env.workspace = r"F:/Backup/E/localgis/trunk/Science Faculty/Fulldata/StudentData.gdb"

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

# Input parameters
ISP = sys.argv[1]
bandwidth =  sys.argv[2]

directory=os.getcwd()

de=os.path.join(directory,"outputs")
outfile= os.path.join(de,ISP,ISP+bandwidth+".shp")




if os.path.exists(os.path.join(de,ISP)):
    print ("File exist")
else:
    print ("File not exist")
    os.mkdir(os.path.join(de,ISP))



def buildWhereClause(table, field, value):
    """Constructs a SQL WHERE clause to select rows having the specified value
    within a given field and table."""

    # Add DBMS-specific field delimiters
    fieldDelimited = arcpy.AddFieldDelimiters(table, field)

    # Determine field type
    fieldType = arcpy.ListFields(table, field)[0].type

    # Add single-quotes for string field values
    if str(fieldType) == 'String':
        value = "'%s'" % value

    # Format WHERE clause
    whereClause = "%s = %s" % (fieldDelimited, value)
    return whereClause




def searchISP(strISP):
    if strISP =="All":
        whereClause=""
    elif strISP =="4G":
        whereClause= '"ISPTYPE" LIKE'+"'%s%%'"% strISP 
        out_feature_class = "FourG_IS"         
    else:
        whereClause= '"ISP" LIKE'+"'%s%%'"% strISP
        out_feature_class = strISP+"_IS"        
    return whereClause, out_feature_class


strISP=str(ISP)    
searchword=searchISP(strISP)

print("Set environment settings done!!")

#Select only one ISP locations and create a FC called KM_points
inputfc ="Final_Data/Student_Data_Full_f"
selectedISP ="ISPSelected"
fieldname = "ISP"
#fieldvalue = ISP+
#whereclause = buildWhereClause(inputfc, fieldname, fieldvalue)
#whereclause = '"' + fieldname + '" = ' + "'" + str(ISP) + '" % ' +"'"

whereclause=searchword[0]
arcpy.Select_analysis(inputfc, selectedISP, whereclause)





# Set local variables

zField = "InterNet_Full_Code"
outLayer = "outKIWB1"
outRaster = "Out_"+strISP
cellSize = 250.00
inBarrier = "Barrier_simplified"
kernelFunction = "GAUSSIAN"
out_feature_class=searchword[1]
power = ""
ridgeParam = "50"
outputType = "PREDICTION"
print("parameters set")
# Check out the ArcGIS Geostatistical Analyst extension license
arcpy.CheckOutExtension("GeoStats")
print("CheckOut GeoStats Extension Successful")
# Execute KernelInterpolationWithBarriers
arcpy.KernelInterpolationWithBarriers_ga(selectedISP, zField, outLayer, outRaster,
                                         cellSize, inBarrier, kernelFunction, bandwidth,
                                         power, ridgeParam, outputType)
                                         
print("Done 1")



# Set local variables
in_geostat_layer = outLayer
contour_type = "Filled_contour"

contour_quality = "Presentation"
classification_type = "Manual"
classes_count = ""
classes_breaks = [-2,-1,0,1,2,10000]

# Execute GALayerToContour
arcpy.GALayerToContour_ga(in_geostat_layer, contour_type, out_feature_class,
                          contour_quality, classification_type, classes_count,
                          classes_breaks)

print("Done 2")

expression = "roadClass(!Value_Max!)" 
codeblock = """def roadClass(type):
    if type == 10000:
        return "3"
    else:
        return type"""


# Execute CalculateField 
arcpy.CalculateField_management(out_feature_class, "Value_Max", expression, "PYTHON", codeblock) 






in_features=out_feature_class
clip_features="Join_Output_full_selection"
clip_out_feature_class=outfile
cluster_tolerance=""


# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Mobitel5_Clip", "Join_Output_full selection"
arcpy.Clip_analysis(in_features, clip_features, clip_out_feature_class, cluster_tolerance)


print("Done Clip_analysis")
print("Final file can be found at " +str(outfile))