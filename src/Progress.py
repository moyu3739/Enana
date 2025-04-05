import json
import threading


class Progress:
    """a class to manage progress"""

    def __init__(self, tasks: list[str] = []):
        self.tasks = {task: "waiting" for task in tasks}
        self.lock = threading.Lock()

    def LoadTasks(self, tasks: list[str]):
        """
        Load tasks from a list
        """
        with self.lock:
            self.tasks = {task: "waiting" for task in tasks}

    def GetTaskNum(self) -> int:
        """
        Get the number of tasks
        """
        with self.lock:
            return len(self.tasks)
        
    def GetTaskNumOfStatus(self, status: str) -> int:
        """
        Get the number of tasks with the given status
        """
        with self.lock:
            return sum(1 for task in self.tasks.values() if task == status)

    def RefreshUndoneTask(self):
        """
        Set all undone tasks to waiting
        """
        with self.lock:
            for task, status in self.tasks.items():
                if status != "done": self.tasks[task] = "waiting"

    def Update(self, task: str, status: str):
        """
        Update the status of a task
        """
        with self.lock:
            self.tasks[task] = status

    def GetOneTaskOfStatusAndUpdate(self, status_get: str, status_update: str) -> str | None:
        """
        Get one task with the given `status_get` and then update its status to `status_update`.
        If no task with the given status, return None
        """
        with self.lock:
            for task, status in self.tasks.items():
                if status == status_get:
                    self.tasks[task] = status_update
                    return task
        return None
    
    def Load(self, file_path: str):
        """
        Load progress from a file
        """
        with self.lock:
            with open(file_path, "r") as f:
                self.tasks = json.load(f)

    def Dump(self, file_path: str):
        """
        Dump progress to a file
        """
        with self.lock:
            with open(file_path, "w") as f:
                json.dump(self.tasks, f, indent=4)
        