# Task003: set-walls-fire-rating

**Goal**: 为所有 IfcWall 添加 Pset_WallCommon.FireRating

**Input**: IFC with walls missing fire rating
**Output**: IFC with FireRating property on all walls
**Constraint**: FireRating must be one of: 0.5HR, 1HR, 2HR, 4HR
**Affected Classes**: IfcWall, IfcWallType
**Difficulty**: 2/5
**Frequency**: Medium
**Business Value**: 9/10
**Source**: buildingSMART IFC4 property sets; fire code compliance

## Description

*Task definition from real-world source. Implementation in BSR tasks/.*
