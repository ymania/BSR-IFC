#!/usr/bin/env python3
"""Baseline all real IFC files in examples/ifc/"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import ifcopenshell
from core.constraint.engine import ConstraintEngine
from core.constraint.geometric import DepthRangeRule, GeometryExistsRule
from core.constraint.topological import ElementHasParentRule

ifc_dir = os.path.join(os.path.dirname(__file__), '..', 'examples/ifc')
baseline_path = os.path.join(os.path.dirname(__file__), '..', 'examples/ifc-baseline.json')
baseline = []
TYPES = ['IfcWall','IfcSlab','IfcDoor','IfcWindow','IfcSpace','IfcBeam','IfcColumn',
         'IfcPile','IfcFlowSegment','IfcBuildingElementProxy','IfcRoof','IfcStair',
         'IfcBridge','IfcRoad','IfcRailway']

for root, dirs, files in os.walk(ifc_dir):
    for f in sorted(files):
        if not f.endswith('.ifc'):
            continue
        path = os.path.join(root, f)
        rel = os.path.relpath(path, ifc_dir)
        m = ifcopenshell.open(path)
        
        info = {"file": rel, "schema": m.schema, "entities": len(list(m)), "types": {}}
        for t in TYPES:
            try:
                n = len(list(m.by_type(t)))
                if n:
                    info["types"][t] = n
            except RuntimeError:
                pass  # type not in schema (e.g. IfcBridge in IFC4)
        
        eng = ConstraintEngine()
        eng.register(DepthRangeRule())
        eng.register(GeometryExistsRule())
        eng.register(ElementHasParentRule())
        results = eng.check_all(m)
        s = eng.summary(results)
        info["check"] = {"passed": s["passed"], "total": s["total"], "pass": s["passed_all"]}
        fails = [{"rule": r.rule, "element": r.element_id, "msg": r.message} for r in results if not r.passed]
        if fails:
            info["check"]["fails"] = fails
        
        baseline.append(info)
        print(f"[{len(baseline)}] {rel}  ({m.schema}, {len(list(m))} entities, check {s['passed']}/{s['total']})")

with open(baseline_path, 'w') as f:
    json.dump(baseline, f, indent=2)
print(f"\nDone. {len(baseline)} files baselined.")
