# Task002: standardize-wall-types

**Goal**: 统一 IfcWall 的 IfcWallType 关联

**Input**: IFC with walls having no type assignment
**Output**: IFC with each wall linked to a IfcWallType
**Constraint**: All IfcWall must have IfcRelDefinesByType
**Affected Classes**: IfcWall, IfcWallType, IfcRelDefinesByType
**Difficulty**: 2/5
**Frequency**: High
**Business Value**: 8/10
**Source**: IfcOpenShell code examples; BIMTester common rules

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
