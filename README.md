# China Pins Factory（CPF）

面向海外批发买家的定制徽章工厂英文站。纯静态站点，无框架、无构建步骤、无依赖。

- 站点结构、关键词地图、SEO 策略与上线检查清单：[`SITE-STRUCTURE.md`](SITE-STRUCTURE.md)
- 生产域名：`https://www.chinapinsfactory.com/`

## 技术栈

原生 HTML + CSS + JavaScript。18 个页面，全部页面共享 `assets/css/styles.css` 与 `assets/js/main.js`。

## 目录结构

```
index.html                  首页（规格速配器 + 询价）
wholesale-custom-pins.html  批发定制别针
wholesale-quote.html        询价页
custom-metal-swag.html      金属周边（挑战币/奖牌/钥匙扣/皮带扣/袖扣）
custom-metal-badges.html    金属徽章
china-pin-factory.html      工厂页
bulk-order-guide.html       批量下单指南
blog.html + blog-*.html     博客（4 篇）
faq.html                    常见问题
samples.html                样品
contact.html                联系方式
privacy-policy.html         隐私政策
thank-you.html              表单提交后落地页
404.html                    404 兜底页
assets/css/styles.css       全站样式
assets/js/main.js           交互脚本（导航、皮肤切换、速配器、表单提交）
assets/images/              图片资源（webp + jpg 双格式，含 srcset 尺寸档）
robots.txt / sitemap.xml    搜索引擎配置
CNAME                      GitHub Pages 自定义域名（www.chinapinsfactory.com）
```

## 本地预览

直接用浏览器打开 `index.html` 即可，**不需要启动本地服务器**。所有资源均为相对路径。

## 部署

纯静态站点，可直接托管在任意静态平台（GitHub Pages、Netlify、Vercel、Cloudflare Pages、传统虚拟主机均可）。

以 GitHub Pages 为例：仓库 Settings → Pages → Source 选择 `main` 分支、根目录。

> 仓库根目录已有 `CNAME` 文件，内容为 `www.chinapinsfactory.com`，与站内 canonical 域名一致。要让 GitHub Pages 通过这个自定义域名访问，还需在域名 DNS 处配置 CNAME 记录指向 `<用户名>.github.io`（若 DNS 服务商同时要求 A 记录，按 GitHub 提示补上）。

## 表单

全站四个表单（首页询价、首页规格速配器、询价页、联系页）统一走 [Web3Forms](https://web3forms.com)，提交逻辑集中在 `assets/js/main.js` 的 `forms` 数组。

Web3Forms 的 `access_key` 以隐藏字段形式写在四个表单里（`index.html` 两处、`wholesale-quote.html` 一处、`contact.html` 一处），全站同一个值。更换 key 时四处必须同步改。

提交成功后跳转 `thank-you.html`，失败则原地显示错误提示。

**上线前需要处理的一件事：**

`SITE-STRUCTURE.md` 第十三章列出了上线前必须替换或确认的数据（联系方式、产能设备、合规声明、交期与打样、起订量表述），请逐项核对后同步修改 HTML、Schema 与 FAQ。

## 两条硬规则

1. **`thank-you.html` 站内零入口链接。** 它只能由脚本在表单提交成功后跳转进入，不得出现在导航、页脚或任何内容区的 `<a href>` 中，也不进 `sitemap.xml`（`noindex, nofollow`）。
2. **全站不公开价格。** 不出现单价、阶梯价、MOQ、免模门槛等表述，报价一律走询价表单。
