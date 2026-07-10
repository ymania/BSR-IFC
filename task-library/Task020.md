# Task020: fix-ifc-openings-missing

**Goal**: 检测门窗开口未正确关联 IfcOpeningElement 的缺陷

**Input**: IFC with doors/windows but no opening elements
**Output**: IFC with IfcRelVoidsElement linking openings
**Constraint**: Each IfcDoor/IfcWindow must have a corresponding IfcOpeningElement
**Affected Classes**: IfcDoor, IfcWindow, IfcOpeningElement, IfcRelVoidsElement
**Difficulty**: 2/5
**Frequency**: High
**Business Value**: 9/10
**Source**: BIMTester rule; common Revit IFC export issue

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
