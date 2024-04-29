import argparse
import csv
import json

# URL de votre fichier CSV (à remplacer par le chemin local si nécessaire)
import requests

csv_url = 'csv_mappings/bdpm_to_cip_label.csv'


# Configuration des arguments pour rendre le script flexible
parser = argparse.ArgumentParser(description='Create FHIR ConceptMap from CSV mappings.')
parser.add_argument('--sourceCanonical', required=True, help='The sourceCanonical URL')
parser.add_argument('--targetCanonical', required=True, help='The targetCanonical URL')
parser.add_argument('--input_csv', required=True, help='Input CSV file path')
parser.add_argument('--output_json', required=True, help='Output JSON file path')

args = parser.parse_args()


# Création du modèle de base du ConceptMap FHIR
concept_map = {
    "resourceType": "ConceptMap",
    "sourceCanonical": args.sourceCanonical,
    "targetCanonical": args.targetCanonical,
    "group": [],
    "useContext": [
        {
            "code": {
                "system": "http://terminology.hl7.org/CodeSystem/usage-context-type",
                "code": "task"
            },
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "https://smt.esante.gouv.fr/terminologie-ncit",
                        "code": "C142485",
                        "display": "alignement des données"
                    }
                ],
                "text": "Aligner les codes CIP BDPM avec les codes CIP du référentiel CIP UCD."
            }
        }
    ]
}

# Initialisation du groupe de mappings
group = {
    "source": args.sourceCanonical,
    "target": args.targetCanonical,
    "element": []
}

# Lecture du fichier CSV et ajout des mappings
with open(args.input_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    #token = getToken()
    for row in reader:
        source_code = row[1]
        target_code = row[4]
        label_source = row[2]
        label_target = row[5]
        # Récupération du libellé pour le code CIP UCD
        #print(f'http://www.data.esante.gouv.fr/ANSM/BDPM-core-ontology/{uri_source}')
        #label_source = getLabel(token,"terminologie-bdpm", f'{uri_source}')
        #label_target = getLabel(token, 'terminologie-cip_ucd',f'{uri_target}')

        element = {
            "code": source_code,
            "display": label_source,
            "target": [
                {
                    "code": target_code,
                    "display": label_target,
                    "equivalence": "equivalent"
                }
            ]
        }
        group['element'].append(element)

# Ajout du groupe au ConceptMap
concept_map['group'].append(group)

# Conversion du ConceptMap en JSON et écriture dans un fichier
with open(args.output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(concept_map, jsonfile, ensure_ascii=False, indent=4)

print("Le fichier concept_map.json a été créé avec succès.")
