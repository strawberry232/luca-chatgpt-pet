# States and triggers

[中文](STATES.zh-CN.md) | [Home](../README.md)

| Row / 行 | Key | Frames / 帧 | 中文 | English |
|---|---|---|---|---|
| 0 | `idle` | 6 | 待机 | Idle |
| 1 | `running-right` | 8 | 向右跑 | Run right |
| 2 | `running-left` | 8 | 向左跑 | Run left |
| 3 | `waving` | 4 | 挥手 | Wave |
| 4 | `jumping` | 5 | 跳跃 | Jump |
| 5 | `failed` | 8 | 失落 | Disappointed |
| 6 | `waiting` | 6 | 等待回应 | Waiting |
| 7 | `running` | 6 | 认真工作 | Working |
| 8 | `review` | 6 | 检查成果 | Review |

Rows 9–10 contain sixteen clockwise look poses: 0° points up, then increments of 22.5°. These are poses, not additional animation states. `running` means work in progress; directional locomotion uses `running-left` and `running-right`.

## What triggers them?

[Official Pets documentation](https://learn.chatgpt.com/docs/pets) describes these client activity states:

| Client state | Meaning |
|---|---|
| Running | A chat is actively working. |
| Needs input | A chat needs approval, an answer or a decision. |
| Ready | A chat has completed with unread activity. |
| Blocked | A chat failed or encountered a system error. |

For multiple chats, the documented priority is Needs input → Blocked → Ready → Running. Documentation was checked on 2026-10-18; client behavior may change.

The asset labels `waiting`, `failed` and `running` fit those meanings and the Pets asset workflow. **The public documentation does not publish a complete mapping of all nine atlas rows to client events.** In particular, “Review” is our descriptive name for row 8, not proof that every Ready event plays it. Typing “be disappointed” or “check the result” is not a confirmed command. This project implements no custom trigger hooks. The linked GIFs preview every state independently without relying on client triggers.
