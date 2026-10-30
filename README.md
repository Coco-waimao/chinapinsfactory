# China Pins Factory（CPF）

面向海外批发买家的定制徽章工厂英文站。纯静态站点，无框架、无构建步骤、无依赖。

- 站点结构、关键词地图、SEO 策略与上线检查清单：[`SITE-STRUCTURE.md`](SITE-STRUCTURE.md)
- 生产域名：`https://www.chinapinsfactory.com/`

## 技术栈

原生 HTML + CSS + JavaScript。18 个页面，全部页面共享 `assets/css/styles.css` 与 `assets/js/main.js`。

## 目录结构

站点按买家路径分五个类目目录，根目录只留系统文件与入口页。

```
index.html                  首页（规格速配器 + 询价）
404.html                    404 兜底页（GitHub Pages 只认根目录这一份）
thank-you.html              表单提交后落地页（noindex，站内零入口链接）
robots.txt / sitemap.xml    搜索引擎配置
CNAME                      GitHub Pages 自定义域名（www.chinapinsfactory.com）

products/                   买什么
  index.html                 目录中枢（对外 URL 为 /products/）
  custom-enamel-pins.html     批发定制别针（5 种工艺）
  custom-metal-swag.html      金属周边（挑战币/奖牌/钥匙扣/皮带扣/袖扣）
  custom-metal-badges.html    金属徽章
  samples.html                样品与打样
  request-a-quote.html        询价页（唯一转化落地页）

guides/                     怎么买
  index.html                 目录中枢（对外 URL 为 /guides/，按买家任务分组）
  bulk-order-guide.html       批量下单指南
  design-file-specs.html      设计文件规范（线宽/色块/字号/格式）
  process-comparison.html     五种工艺对比矩阵
  faq.html                    常见问题（27 问）

company/                    是不是靠谱
  index.html                 目录中枢（对外 URL 为 /company/）
  factory.html                工厂与品控
  contact.html                联系方式与联系表单

blog/                       知识
  index.html                  博客索引（对外 URL 为 /blog/）
  how-to-order-custom-lapel-pins-from-china.html
  hard-enamel-vs-soft-enamel-pins.html
  lapel-pin-sizes-guide.html
  custom-challenge-coin-sizes-guide.html

legal/
  privacy-policy.html         隐私政策

assets/
  css/styles.css              全站样式
  js/main.js                  交互脚本（导航、皮肤切换、速配器、表单提交）
  images/                     图片资源（webp + jpg 双格式，含 srcset 尺寸档）

feed.xml                    RSS 2.0（AI 爬虫与聚合器的内容入口）
llms.txt                    AI 爬虫索引（Markdown 格式，列出关键页面与一句话说明）
```

每个页面只服务一个主关键词，文件名即主词 slug，目录即页面角色组。

## 本地预览

直接用浏览器打开 `index.html` 即可，**不需要启动本地服务器**。所有页面间链接、资源引用一律用相对路径。

> 注意：站内链接一律写成显式文件名（例如 `../blog/index.html`），不写目录形式（`../blog/`）。浏览器打开 `file://` 目录时会显示文件列表而不是 `index.html`，写成目录形式会丢掉双击预览的能力。对外 URL 仍由 canonical 指向干净的 `/blog/`。

## 提交前检查

**每次 commit / push 之前必须先跑本地检查。** 不要上线后再补做检查。

```bash
python scripts/check.py          # 完整报告
sh scripts/install-hooks.sh      # 一次性安装 git hook
```

安装后 `pre-commit` 和 `pre-push` 会自动执行检查，**不通过就拦住提交和推送**，报错直接显示在终端。

检查覆盖 11 项：

| # | 检查项 | 拦截什么 |
|---|---|---|
| 1 | JSON-LD 解析 | 结构化数据语法错误 |
| 2 | 内部链接 | 指向不存在文件的相对链接与站内绝对链接（含 canonical） |
| 3 | 图片引用 | 指向不存在文件的图片与 srcset |
| 4 | ItemList | `numberOfItems` 与条目数不符，或条目在页面上不可见 |
| 5 | FAQPage | Question 数与可见问题数不符 |
| 6 | H1 / canonical | 一页多个 H1、canonical 缺失或重复 |
| 7 | 机器层 | sitemap / feed / llms.txt 三者互相不一致，页面漏进 sitemap |
| 8 | 可达性 | 存在从首页无法到达的孤岛页；目录 hub 入链不足 |
| 9 | 面包屑 | 目录页缺少层级，或目录项没链到对应 hub |
| 10 | 导航 | 导航链接集合与全站不一致，重复的询价入口，当前项多于一个 |
| 11 | 行尾 | 单个文件的 CRLF/LF 被意外翻转（会造成巨大无意义 diff） |

第 8 项的原理是：每个页面都必须在链接图上从 `index.html` 可达。`404.html` 与 `thank-you.html` 是仅有的两个例外（前者由服务器兜底，后者由脚本跳转），脚本已按预期处理。

第 9 项对应站点的层级约定：**导航 = 买家意图直达（3 个下拉组 + 1 个平铺项），面包屑 = 目录层级，页脚 = 平铺实用链接。** 子页面包屑形如 `Home / Products / Custom Pins`，其中 `Products` 是可点链接，指向 `products/index.html`；目录页自身显示 `Home / Products`，`Products` 为当前项。目录入口不走页脚——页脚三列装的是具体工艺与杂项链接，塞进目录节点会打乱层级。

第 10 项：导航固定为 `Products | Guides | Our Factory | Journal` 四项顶级，其中前三项各挂一个下拉组（Products 4 个二级、Guides 4 个二级、Our Factory 2 个二级），`Journal` 保持平铺。校验方式不是比对文本，而是把每页 nav 块里的链接归一化成仓库相对路径后比对集合，确保全站一致。每个下拉组的父项本身就是通往目录中枢的真实链接（`products/index.html` / `guides/index.html` / `company/index.html`），脚本不运行时二级页面照样可达。询价入口只有页头 `Get a Quote` 按钮、移动端吸底条与各页语境 CTA，导航里不再重复放。

配套的可达性明细可以用 `python scripts/reachability.py` 查看，它会列出每个页面的入链数、出链数、距首页的层级，以及三个目录中枢页各自被哪些页面链接。

## 导航维护

导航的唯一来源是 `scripts/nav_sync.py`。**不要手改单个页面的 nav 块**，28 页手改必然漂移，提交前检查会拦下来。

```bash
python scripts/nav_sync.py           # 按菜单模型批量重写 28 页导航
python scripts/nav_sync.py --check   # 只报告差异，不落盘
python scripts/nav_responsive.py     # 无头浏览器实测：14 页 × 9 断点 = 126 组合
```

增删二级项只改 `scripts/nav_sync.py` 里的 `NAV_GROUPS` / `NAV_FLAT`，然后跑一次重写。`nav_responsive.py` 会检查横向溢出、导航与页头按钮的可见性、面包屑高度是否恒定、下拉面板是否越界、移动端手风琴是否真的展开。改完导航结构跑一次。

## 写一篇新 blog 的流程

固定流程，不再逐次讨论。完整版见 `SITE-STRUCTURE.md` 15.4.1。

1. **规划**：从 `SITE-STRUCTURE.md` 15.4 的队列里挑缺口，先 grep 核实站内数据撑不撑得起整篇，给用户看主词、结构、每个数字的出处、内链外链、入口位置，**并问配图方案**
2. **用户拍板**选题与配图
3. **AI 生成 900×600 JPG 母版**，落在 `raw-images/<slug>/masters/`，文件名要有语义（如 `blog-cost-quote.jpg`）
4. **用户去水印**（AI 生成的图右下角有「AI生成 WORKBUDS」水印），放回原位
5. **AI 转码**：跑 `scripts/blog_images.py`，输出 1400×933 + 700×467 的 webp 与 jpg 到 `assets/images/`
6. **AI 写正文与接线**：内链 2–5 条、外链 1–4 条、FAQ、CTA，同步 sitemap / feed / llms.txt，索引页收录
7. **AI 全量校验**：`check.py` + `nav_responsive.py` + 截图肉眼过一遍
8. **给用户看效果**，等确认
9. **用户确认后**才 commit 并 push

红线：正文**不出现任何单价、单价区间、百分比成本或汇率**，讲「什么决定报价」不报数；不写具体关税数字；每个数字都要有站内出处；不编造工厂参数。

入口：新文章进 `blog/index.html`（自动成为头条大卡），**不进导航**，不进首页 Journal 精选。

```bash
python scripts/blog_images.py --slug cost-factors   # 转码某篇文章的母版
```

## 部署

纯静态站点，可直接托管在任意静态平台（GitHub Pages、Netlify、Vercel、Cloudflare Pages、传统虚拟主机均可）。子目录会被静态服务器原样映射成 URL 路径，无需任何配置。

以 GitHub Pages 为例：仓库 Settings → Pages → Source 选择 `main` 分支、根目录。

> 仓库根目录已有 `CNAME` 文件，内容为 `www.chinapinsfactory.com`，与站内 canonical 域名一致。要让 GitHub Pages 通过这个自定义域名访问，还需在域名 DNS 处配置 CNAME 记录指向 `<用户名>.github.io`（若 DNS 服务商同时要求 A 记录，按 GitHub 提示补上）。

## 旧 URL 迁移

站点早期是扁平结构，2026-10-25 改为分类目录。旧地址仍可能被外部链接或书签引用：

- `404.html` 内置了旧路径 → 新路径的跳转表，命中即自动跳走（不留死链）。
- 真正的 301 需要在 Cloudflare 侧配置（当前域名已套 Cloudflare 代理）：Rules → Redirect Rules → Bulk Redirect，按下方对照表逐条添加，状态码选 301。

| 旧路径 | 新路径 |
|---|---|
| `/wholesale-custom-pins.html` | `/products/custom-enamel-pins.html` |
| `/custom-metal-swag.html` | `/products/custom-metal-swag.html` |
| `/custom-metal-badges.html` | `/products/custom-metal-badges.html` |
| `/samples.html` | `/products/samples.html` |
| `/wholesale-quote.html` | `/products/request-a-quote.html` |
| `/bulk-order-guide.html` | `/guides/bulk-order-guide.html` |
| `/faq.html` | `/guides/faq.html` |
| `/china-pin-factory.html` | `/company/factory.html` |
| `/contact.html` | `/company/contact.html` |
| `/blog.html` | `/blog/` |
| `/blog-how-to-order-custom-lapel-pins-from-china.html` | `/blog/how-to-order-custom-lapel-pins-from-china.html` |
| `/blog-hard-enamel-vs-soft-enamel-pins.html` | `/blog/hard-enamel-vs-soft-enamel-pins.html` |
| `/blog-lapel-pin-sizes-guide.html` | `/blog/lapel-pin-sizes-guide.html` |
| `/blog-custom-challenge-coin-sizes-guide.html` | `/blog/custom-challenge-coin-sizes-guide.html` |
| `/privacy-policy.html` | `/legal/privacy-policy.html` |

## 表单

全站四个表单（首页询价、首页规格速配器、询价页、联系页）统一走 [Web3Forms](https://web3forms.com)，提交逻辑集中在 `assets/js/main.js` 的 `forms` 数组。

Web3Forms 的 `access_key` 以隐藏字段形式写在四个表单里（`index.html` 两处、`products/request-a-quote.html` 一处、`company/contact.html` 一处），全站同一个值。更换 key 时四处必须同步改。

提交成功后跳转 `thank-you.html`，失败则原地显示错误提示。跳转目标由 `main.js` 依据脚本自身地址反推站点根路径，因此页面放在任何层级都不会跳错。

**上线前需要处理的一件事：**

`SITE-STRUCTURE.md` 第十三章列出了上线前必须替换或确认的数据（联系方式、产能设备、合规声明、交期与打样、起订量表述），请逐项核对后同步修改 HTML、Schema 与 FAQ。

## 两条硬规则

1. **`thank-you.html` 站内零入口链接。** 它只能由脚本在表单提交成功后跳转进入，不得出现在导航、页脚或任何内容区的 `<a href>` 中，也不进 `sitemap.xml`（`noindex, nofollow`）。
2. **全站不公开价格。** 不出现单价、阶梯价、MOQ、免模门槛等表述，报价一律走询价表单。
