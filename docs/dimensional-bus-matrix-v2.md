# Planning

> 1 star (Movie details), make use of bridge tables and agregations (e.g.: genre and year) to increase complexity

## 1. Dimensional Bus Matrix

| Fact Table    | Date | Movie | Keyword | Director | Writer | Genre | Actor |
| ---           | ---- | ----- | ------- | -------- | ------ | ----- | ----- |
| Movie Details | X    | X     | X       | X        | X      | X     | X     |

## 2. Dimensions Dictionary

- **Date**:
- **Movie**:
- **Keyword**:
- **Director**:
- **Writer**: 
- **Genre**: 
- **Actor**: 

## 3. Facts Dictionary

- **Movie Details Fact Table**:

## 4. Bridge Tables (not defined on matrix)

- MovieCast: connects the movies with it's top 5 cast
- MovieKeywords: connects the movies with it's keyword
- MovieGenres: connects the movies with it's genres

## 5. Agregation Star (?)
