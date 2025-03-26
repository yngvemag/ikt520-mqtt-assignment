#!/usr/bin/env python3
"""
Run all MQTT tasks sequentially
"""
import os
import time
import importlib
import sys

def run_task(task_number: int, wait_time: int = 2) -> None:
    """
    Run a specific task and wait between tasks.
    
    Args:
        task_number: The task number to run
        wait_time: Time to wait after task completion in seconds
    """
    task_name = f"task{task_number}"
    
    if task_number == 1:
        task_name = "task1_create_clients"
    elif task_number == 2:
        task_name = "task2_connect_publisher"
    elif task_number == 3:
        task_name = "task3_connect_subscriber"
    elif task_number == 4:
        task_name = "task4_publish_message"
    elif task_number == 5:
        task_name = "task5_wildcard_subscriptions"
    elif task_number == 6:
        task_name = "task6_persistent_session_qos1"
    elif task_number == 7:
        task_name = "task7_non_persistent_session"
    elif task_number == 8:
        task_name = "task8_persistent_mixed_qos"
    
    print(f"\n{'='*80}")
    print(f"Running Task {task_number}")
    print(f"{'='*80}\n")
    
    try:
        # Import and run the task module
        task_module = importlib.import_module(task_name)
        task_module.main()
        
        print(f"\nTask {task_number} completed. Waiting {wait_time} seconds before next task...\n")
        time.sleep(wait_time)
    except Exception as e:
        print(f"Error running task {task_number}: {e}")

def main() -> None:
    """Main function to run all tasks."""
    print("MQTT Assignment - Running All Tasks")
    
    # Check if a specific task was requested
    if len(sys.argv) > 1:
        try:
            task_number = int(sys.argv[1])
            if 1 <= task_number <= 8:
                run_task(task_number)
            else:
                print(f"Invalid task number: {task_number}. Must be between 1 and 8.")
        except ValueError:
            print(f"Invalid task number: {sys.argv[1]}. Must be an integer.")
        return
    
    # Run all tasks
    for task_number in range(1, 9):
        run_task(task_number)
    
    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    main() 