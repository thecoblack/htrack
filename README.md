Command line habit tracker. Why ? Because I was bored.

## Setup

Install the package

`pip install .`

The following command will create the necessary files in $HOME/.local/share/htrack

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
