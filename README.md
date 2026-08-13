# GenLayer AI-Verified Task Completion System

Complete GenLayer app where GenLayer is central to the main workflow.

## Use Case
Users create tasks with natural-language criteria.  
Workers submit a proof URL.  
The Intelligent Contract fetches the live webpage and uses decentralized AI consensus to decide if the task is completed.

## Requirements satisfied
- Clear real-world use case
- One real Intelligent Contract (Python)
- App logic that interacts with GenLayer (via Studio)

## How to test (100% free)
1. Go to https://studio.genlayer.com
2. Create new contract and paste the code from `contracts/task_verifier.py`
3. Deploy the contract
4. Call the methods in order:
   - create_task
   - submit_proof
   - verify_task
   - get_task

## Contract file
`contracts/task_verifier.py`

## Deployed Contract

- **Studio / Testnet Address**: `0x4A59BB444Bc02E8e1587fE36b42AC6cA7A1d3898`
