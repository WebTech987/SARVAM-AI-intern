import argparse
import os
import json
from datasets import load_dataset 
import pandas as pd
from tqdm import tqdm


def consolidate_instruct(dataset_str, output_path, sft_dataset):
    
    id_str = dataset_str + '-'
    print(f"Consolidating {dataset_str}")
#    sft_dataset = sft_dataset['train']
    sarvam_format = []
    
    for index, data_point in tqdm(enumerate(sft_dataset)):
        sarvam_format.append({
            'id': id_str + str(index),
            'turns': [
                {
                    'role': 'system',
                    'content': ''
                },
                {
                    'role': 'user',
                    'content': data_point['instruction'] + data_point['input'] if data_point['input'] is not None else ''
                },
                {
                    'role': 'assistant',
                    'content': data_point['response'],
                    'thoughts': ['[OUTPUT_LANGUAGE]\nEnglish']
                }
            ]
        })
    
    return sarvam_format

def main(args):
    dataset_func = {
        'gpt4-instruct-dedupe-only-dataset': consolidate_instruct
        # Add more dataset functions if needed
    }

    # Check if the dataset file exists
    if args.dataset == 'gpt4-instruct-dedupe-only-dataset':
        dataset_file = os.path.join(os.path.dirname(__file__), 'gpt4-instruct-dedupe-only-dataset.json')
    if not os.path.isfile(dataset_file):
        raise FileNotFoundError(f"Dataset file '{dataset_file}' not found.")

    # Load the dataset
    sft_dataset = load_dataset('json', data_files=dataset_file)['train']

    # Call the appropriate function from the dictionary
    if args.dataset not in dataset_func:
        raise KeyError(f'Dataset {args.dataset} not found in the dictionary')
    else:
        sarvam_format = dataset_func[args.dataset](args.dataset, args.output_path, sft_dataset)

    # Convert to DataFrame and save to JSON
    sarvam_format = pd.DataFrame(sarvam_format)
    sarvam_format.to_json(os.path.join(args.output_path, args.dataset+'-consolidated.jsonl'), orient='records', lines=True, force_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dataset Consolidation")
    parser.add_argument('--dataset', type=str, default='gpt4-instruct-dedupe-only-dataset', help='Dataset name')
    parser.add_argument('--output_path', type=str, required=True, help='Output path')

    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

    main(args)

