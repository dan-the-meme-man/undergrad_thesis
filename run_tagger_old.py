import subprocess
import os

try:
    input_dir = os.path.join(os.getcwd(), 'coraal_clean')
except:
    print('Please run preprocess.py first.')
    exit()

output_dir = os.path.join(os.getcwd(), 'coraal_tagged')

ark_path = os.path.join(os.getcwd(), 'ark-tweet-nlp-0.3.2', 'ark-tweet-nlp-0.3.2.jar')

if not os.path.exists(ark_path):
    print(f'The tagger was not found or was not located at the expected path, which is {ark_path}.')
    exit()    

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for file in os.listdir(input_dir):
    print(f'Processing {file}')
    
    input_file = os.path.join(input_dir, file)
    
    print(ark_path)
    print(input_file)
    
    p = subprocess.check_output(f'java -XX:ParallelGCThreads=2 -Xmx500m -jar {ark_path} {input_file}')
    
    loc = os.path.join(output_dir, file[:-4] + '_output.tsv')
    
    with open(loc, 'wb') as f:
        f.write(p)
        print(f'Wrote to {loc}')

    print()