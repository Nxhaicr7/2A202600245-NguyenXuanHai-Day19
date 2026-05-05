import csv

def convert_csv_to_text(csv_path, txt_path):
    with open(csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        with open(txt_path, mode='w', encoding='utf-8') as outfile:
            for row in reader:
                # Basic template: Subject predicate object.
                sentence = f"{row['subject']} {row['predicate']} {row['object']}.\n"
                outfile.write(sentence)

if __name__ == "__main__":
    convert_csv_to_text('input/wikidata_sample.csv', 'input/corpus.txt')
