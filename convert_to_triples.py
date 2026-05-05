import csv
import ast
import os

def clean_list_string(value):
    """
    Attempts to clean a string that looks like a list but might be missing commas.
    Example: "['hotel' 'Viennese coffee house']" -> "['hotel', 'Viennese coffee house']"
    """
    if not isinstance(value, str) or not (value.startswith('[') and value.endswith(']')):
        return value
    
    # Simple heuristic to add commas between quoted strings if missing
    # Replace "' '" with "', '"
    cleaned = value.replace("' '", "', '")
    # Also handle possible double quotes if they appear
    cleaned = cleaned.replace('" "', '", "')
    
    try:
        return ast.literal_eval(cleaned)
    except:
        return value

def convert_to_triples(csv_path, output_path):
    triples = []
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = row.get('wikidata_uri')
            if not subject:
                continue
            
            mappings = {
                'company name': 'has_name',
                'description': 'has_description',
                'country': 'located_in',
                'instance of': 'instance_of',
                'inception': 'founded_on',
                'official website': 'has_website',
                'industry': 'belongs_to_industry',
                'founded by': 'founded_by'
            }
            
            for col, predicate in mappings.items():
                value = row.get(col)
                if value and value.strip():
                    if col in ['instance of', 'industry']:
                        parsed_value = clean_list_string(value)
                        if isinstance(parsed_value, list):
                            for item in parsed_value:
                                triples.append([subject, predicate, item])
                        else:
                            triples.append([subject, predicate, value])
                    else:
                        triples.append([subject, predicate, value])
    
    with open(output_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['subject', 'predicate', 'object'])
        writer.writerows(triples)
        
    return triples

if __name__ == "__main__":
    csv_file = '/home/nxhai/AI_thucchien/Lab19_GraphRAG/wikidata_global_companies_info.csv'
    output_file = '/home/nxhai/AI_thucchien/Lab19_GraphRAG/wikidata_triples.csv'
    
    if os.path.exists(csv_file):
        print(f"Reading {csv_file}...")
        all_triples = convert_to_triples(csv_file, output_file)
        print(f"Conversion complete. Total triples: {len(all_triples)}")
        print("\nSample Triples (first 10):")
        for t in all_triples[:10]:
            print(f"({t[0]}, {t[1]}, {t[2]})")
    else:
        print(f"File not found: {csv_file}")
