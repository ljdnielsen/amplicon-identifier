import time
import requests
import argparse

def run_blast_api(fasta_file, output_folder):
    url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

    # Submit the BLAST job
    with open(fasta_file, "r") as file:
        fasta_data = file.read()

    params = {
        "CMD": "Put",
        "PROGRAM": "blastn",
        "DATABASE": "nt",
        "QUERY": fasta_data,
        "FORMAT_TYPE": "Text"
    }

    response = requests.post(url, data=params)
    if "RID =" not in response.text:
        print("Error submitting BLAST job.")
        return None

    rid = response.text.split("RID = ")[1].split("\n")[0].strip()
    print(f"BLAST Job Submitted. RID: {rid}")

    # Wait for BLAST results
    while True:
        status = requests.get(f"{url}?CMD=Get&RID={rid}").text
        if "Status=WAITING" not in status:
            break
        print("Waiting for BLAST results...")
        time.sleep(10)  # Check every 10 sec

    # Retrieve results
    results = requests.get(f"{url}?CMD=Get&RID={rid}&FORMAT_TYPE=Text").text
    with open("{}/results.blast".format(output_folder), "w") as out_file:
        out_file.write(results)

    print("BLAST results saved to results.blast.")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="BLAST amplicons against NCBI nucleotide database bypassing blastn queue.")
parser.add_argument("filename", help="Path to the fasta file containing sequences")
parser.add_argument("output_folder", help="Path to desired output folder")
args = parser.parse_args()

run_blast_api(args.filename, args.output_folder)
