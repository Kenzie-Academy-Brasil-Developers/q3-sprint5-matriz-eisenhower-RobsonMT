def serialize_categories(categories) -> list:
    output = []

    for category in categories:
        categories_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": []
        }

        for task in category.tasks:
            task_data  = {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "classification": task.type
            }
            
            categories_data["tasks"].append(task_data)
        
        output.append(categories_data)
    
    return output
