# Quesnet_vis
## Network data structure
### Node:
"id": randomly assigned; long enough to make sure there's no replication

"label": text shown in network

"feature": possible values are "central question","question", "unanswered question","answer". this determines the color and shape of the nodes in network

"content": more complete description of the node

"reference": shown as a floating card when the node is clicked on.

"properties": other properties may be useful for future functionality.

**question example**

{"id": "q23144958", "label":"how to measure curiosity?", "feature": "unanswered question","reference":[],"properties":{"answer":[],"N_answer":0}}


**answer example**

{"id": "a21402924", "label":"self-report from 1-3", "feature": "answer", "content": "asking the subject to report from keyboard", "reference":[{"abbr":Kemp et al},{"abbr": Celest et al}],"properties":{"details": "use either number or scrolls"}}

### Link:
example:

{"id": "l928371", "start":"q23144958", "end": "a21402924","label":"answer","properties":{}}
