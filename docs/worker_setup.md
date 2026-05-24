# Worker Startup Guide

This project uses RQ to process review jobs in a background worker.

## Open a New Terminal in VS Code

1. In VS Code, open the Terminal menu.
2. Select New Terminal.
3. Make sure the terminal starts in the project root folder.

## Activate the Virtual Environment on Mac

Run this command in the new terminal:

```bash
source venv/bin/activate
```

## Start the Worker

Run:

```bash
rq worker
```

## Expected Output

When the worker starts correctly, you should see output like:

```text
Listening for work...
```

## How to Verify the Worker Is Running

1. Start the FastAPI app.
2. Start the worker in a second terminal.
3. Send a pull request event through the webhook.
4. Watch the worker terminal for these debug logs:
   - `Worker started`
   - `Job received`
   - `Processing review`
   - `Redis connected`

If you see those messages, the worker is running and receiving jobs.

## Notes

- `redis` and `rq` are already listed in `requirements.txt`.
- Do not change the webhook or architecture when following this guide.