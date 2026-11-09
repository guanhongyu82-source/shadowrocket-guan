# shadowrocket-guan

个人小飞机配置。不含节点、不含订阅链接。

- 当前配置：`guan.conf`（版本注释见文件头，当前 **20261109**）
- 版本存档：
  - `archive/guan-20260929.conf`（本次维护前原稿，逐字节保留）
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

## 策略摘要（20261109）

手机很少连 Wi-Fi，按中国移动 5G。稳定优先。坏了才换，不比谁更快。

- **ChatGPT、xai、官**：香港 → 日本 → 新加坡 → 美国。
- **xai**：Cursor、Grok、X、Grok bot 同一组。
- 沿用检测页 `http://www.gstatic.com/generate_204`、`interval=600`、`timeout=5`。这是基础健康探测，不保证业务故障后 5 秒恢复，也不能证明 ChatGPT 所有功能可用。
- 使用有序 `fallback`；实际接替与回切取决于手机客户端版本和当时的健康结果。
- **狗狗**：不在自动链。不要点「测试」。不要改回自动测速。
- 首页选「官」，工作模式选「配置」。

## 手机更新

推送后：小飞机 → 配置「官」→ **更新**。

看一眼策略组：只有 ChatGPT、xai、官三行，右边是「奶昔-香港」。不再有单独的 Grok、Cursor 组。不用改节点订阅。

## 本次维护范围

- 补齐 `oaistatsig.com`、`challenges.cloudflare.com` 和官方网络建议列出的六个精确 WorkOS 资源域名，让它们优先进入 ChatGPT 组。
- 原有整个 `workos.com` 仍归 xai；仅新增的精确资源域名作为 ChatGPT 优先例外。共享域名无法按网页来源区分，因此其他应用访问这些相同资源时也会使用该例外。
- 三个顶层组仍是香港 → 日本 → 新加坡 → 美国；狗狗仍只在手机中手动选择，不并入自动链。
- 未改变 `[General]`、所有策略组定义、其他既有规则及 URL Rewrite；未调整 DNS、IPv6、节点过滤、检测地址或检测频率。不复制 Mac 的维护程序，也不为固定 IP 收紧手机线路。
- `policy-regex-filter` 按节点名称筛选，不能单凭组名证明节点属于哪个订阅；手机节点重命名后需核对候选非空。本次保留现有筛选以避免影响已能使用的订阅。

依据：[OpenAI 网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)。该页面用于核对域名；不把它的企业网络配置建议直接套到手机。

## 验证与回退

执行 `python3 tests/check_config.py` 可检查组引用、地区顺序、规则优先级、既有规则保留以及非目标分流未变化。该脚本是静态检查，不是 Shadowrocket 原生解析器或手机实测。

GitHub 更新不等于手机已加载：手机配置更新后，才会使用本版。当前无法远程确认手机安装的客户端版本、启用的配置、蜂窝/Wi-Fi 连接、登录、流式回答、上传及语音表现，不将仓库检查通过表述为手机验收通过。

若本版出现异常，可恢复 `archive/guan-20260929.conf` 或回退到维护前提交；无需重置节点订阅、账号或证书。
