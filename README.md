# aid-lab-assignment

## Guidelines 

### Discussion
2024-01-14 14:00 B102

### Goals
To design a data warehouse, implement it, and exemplify its use.

### Workgroups
The assignment must be performed in groups of 3 to 4 members.

### Subject
The subject of the assignment is chosen by the group. However, it must comply to, at least, the following rules:

- The number of facts must be over 10000 with, at least, one additive measure. Ex: electricity consumption, sales, phone calls, product composition cost, distance or price in transport companies or highways, number of votes, etc.
- There must be aggregated facts or snapshots with at least one semi-additive measure.
- There must be at least 4 dimensions, one of which temporal, and some of them are common to both kinds of facts.

The assignment subject must be approved by the professor, who if need arises, may suggest a subject.

### Report
The report includes the following parts, corresponding to the work to be developed:

1. Subject description. Assignment requirements.
2. Planning: dimensional bus matrix, dimensions and facts dictionary. [Docs](./docs/dimensional-bus-matrix)
3. Dimensional data model ([explained](./docs/dimensional-model/diagram.md)). [Image](./docs/dimensional-model/diagram.png)
4. Data sources selection. Extraction, transformation and loading.
5. Querying and data analysis.
6. Critical reflection about the advantages and short comes with respect to the operational databases.
7. Conclusion.