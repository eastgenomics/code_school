# Codeschool task for 15/04/24:
--------------------------------------------------------------
## Task 1:
- Get an atlassian API token
- Get number of documents in a particular confluence space with a particular label
- Docs: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about

e.g. labels = controlled and space = DV
❯ curl --request GET --url 'https://cuhbioinformatics.atlassian.net/wiki/api/v2/labels/2656043029/pages?space-id=2903080965' --user 'email:token' --header 'Accept: application/json'

## Task 2
Using the  cimulated WGS RD JSONS
Looking in the interpreted_genome cip_version 1 variants:
- How many variants are there?
- Of those, how many TIER1 variants?
- How many structuralVariants are there?
- Of those, how many TIERA variants

Docs: https://ip-cipapi-help.genomicsengland.co.uk/2.25/data_description/
