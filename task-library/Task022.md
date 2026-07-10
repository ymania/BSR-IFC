# Task022: duplicate-guid-fix

**Goal**: 修复重复 GUID（已有 BSR task）

**Input**: IFC with duplicate GlobalId
**Output**: IFC with all GUIDs unique
**Constraint**: GlobalId must be unique across file
**Affected Classes**: All entities
**Difficulty**: 1/5
**Frequency**: Low
**Business Value**: 9/10
**Source**: IfcOpenShell validation; buildingSMART IDs spec

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
