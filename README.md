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
