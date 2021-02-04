# Instance objects in a curve.
# Distribute by bbox size
#
#
# Author: Giuliano Franca
# 
# Usage:
# Select first the source object than the curve and run the script. Change
# the aimAxis and upAxis on the script
#
#
#
#
#
import math
import maya.cmds as cmds
import maya.api.OpenMaya as om2

########################################################################
############################## EDIT HERE! ##############################
########################################################################

aimAxis = "Y"
upAxis = "Z"

########################################################################
############################# END EDIT HERE ############################
########################################################################

# Get selection
selList = om2.MGlobal.getActiveSelectionList()
if selList.length() != 2:
    raise RuntimeError("Select first the source object than the curve.")

# Get curve obj and shape paths
curvePath = selList.getDagPath(1)
if not curvePath.node().hasFn(om2.MFn.kTransform):
    raise RuntimeError("Select the transform node of the curve.")
curveShapePath = om2.MDagPath(curvePath)
curveShapePath.extendToShape()
if not curveShapePath.node().hasFn(om2.MFn.kNurbsCurve):
    raise RuntimeError("Select an NURBS curve as curve object.")

# Get the original obj and shape paths
origPath = selList.getDagPath(0)
if not origPath.node().hasFn(om2.MFn.kTransform):
    raise RuntimeError("Select the transform node of the source object.")
origShapePath = om2.MDagPath(origPath)
origShapePath.extendToShape()
if origShapePath.node().hasFn(om2.MFn.kMesh):
    # Get object width, height and depth
    origMtx = origPath.inclusiveMatrix()
    dagFn = om2.MFnDagNode(origShapePath)
    objBBox = dagFn.boundingBox
    objWidth = objBBox.width * origMtx[0]
    objHeight = objBBox.height * origMtx[5]
    objDepth = objBBox.depth * origMtx[10]
elif origShapePath.node().hasFn(om2.MFn.kPluginShape):
    # Get object width, height and depth
    origMtx = origPath.inclusiveMatrix()
    shapeMob = origShapePath.node()
    nodeFn = om2.MFnDependencyNode(shapeMob)
    minValues = []
    maxValues = []
    for i in range(3):
        curPlug = nodeFn.findPlug("MinBoundingBox%s" % i, False)
        curValue = curPlug.asFloat()
        minValues.append(curValue)
    for i in range(3):
        curPlug = nodeFn.findPlug("MaxBoundingBox%s" % i, False)
        curValue = curPlug.asFloat()
        maxValues.append(curValue)
    minPnt = om2.MPoint(minValues)
    maxPnt = om2.MPoint(maxValues)
    objBBox = om2.MBoundingBox(minPnt, maxPnt)
    objWidth = objBBox.width * origMtx[0]
    objHeight = objBBox.height * origMtx[5]
    objDepth = objBBox.depth * origMtx[10]
else:
    raise RuntimeError("Select an polygon mesh or plugin shape as source object.")
srcObj = origPath.fullPathName()

# Get the aim axis
if aimAxis.upper() == "X":
    aimAxis = om2.MVector.kXaxisVector
elif aimAxis.upper() == "Y":
    aimAxis = om2.MVector.kYaxisVector
elif aimAxis.upper() == "Z":
    aimAxis = om2.MVector.kZaxisVector
else:
    raise RuntimeError("Aim axis don't recognized. Please choose one between 'X', 'Y' or 'Z'.")

# Get the up axis
if upAxis.upper() == "X":
    upAxis = om2.MVector.kXaxisVector
elif upAxis.upper() == "Y":
    upAxis = om2.MVector.kYaxisVector
elif upAxis.upper() == "Z":
    upAxis = om2.MVector.kZaxisVector
else:
    raise RuntimeError("Up axis don't recognized. Please choose one between 'X', 'Y' or 'Z'.")

# Check if the aim axis is equal to up axis
if aimAxis == upAxis:
    raise RuntimeError("Aim axis is the same of up axis.")

# Get the size
binormalAxis = aimAxis ^ upAxis
if binormalAxis.x != 0.0:
    size = objWidth
elif binormalAxis.y != 0.0:
    size = objHeight
else:
    size = objDepth

# Get curve info
curveFn = om2.MFnNurbsCurve(curveShapePath)
curveArcLen = curveFn.length()

# Get the step distance
numInstances = int(math.floor(curveArcLen / size))
moduloLen = curveArcLen - ((numInstances - 1) * size)
moduloLenHalf = moduloLen / 2.0

for i in range(numInstances):
    # Get the curve U param for the current object
    curLen = i * size + moduloLenHalf
    param = curveFn.findParamFromLength(curLen)

    # Get the transformation values for the current object
    pos = curveFn.getPointAtParam(param, om2.MSpace.kWorld)
    tangent = curveFn.tangent(param, om2.MSpace.kWorld).normalize()
    upVector = om2.MVector(0.0, 1.0, 0.0)
    aim = tangent ^ upVector
    aim.normalize()
    normal = aim ^ tangent
    normal.normalize()
    qBasis = om2.MQuaternion()
    qAim = om2.MQuaternion(aimAxis, aim)
    qBasis *= qAim
    secAxis = upAxis.rotateBy(qAim)
    angle = secAxis.angle(normal)
    qNormal = om2.MQuaternion(angle, aim)
    if not normal.isEquivalent(secAxis.rotateBy(qNormal), 1.0e-5):
        angle = 2.0 * math.pi - angle
        qNormal = om2.MQuaternion(angle, aim)
    qBasis *= qNormal
    rot = qBasis.asEulerRotation()
    rot = [
        om2.MAngle(rot.x).asDegrees(),
        om2.MAngle(rot.y).asDegrees(),
        om2.MAngle(rot.z).asDegrees()
    ]

    # Create an instance of the original obj and apply the transformation
    instObj = cmds.instance(srcObj, n="%sInstance1" % srcObj, lf=True)[0]
    cmds.xform(instObj, t=(pos.x, pos.y, pos.z), ro=(rot[0], rot[1], rot[2]))