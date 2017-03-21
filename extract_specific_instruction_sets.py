# This script extracts specific sets of instructions generated by the prohow-crawler
# The urls to extract are found in the extract_specific_sets_instructions.txt file
# The extract_specific_sets_instructions.txt file should contain one URL per line
# only the sets of instructions corresponding to these URLs will be extracted
# the URLs will be matched in a non-case sensitive way

## IN-CODE PARAMETERS



# This parameter can be changed to only select instructions with specific language tags.
# More specifically, the algorighm will only consider files having a name which starts with at least one 
# list_of_allowed_languages = []
# for example, for English and Spanish: 
list_of_allowed_languages = ["en","es"]

# This parameter can be changed to only select instructions witin specific categories.
# More specifically, the algorighm will select all the instructions which directly belong to one of the types
# in list_of_allowed_categories, or one their sub-classes as defined in RDFS, in the Turtle file class_hierarchy.ttl
list_of_allowed_categories = ["http://es.wikihow.com/Categor%C3%ADa:Desayunos","http://www.wikihow.com/Category:Breakfast" 
                              ,"http://www.wikihow.com/Category:Recipes","http://es.wikihow.com/Categor%C3%ADa:Recetas" 
                              ,"http://es.wikihow.com/Categor%C3%ADa:Recetas-para-dietas-especiales","http://www.wikihow.com/Category:Specialty-Diet-Recipes"
                              ,"http://www.wikihow.com/Category:Food-Preparation","http://www.wikihow.com/Category:Food-Preparation"    
                                                                                                                                        
                               ]
# for example, the following configuration extracts only breakfast food instructions in Spanish and English
# list_of_allowed_categories = ["http://www.wikihow.com/Category:Breakfast","http://es.wikihow.com/Categor%C3%ADa:Desayunos"]

# ADVANCED PARAMETERS

# This parameter allows advanced filtering of the sets of instructions to output
# If this parameter is set to false, all the following parameters are considered set to false too
perform_sparql_filtering = True
# If this parameter is set to true, sets of instructions containing multiple methods will be ignored
remove_multiple_methods = True
# If this parameter is set to true, sets of instructions containing multiple sets of requirements will be ignored
remove_multiple_requirements = True

# These parameters allow you to select instructions with a number of steps and requirements within a certain range
# If this parameter larger than -1, sets of instructions with less than this number of steps will be ignored
min_number_of_steps = 5
# If this parameter larger than -1, sets of instructions with more than this number of steps will be ignored
max_number_of_steps = 20
# If this parameter larger than -1, sets of instructions with less than this number of requirements will be ignored
min_number_of_requirements = 5
# If this parameter larger than -1, sets of instructions with more than this number of requirements will be ignored
max_number_of_requirements = 20

# If this list contains at least one element, at least one pair of strings inside must occur in the subject and object
# of an owl:sameAs relation. For example, by setting:
# owl_sameAs_required_prefixes = [["http://es.wikihow.com/","http://www.wikihow.com/"]]
# we select only instructions in English which have an equivalent Spanish page or vice-versa
owl_sameAs_required_prefixes = [["http://es.wikihow.com/","http://www.wikihow.com/"]]

save_simplified = True
# CODE START

import os, ntpath, string, rdflib

hierarchy = {}
# load hieararchy if present
if os.path.isfile("class_hierarchy.ttl"):
    print "Loading a class hierarchy"
    num = 0
    h = open("class_hierarchy.ttl",'r')
    for line in h:
        urls = line.split("> rdfs:subClassOf <")
        #print urls
        url1 = urls[0][1:]
        url2 = urls[1][:-4]
        #print url1
        #print url2
        hierarchy[url1] = url2
        num += 1
    h.close()
    print str(num)+" sub-class relations extracted."

def is_subclass_of(concept,super):
    return is_subclass_of_with_recursion_limit(concept,super,0)

def is_subclass_of_with_recursion_limit(concept,super,level):
    if level > 30:
        return False
    if concept == super:
        return True
    if concept in hierarchy:
        return is_subclass_of_with_recursion_limit(hierarchy[concept],super,level+1)
    return False

list_of_urls = []
if os.path.isfile("extract_specific_sets_instructions.txt"):
    print "Loading the extract_specific_sets_instructions file"
    conf = open("extract_specific_sets_instructions.txt",'r')
    for line in conf:
        extracted = line.lower().strip()
        if len(extracted) > 0:
            list_of_urls.append(extracted);
    conf.close()

print "Specific URL extraction configured with: "+str(len(list_of_urls))+" URLs"
	


out = open('extracted_graph.ttl','w')

out_simple = None
if save_simplified:
    out_simple = open('extracted_simplified_graph.ttl','w')

prefixes = "@prefix w: <http://w3id.org/prohowlinks#> .\n@prefix oa: <http://www.w3.org/ns/oa#> .\n@prefix prohow: <http://w3id.org/prohow#> .\n\
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\
@prefix owl: <http://www.w3.org/2002/07/owl#> .\n@prefix dbo: <http://dbpedia.org/ontology/> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"

sparql_prefixes = "PREFIX prohow: <http://w3id.org/prohow#> \n PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \n\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \n PREFIX oa: <http://www.w3.org/ns/oa#> \n\
PREFIX owl: <http://www.w3.org/2002/07/owl#> "

out.write(prefixes)


def save(line):
    if perform_sparql_filtering:
        g = rdflib.Graph()
        result = g.parse(data = prefixes+"\n"+line, format="turtle")
        if remove_multiple_methods:
            qres = g.query(
                sparql_prefixes+"""SELECT DISTINCT ?m
                   WHERE {
                      ?main rdf:type prohow:instruction_set .
                      ?main prohow:has_method ?m .
                   }""")
            if len(qres) > 1:
                #print("Too many methods: "+str(len(qres)))
                return False
        if min_number_of_steps > -1 or max_number_of_steps > -1:
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?p
                               WHERE {
                                  {?main rdf:type prohow:instruction_set .
                                  ?main prohow:has_method ?m .
                                  ?m prohow:has_step ?p .}
                                  UNION
                                  {?main rdf:type prohow:instruction_set .
                                  ?main prohow:has_method ?m .
                                  ?m prohow:has_step ?part .
                                  ?part prohow:has_method ?pm .
                                  ?pm prohow:has_step ?p .}
                               }""")
            if min_number_of_steps > -1 and len(qres) < min_number_of_steps:
                #print("Too few steps: "+str(len(qres))+" "+line[0:300])
                return False
            if max_number_of_steps > -1 and len(qres) > max_number_of_steps:
                #print("Too many steps: "+str(len(qres))+" "+line[0:300])
                return False
        if remove_multiple_requirements:
            qres = g.query(
                sparql_prefixes+"""SELECT DISTINCT ?r
                   WHERE {
                      ?main rdf:type prohow:instruction_set .
                      ?main prohow:requires ?r .
                      ?r prohow:has_step ?s .
                      ?s rdf:type prohow:consumable .
                   }""")
            if len(qres) > 2:
                #print("Too many requirements: "+str(len(qres))+" "+line[0:300])
                return False
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?r
                              WHERE {
                                 ?main rdf:type prohow:instruction_set .
                                 ?main prohow:requires ?r .
                                 ?r prohow:has_step ?s .
                                 ?s rdf:type prohow:requirement .
                              }""")
            if len(qres) > 2:
                #print("Too many requirements: " + str(len(qres)) + " " + line[0:300])
                return False
        if min_number_of_requirements > -1 or max_number_of_requirements > -1:
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?s
                   WHERE {
                      ?main rdf:type prohow:instruction_set .
                      ?main prohow:requires ?r .
                      ?r prohow:has_step ?s .
                   }""")
            if min_number_of_requirements > -1 and len(qres) < min_number_of_requirements:
                #print("Too few requirements: "+str(len(qres))+" "+line[0:300])
                return False
            if max_number_of_requirements > -1 and len(qres) > max_number_of_requirements:
                #print("Too many requirements: "+str(len(qres))+" "+line[0:300])
                return False
        if len(owl_sameAs_required_prefixes) > 0:
            found = False
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?s ?o
                       WHERE {
                          ?s owl:sameAs ?o .
                       }""")
            if len(qres) < 1:
                return False
            for row in qres:
                if not found:
                    for pair in owl_sameAs_required_prefixes:
                        if (pair[0] in row["s"] and pair[1] in row["o"]) or (pair[1] in row["s"] and pair[0] in row["o"]):
                            found = True
            if not found:
                #print("Not enough languages: " + str(len(qres)) + " " + line[0:300])
                return False
        if save_simplified:
            # get title
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?main ?l
                               WHERE {
                                  ?main rdf:type prohow:instruction_set .
                                  ?main rdfs:label ?l .
                               }""")
            title = qres.bindings[0]["l"]
            title_uri = qres.bindings[0]["main"]
            #print title
            #print title_uri
            # get requirements
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?s ?l
                               WHERE {
                                  ?main rdf:type prohow:instruction_set .
                                  ?main prohow:requires ?r .
                                  ?r prohow:has_step ?s .
                                  ?s rdfs:label ?l .
                               }""")
            for row in qres:
                label = row["l"]
                uri = row["s"]
                #print uri
                #print label
            # get ordered steps
            qres = g.query(
                sparql_prefixes + """SELECT DISTINCT ?m2
                               WHERE {
                                  ?main rdf:type prohow:instruction_set .
                                  ?main prohow:has_method ?m .
                                  ?m prohow:has_step ?s .
                                  ?s prohow:has_method ?m2 .
                               }""")
            if len(qres) > 1:
                print "there are multiple parts"
            else:
                print "no parts"
        print(" X graph has %s statements." % len(g))
    out.write(line+"\n\n")

    return True

def parse_file(file):
    print "Parsing file "+str(file)
    f = open(file,'r')
    full_instruction = ""	
    found = False
    found_num = 0
    for line in f:
        if 'oa:hasTarget <' in line:
            for url in list_of_urls:
                if "<"+str(url.lower())+">" in line.lower():
                    found = True
        if "rdf:type <" in line:
            line_parts = line.split("rdf:type <")
            type = line_parts[1][:-4]
            for allowed_concept in list_of_allowed_categories:
                if is_subclass_of(type,allowed_concept):
                    found = True
        #if 'http://www.wikihow.com/Category:Cocktails' in line or ('http://es.wikihow.com/Categor%C3%ADa:Bebidas-alcoh%C3%B3licas' in line)\
        #        or ('http://es.wikihow.com/Categor%C3%ADa:Pizza' in line) or ('http://www.wikihow.com/Category:Pizza' in line):
        #    found = True
        if 'rdf:type prohow:instruction_set .' in line:
            # if the previous instruction set was selected, save it in output
            if found:
                if save(full_instruction):
                  found_num += 1
            # start collecting a new instructions set
            found = False
            full_instruction = line
        else:
            if len(full_instruction) > 0:
                if "<" in line and ">" in line and ":" in line and "http:" in line:
                    line = string.replace(line, "(", "")#tring.replace(s, old, new[, maxreplace])
                    line = string.replace(line, ")", "")
                full_instruction = full_instruction+line
    if found:
        if save(full_instruction):
          found_num += 1
    f.close()
    print "Found in file: "+str(found_num)
    return found_num


rootdir = os.getcwd()
total_found = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        if filepath.endswith(".ttl"):
            if len(list_of_allowed_languages) > 0:
                for lang in list_of_allowed_languages:
                    if ntpath.basename(filepath).startswith(lang):
                        print filepath
                        total_found += parse_file(filepath)
            else:
                total_found += parse_file(filepath)
out.close()
if save_simplified:
    out_simple.close()
print 'In total, '+str(total_found)+' were found'
