# early drafts, delete later

The most basic operation, a single tag value, uses the following

{
  type: "TagValue"
  osmt: "highway=residential"
}


---
{
  type: Concept,
  name: "low speed roads"
  mainExpression: {
    type: TagValue
    schemas: [
      "highway=residential",
      ...
    ]
}

---

{
  type: Concept,
  name: "low speed roads"
  mainExpression: {
    type: TagValue
    schemas: [
      "highway=residential",
      ...
    ]
}


[
  "highway=residential"
]

[
  "highway=residential", "access=yes"
]

[
  [ "highway=residential" ],
  [ "highway=service", "access=yes" ]
]
