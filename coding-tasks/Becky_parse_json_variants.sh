## Codeschool task for 15/04/24
## Using the  cimulated WGS RD JSONS
## Looking in the interpreted_genome cip_version 1 variants:
## How many variants are there?
## Of those, how many TIER1 variants?
## How many structuralVariants are there?
## Of those, how many TIERA variants
## Docs: https://ip-cipapi-help.genomicsengland.co.uk/2.25/data_description/

for jsonfile in *.json;
    do echo "File: $jsonfile";

    VARIANTS=$(jq '.interpreted_genome[] | select(.cip_version==1).interpreted_genome_data.variants | length' $jsonfile);
    TIER1=$(jq '[ .interpreted_genome[] | select(.cip_version==1).interpreted_genome_data.variants[].reportEvents[] | select(.tier=="TIER1")] | length' $jsonfile);
    STRUCTURAL=$(jq '.interpreted_genome[] | select(.cip_version==1).interpreted_genome_data.structuralVariants | length' $jsonfile);
    STRUCTURAL_TIERA=$(jq '[.interpreted_genome[] | select(.cip_version==1).interpreted_genome_data.structuralVariants[].reportEvents[] | select(.tier=="TIERA")] | length' $jsonfile);

    echo "Number of variants is $VARIANTS";
    echo "Number of TIER1 variants is $TIER1";
    echo "Number of structural variants is $STRUCTURAL";
    echo "Number of TIERA structural variants is $STRUCTURAL_TIERA";
done
