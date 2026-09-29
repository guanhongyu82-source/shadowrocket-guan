# shadowrocket-guan

个人小飞机配置。不含节点、不含订阅链接。

- 当前配置：`guan.conf`（版本注释见文件头，当前 **20260929**）
- 版本存档：
  - `archive/guan-20260926.conf`（全部手选，不自动换，已替换）
  - `archive/guan-20260924b.conf`（Grok 与 Cursor 分开，Cursor 在美西，已替换）
  - `archive/guan-20260924.conf`（香港/美国自动测速，节点来回跳，已替换）
  - `archive/guan-20260923.conf`（Grok / X 钉美西，手机上慢，已替换）
  - `archive/guan-20260918b.conf`（港→日→新→美自动切换，已替换）
  - `archive/guan-20260918-usfirst.conf`（ChatGPT 美优先试排，已弃）
  - `archive/guan-20260914.conf`
  - `archive/guan-20260910.conf`
  - `archive/guan-20260901.conf`
- 小飞机用 URL 添加；只读口令写在手机本地，不要提交进仓库。

## 策略摘要（20260929）

手机很少连 Wi-Fi，按中国移动 5G。稳定优先。坏了才换，不比谁更快。

- **ChatGPT、xai、官**：香港 → 日本 → 新加坡 → 美国。
- **xai**：Cursor、Grok、X、Grok bot 同一组。
- 检测页 `http://www.gstatic.com/generate_204`。每 10 分钟一次，5 秒打不开才换。能打开，再慢也不换。
- 同一地区里，当前节点失败才换下一条。
- **狗狗**：不在自动链。不要点「测试」。不要改回自动测速。
- 首页选「官」，工作模式选「配置」。

## 手机更新

推送后：小飞机 → 配置「官」→ **更新**。

看一眼策略组：只有 ChatGPT、xai、官三行，右边是「奶昔-香港」。不再有单独的 Grok、Cursor 组。不用改节点订阅。
