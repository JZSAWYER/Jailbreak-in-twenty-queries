import os
import yaml
import re
import json

def update_counts(attack_model, target_model, judge_model, success_increment, total_increment):
    """
    Update the success and total counts for a given combination of models.

    Parameters:
    - attack_model (str): The attacking model.
    - target_model (str): The target model.
    - judge_model (str): The judge model.
    - success_increment (int): The number to add to the success count.
    - total_increment (int): The number to add to the total count.
    """
    model_stats[attack_model][target_model][judge_model]['success'] += success_increment
    model_stats[attack_model][target_model][judge_model]['total'] += total_increment

def get_counts(attack_model, target_model, judge_model):
    """
    Retrieve the success and total counts for a given combination of models.

    Parameters:
    - attack_model (str): The attacking model.
    - target_model (str): The target model.
    - judge_model (str): The judge model.

    Returns:
    Tuple of (success, total)
    """
    stats = model_stats[attack_model][target_model][judge_model]
    return stats['success'], stats['total']

def process_yaml_and_log(task_path):
    """
    Reads config.yaml and output.log from the given task_path,
    then performs placeholder operations on the content.

    Parameters:
    - task_path (str): The path to the task directory.
    """
    # Construct the paths to config.yaml and output.log
    config_path = os.path.join(task_path, "files", "config.yaml")
    sum_path = os.path.join(task_path, "files", "wandb-summary.json")

    _sus = 0
    # trg 
    # Read and process config.yaml
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
                # print(f"Config for {task_path}: {config}")
                # Placeholder for operations with config
            except yaml.YAMLError as exc:
                print(f"Error reading config.yaml in {task_path}: {exc}")

    # Read and process output.log
    if os.path.exists(sum_path):
        with open(sum_path, "r") as sum_file:
            data = json.load(sum_file)
    
            # Access and print the "is_jailbroken" parameter
            is_jailbroken = data.get("is_jailbroken", None)
            if is_jailbroken:
                _sus = 1
    
    update_counts(config['attack_model']['value'], config['target_model']['value'], config['judge_model']['value'], _sus, 1)


def process_directory(dir_path):
    """
    Function to process each directory.
    Placeholder for your specific operations.

    Parameters:
    - dir_path (str): The path to the directory to process.
    """
    # Placeholder for your operations
    # print(f"Processing directory: {dir_path}")
    # Example: print the names of all files in this directory
    for entry in os.listdir(dir_path):
        # Construct the full path to the entry
        full_entry_path = os.path.join(dir_path, entry)
        
        # Check if this entry is a directory
        if os.path.isdir(full_entry_path):
            # Process this directory if it's a first-level subfolder
            process_yaml_and_log(full_entry_path)
    # for file in os.listdir(dir_path):
        # print(f"Found file: {file} in directory: {dir_path}")

def walk_through_wandb_folders(base_dir):
    """
    Recursively walks through all folders within the base_dir,
    calling process_directory for each sub-directory found.

    Parameters:
    - base_dir (str): The base directory to start the walk from.
    """
    for root, dirs, files in os.walk(base_dir):
        # Process the current root directory
        process_directory(root)
        # If you want to process only the sub-directories but not the base directory,
        # you can move the process_directory call inside the for loop below

        # Optionally process each sub-directory (if any specific action needed)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Call the process function for each sub-directory
            # process_directory(dir_path)

def display_model_stats(model_stats):
    for attack_model, target_models in model_stats.items():
        print(f"Attack Model: {attack_model}")
        for target_model, judge_models in target_models.items():
            print(f"  Target Model: {target_model}")
            for judge_model, stats in judge_models.items():
                success, total = stats['success'], stats['total']
                if total:
                    print(f"    Judge Model: {judge_model}, Success: {success}, Total: {total}")
        print()  # Add a blank line for better separation between attack models

if __name__ == "__main__":
    # Define the model choices for each category
    attack_model_choices = ["vicuna", "llama-2", "gpt-35-turbo", "gpt-4", "claude-instant-1","claude-2", "palm-2"]
    target_model_choices = ["vicuna", "llama-2", "gpt-35-turbo", "gpt-4", "claude-instant-1","claude-2", "palm-2"]
    judge_model_choices = ["gpt-35-turbo", "gpt-4","no-judge"]

    # Initialize the nested dictionary
    model_stats = {}
    for attack in attack_model_choices:
        model_stats[attack] = {}
        for target in target_model_choices:
            model_stats[attack][target] = {}
            for judge in judge_model_choices:
                # Initialize success and total counts to 0
                model_stats[attack][target][judge] = {'success': 0, 'total': 0, 'num_que': 0}

    base_dir = "/home/v-hazhong/Projects/Jailbreak-in-twenty-queries/wandb"  # Change this to your wandb folder path
    process_directory(base_dir)
    display_model_stats(model_stats)