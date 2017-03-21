# PROHOW Extractor

A script to extract subsets and simplified versions from the PROHOW Multilingual Dataset.

## Installation

- Download a copy of the [PROHOW Multilingual Dataset](https://www.kaggle.com/paolop/human-instructions-multilingual-wikihow) for all the languages you are interested in.
- Download the scripts from this repository and place them in the root directory where the Multilingual Dataset is stored.
- Make sure that Python is installed, and the following libraries are available:
  - `rdflib`
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) (optional, required only for the `parse_html_into_text` feature)

## Quick Start

If you want to quickly get a simplified version of the dataset to work with, after following the installation, copy the following configuration variables:
```
perform_sparql_filtering = True
remove_multiple_methods = True
remove_multiple_requirements = True
save_simplified = True
parse_html_into_text = True
```
just before this line in file `extract_specific_instruction_sets.py`:
```
# CODE START
``` 

Then run the main script:

```
python extract_specific_instruction_sets.py
```

When the computation finishes, the file `extracted_simplified_graph.ttl` will contain all the instructions for the language files you have downloaded in a simplified format:
 - Sets of instructions of type `prohow:instruction_set` containing
   - A list of labelled steps (linked with the `prohow:has_step` relation.)
   - A list of labeleld requirements (linked with the `prohow:requires` relation.)
   - The order between the steps (linked with the `prohow:requires` relation.)
   - The set of associated web-pages (linked with the `owl:sameAs` relation.)
   - A language identified linked with the `prohow:language` relation

NOTE: the generated file might become quite big if you run it on multiple languages at once, so you might want to run it on a few languages or language files at a time.

## Tutorial 1/3 - Basic Filters

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

## Tutorial 2/3 - SPARQL Filters

The configuration parameters defined here allow you to have more control over the type of instructions that you want to extract. In order to use these features, the `perform_sparql_filtering` variable must be set to True:
```
perform_sparql_filtering = True
```

### Remove Instructions with Composite Requirements and Methods

Certain sets of instructions contain multiple methods or sets of requirements. This additional level of detail might be useful to some, but it might make computation more difficult. If you want to work with simpler sets of instructions, which can be represented as a single list of requirements and a single ordered list of steps, then follow these steps:

If you don't want to have instructions that contain multiple methods, change the value of variable `remove_multiple_methods` to true:

```
remove_multiple_methods = True
```

If you don't want to have instructions that contain multiple sets of requirements, change the value of variable `remove_multiple_requirements` to true:

```
remove_multiple_requirements = True
```

### Limit the Number of Steps and Requirements

If the variable `min_number_of_steps` is greater than -1, instructions with less steps than this number are filtered out.
If the variable `max_number_of_steps` is greater than -1, instructions with more steps than this number are filtered out.
If the variable `min_number_of_requirements` is greater than -1, instructions with less requirements than this number are filtered out.
If the variable `max_number_of_requirements` is greater than -1, instructions with more requirements than this number are filtered out.

For example, if we want instructions with at least 3 but no more than 7 steps, and with at least 5 requirements, we can configure those variables as follows:
```
min_number_of_steps = 3
max_number_of_steps = 7
min_number_of_requirements = 5
max_number_of_requirements = -1
```

### Limit to Multilingual Instructions

If you are only interested in instructions that have an equivalent version in a specific language, you can configure the `owl_sameAs_required_prefixes` variable. If you want to use this feature, this variable should be a list containing pairs of URL prefixes that are associated with each pair of languages you are interested in.

For example, if you want to select only English or Spanish sets of instructions which have an English or Spanish equivalent version, then you can configure this parameter as follows:

```
owl_sameAs_required_prefixes = [["http://es.wikihow.com/","http://www.wikihow.com/"]]
```

## Tutorial 3/3 Simplified Data Output

The multilingual dataset contains many features which make the representation richer, but can also be confusing to a first time user. If you are only interested in instructions represented with one single list of requirements, and one single list of steps, then follow these instructions to extract data in a simplified format.

First of all, you need to enable the simplified output variable `save_simplified`:

```
save_simplified = True
```

It is advised that you start by setting these variables to true:

```
remove_multiple_methods = True
remove_multiple_requirements = True
```

### Remove HTML Code from Labels

If you want labels in plain text, without the related HTML code surrounding it, then set variable `parse_html_into_text` to true:

```
parse_html_into_text = True
```

### Unify Abstract and Label

Entities typically have a shorter description under property `rdfs:label` and a longer one under `dbo:abstract`. If you want to concatenate both scripts into a single label property, turn variable `concatenate_label_abstract` to true:

```
concatenate_label_abstract = True
```
