# Task014: auto-name-classrooms

**Goal**: 将教学楼 IfcSpace 按'楼号-楼层-编号'规则重命名

**Input**: IFC with school spaces named 'Room'
**Output**: IFC with spaces named 'A-1-01' pattern
**Constraint**: Name must match regex: ^[A-Z]-\d+-\d{2}$
**Affected Classes**: IfcSpace, IfcBuildingStorey
**Difficulty**: 1/5
**Frequency**: High
**Business Value**: 8/10
**Source**: buildingSMART school example; education BIM mandate

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
