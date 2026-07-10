# Task009: add-ifc-zone-definition

**Goal**: 将房间按部门分组为 IfcZone

**Input**: IFC with IfcSpace but no IfcZone
**Output**: IFC with zone hierarchy added
**Constraint**: Each zone must reference existing spaces
**Affected Classes**: IfcZone, IfcSpace, IfcRelAssignsToGroup
**Difficulty**: 3/5
**Frequency**: Low
**Business Value**: 7/10
**Source**: buildingSMART zone example; facility management

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
