# PROHOW Extractor
### Script to Extract Subsets and Simplified Versions from the PROHOW Multilingual Dataset


## Installation

- Download a copy of the [PROHOW Multilingual Dataset](https://www.kaggle.com/paolop/human-instructions-multilingual-wikihow) for all the languages you are interested in.
- Download the scripts from this repository and place them in the root directory where the Multilingual Dataset is stored.
- Make sure that Python is installed, and the following libraries are available:
  - `rdflib`

## Tutorial 1/2 - Basic Filters

### Overview of how to Configure and Run the Script

The first section of the `extract_specific_instruction_sets.py` script contains all the necessary configuration variables. Make sure that all the variables are initialised to their default values, except for the ones you want to use in the filtering.

After configuring the script, simply run the main script:
```
python extract_specific_instruction_sets.py
```

After the computation is finished, a new file `extracted_graph.ttl` will be generated in the root directory of the computation, and it will contain all the sets of instructions that passed the filter.

### Run a Language Based Filter

If you are interested only in certain languages, such as English and Spanish, add their language code to the `list_of_allowed_languages` configuration variable. The language code is made of the first two characters of all the database files for a given language. For example, to select English and Spanish, the following configuration can be used:

```
list_of_allowed_languages = ["en","es"]
```

This configuration will filter out language filenames which do not start with the given prefixes.

### Extract Specific Sets of Instructions

If you know the URLs of a specific set of wikiHow articles that you want to extract, you can create a file called `extract_specific_sets_instructions.txt`, and write one such URL per line, with no blank lines. Depending on the version of the dataset you are using, you might have to lowecase the URLs of the sets of instructions. You should then place this file in the same directory where you are running the script.

If the script finds this file, all the sets of instructions associated with the wikiHow articles listed in the file will be outputted.

### Extract Specific Categories

It is possible to limit the extractions to instructions that fall under specific categories. This can be done by modifying the list_of_allowed_languages variable in the extract_specific_instruction_sets.py script. More specifically, if this variable contains some values, the algorighm will select all the instructions which directly belong to one of the types defined in `list_of_allowed_categories` or any of their sub-classes. 

To consider sub-classes, they need to be defined as defined in RDFS in the Turtle file `class_hierarchy.ttl`. The class hierarchy file for the dataset you are using can be downlaoded from the [PROHOW Multilingual Dataset](https://www.kaggle.com/paolop/human-instructions-multilingual-wikihow) page.

The types/categories need to be added as URL strings in the list_of_allowed_languages list. For example, the following configuration extracts breakfast food instructions in Spanish and English: 

```
list_of_allowed_categories = ["http://www.wikihow.com/Category:Breakfast","http://es.wikihow.com/Categor%C3%ADa:Desayunos"]
```

## Tutorial 2/2 - SPARQL Filters

The configuration parameters defined here allow you to have more control over the type of instructions that you want to extract. In order to use these features, the `perform_sparql_filtering` variable must be set to True:
```
perform_sparql_filtering = True
```
