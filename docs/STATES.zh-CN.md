# 九种状态与触发方式

[English](STATES.md) | [返回首页](../README.zh-CN.md)

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

第 9、10 行保存十六个顺时针注视姿态：0° 朝上，每次增加 22.5°。它们是姿态，不是新增动画状态。`running` 表示处理任务，真正左右奔跑使用 `running-left` 和 `running-right`。

## 怎么触发？

[Pets 官方说明](https://learn.chatgpt.com/docs/pets)列出以下客户端活动状态：

| 客户端状态 | 含义 |
|---|---|
| Running | 某个聊天正在工作。 |
| Needs input | 聊天需要批准、回答或决定。 |
| Ready | 聊天已完成，存在未读活动。 |
| Blocked | 聊天失败或发生系统错误。 |

多个聊天同时存在时，官方说明的优先级是 Needs input → Blocked → Ready → Running。资料核对日期为 2026-10-18，客户端行为可能更新。

`waiting`、`failed`、`running` 的素材含义与上述状态及 Pets 素材工作流相符。**公开文档没有公布九行图集与客户端事件的完整映射。**尤其“检查成果”是我们给第 8 行的中文描述，不能据此保证每次 Ready 都播放它。发送“失落一下”“检查成果”等话语也不是已确认的指令。本项目没有实现自定义触发接口；首页 GIF 可以独立预览每种动作，无需等待客户端触发。
