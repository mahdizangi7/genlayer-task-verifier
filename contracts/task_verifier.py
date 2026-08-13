# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

class TaskVerifier(gl.Contract):
    task_counter: u256
    tasks: TreeMap[str, str]

    def __init__(self):
        self.task_counter = u256(0)
        self.tasks = TreeMap[str, str]()

    @gl.public.write
    def create_task(self, title: str, description: str, verification_criteria: str) -> str:
        task_id = str(int(self.task_counter))
        self.task_counter = self.task_counter + u256(1)

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "criteria": verification_criteria,
            "creator": str(gl.message.sender_address),
            "status": "open",
            "proof_url": "",
            "worker": "",
            "verdict": ""
        }
        self.tasks[task_id] = json.dumps(task)
        return task_id

    @gl.public.write
    def submit_proof(self, task_id: str, proof_url: str) -> str:
        if task_id not in self.tasks:
            raise Exception("Task not found")
        task = json.loads(self.tasks[task_id])
        if task["status"] != "open":
            raise Exception("Task is not open")
        task["status"] = "submitted"
        task["proof_url"] = proof_url
        task["worker"] = str(gl.message.sender_address)
        self.tasks[task_id] = json.dumps(task)
        return "Proof submitted"

    @gl.public.write
    def verify_task(self, task_id: str) -> str:
        if task_id not in self.tasks:
            raise Exception("Task not found")
        task = json.loads(self.tasks[task_id])
        if task["status"] != "submitted":
            raise Exception("Task is not in submitted state")

        proof_url = task["proof_url"]
        title = task["title"]
        description = task["description"]
        criteria = task["criteria"]

        def fetch_evidence():
            web_data = gl.nondet.web.render(proof_url, mode="text")
            return web_data[:5000] if web_data else ""

        evidence = gl.eq_principle.strict_eq(fetch_evidence)

        if not evidence or len(evidence) < 30:
            task["status"] = "rejected"
            task["verdict"] = "Could not fetch valid evidence"
            self.tasks[task_id] = json.dumps(task)
            return "REJECTED: Invalid evidence"

        prompt = f"""You are an impartial AI judge verifying task completion.

TASK TITLE: {title}
TASK DESCRIPTION: {description}
VERIFICATION CRITERIA: {criteria}

SUBMITTED EVIDENCE (from {proof_url}):
{evidence}

Decide if the evidence proves the task is completed.
Respond with EXACTLY one of these:
VERIFIED: short reason
OR
REJECTED: short reason"""

        def analyze():
            return gl.nondet.exec_prompt(prompt)

        result = gl.eq_principle.prompt_non_comparative(
            analyze,
            task="Judge whether the submitted evidence satisfies the task criteria",
            criteria="The response must start with VERIFIED: or REJECTED: and give a short clear reason"
        )

        if result.strip().upper().startswith("VERIFIED"):
            task["status"] = "verified"
        else:
            task["status"] = "rejected"
        task["verdict"] = result
        self.tasks[task_id] = json.dumps(task)
        return result

    @gl.public.view
    def get_task(self, task_id: str) -> str:
        if task_id not in self.tasks:
            return "Task not found"
        return self.tasks[task_id]

    @gl.public.view
    def get_all_tasks(self) -> str:
        return json.dumps(list(self.tasks.values()))