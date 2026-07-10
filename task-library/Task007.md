# Task007: rename-doors-by-room

**Goal**: 按关联房间名自动命名 IfcDoor

**Input**: IFC with doors named 'Door-001'
**Output**: IFC with doors named 'R-Office-D01' pattern
**Constraint**: Door name must include room name prefix
**Affected Classes**: IfcDoor, IfcSpace, IfcRelSpaceBoundary
**Difficulty**: 2/5
**Frequency**: High
**Business Value**: 8/10
**Source**: BIM mandate naming conventions; common handover requirement

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
