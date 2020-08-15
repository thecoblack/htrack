Command line habit tracker. Why ? Because I was bored.

## Setup

Install the package

`pip install .`

The following command will create the necessary files.

`htrack setup`

## Usage 

Create new habit

`htrack habits -n newhabit`

Mark as complete habit today.

`htrack habits -c newhabit`

List all your habits

`htrack habits -l`

Show a timeline of your progress the last days

`htrack habits timeline`

```
                8/9     8/10    8/11    8/12    8/13    8/14    8/15
Watch naruto            X       X                                        
Pray to harambe                                 X       X       X        
Wake up         X       X               X       X       X       X
```

Show a plot of your progress the last days

`htrack habits plot`

