# Task004: fix-floating-slabs

**Goal**: 检测并修复未关联 IfcBuildingStorey 的 IfcSlab

**Input**: IFC with slabs not contained in any storey
**Output**: IFC with all slabs in IfcRelContainedInSpatialStructure
**Constraint**: Each IfcSlab must have exactly one container
**Affected Classes**: IfcSlab, IfcBuildingStorey, IfcRelContainedInSpatialStructure
**Difficulty**: 1/5
**Frequency**: Medium
**Business Value**: 7/10
**Source**: BIMTester spatial containment rules; real IFC export issues

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
