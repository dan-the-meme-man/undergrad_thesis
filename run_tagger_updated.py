import subprocess
import os

input_file = os.path.join(os.getcwd(), 'tagger_data', 'tagger_raw_data.txt')

output_dir = os.path.join(os.getcwd(), 'tagger_data')

ark_path = os.path.join(os.getcwd(), 'ark-tweet-nlp-0.3.2', 'ark-tweet-nlp-0.3.2.jar')

if not os.path.exists(ark_path):
    print(f'The tagger was not found or was not located at the expected path, which is {ark_path}.')
    exit()

print(f'Processing {input_file}')
    
p = subprocess.check_output(f'java -XX:ParallelGCThreads=2 -Xmx500m -jar {ark_path} {input_file}')
    
loc = os.path.join(output_dir, 'tagger_output.tsv')
    
with open(loc, 'wb') as f:
    f.write(p)
    print(f'Wrote to {loc}')