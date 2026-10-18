# Quality evidence / 质量检查

These are archived checks from the final v5 production run; machine-local paths have been replaced with relative labels. They are not newly performed by `scripts/verify.py`.

这些 JSON 是最终 v5 制作过程的实际检查记录，本机绝对路径已经替换为相对标签；不是运行 `scripts/verify.py` 时重新执行的全部检查。

- `atlas-validation.json`: correct v2 geometry; no opaque key-color pixels, chroma fringe or hidden transparent RGB. / 图集尺寸、色键绿边及透明像素检查通过。
- `preserved-rows.json`: all nine non-running rows remain exact RGBA matches. / 跑步以外九行逐像素保留。
- `rig-color-connectivity.json`: all sixteen run frames have no extra disconnected component of eight or more pixels; interior brown hair median differs from idle by at most 1/255 per channel. This is not a claim that every material pixel matches the front view. / 十六帧未出现至少八像素的额外断开块，内部棕发中位色差不超过每通道 1/255，不代表正侧面所有材质像素完全相同。
- `side-palette-matching.json`: one-time material calibration of profile anchors. / 侧身原画的一次性材质配色校准。
- `pet-quality.json`: existing look-pose checks include a non-fatal warning around 157.5° → 180°; these poses were preserved. / 原有注视姿态在 157.5° → 180° 附近有非致命警告，相关姿态未改动。
- `standard-frame-review.json`: documents the manual rig approach; generated anatomical component metadata is not available for these manually cut layers. / 记录手工分层绑定方式，不能把它声称为逐帧 AI 组件验收。

`scripts/verify.py` independently checks the shipped assets, hashes, cell occupancy, transparent pixels, unchanged rows and optional rebuilt-image parity. It does not assess whether a viewer finds the motion natural. / 仓库验证脚本独立检查素材、哈希、格子占用、透明像素、保留行及可选的重建一致性；动作是否自然仍需人工观看。
