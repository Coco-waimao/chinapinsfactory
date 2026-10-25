/**
 * China Pins Factory — site behaviour
 * Navigation drawer, spec builder, FAQ accordion, RFQ feedback, skin switcher.
 */

(function () {
  'use strict';

  var STORE_KEY = 'cpf-skin';

  /* 站点根路径。页面分布在不同层级的子目录里，但 thank-you.html 固定在根目录，
     所以用脚本自身的地址反推根路径：.../assets/js/main.js -> .../
     currentScript 在脚本同步执行期间有效；万一取不到，退回查询 <script> 标签。 */
  var SITE_ROOT = (function () {
    var src = '';
    if (document.currentScript && document.currentScript.src) {
      src = document.currentScript.src;
    } else {
      var tag = document.querySelector('script[src*="assets/js/main.js"]');
      if (tag) { src = tag.src; }
    }
    if (src) { return src.replace(/\/assets\/js\/main\.js(\?.*)?$/, '/'); }
    if (window.location.origin && window.location.origin !== 'null') {
      return window.location.origin + '/';
    }
    return './';
  })();
  var THANK_YOU_URL = SITE_ROOT + 'thank-you.html';

  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); }
    else { document.addEventListener('DOMContentLoaded', fn); }
  }

  ready(function () {

    /* ---------------------------------------------------------- 1. Navigation */
    var navToggle = document.getElementById('navToggle');
    var nav = document.getElementById('mainNav');

    if (navToggle && nav) {
      navToggle.addEventListener('click', function () {
        var open = nav.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', String(open));
      });
      nav.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          nav.classList.remove('is-open');
          navToggle.setAttribute('aria-expanded', 'false');
        }
      });
    }

    /* ------------------------------------------------------- 2. Skin switcher */
    var skin = document.getElementById('skinSwitcher');
    var skinToggle = document.getElementById('skinToggle');

    if (skin && skinToggle) {
      var skinButtons = skin.querySelectorAll('.skin__opt');

      function applySkin(name) {
        document.documentElement.setAttribute('data-theme', name);
        skinButtons.forEach(function (btn) {
          btn.setAttribute('aria-pressed', String(btn.getAttribute('data-skin') === name));
        });
        try { localStorage.setItem(STORE_KEY, name); } catch (e) {}
      }

      skinToggle.addEventListener('click', function () {
        var open = skin.classList.toggle('is-open');
        skinToggle.setAttribute('aria-expanded', String(open));
      });

      skinButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          applySkin(btn.getAttribute('data-skin'));
        });
      });

      var stored = null;
      try { stored = localStorage.getItem(STORE_KEY); } catch (e) {}
      applySkin(stored || document.documentElement.getAttribute('data-theme') || 'ink');

      document.addEventListener('click', function (e) {
        if (!skin.contains(e.target)) {
          skin.classList.remove('is-open');
          skinToggle.setAttribute('aria-expanded', 'false');
        }
      });
    }

    /* -------------------------------------------------------- 3. Spec builder */
    var PROCESS = {
      'hard-enamel': {
        label: 'Hard enamel',
        metal: 'Brass or iron',
        colors: 'Up to 4 Pantone',
        tooling: 'CNC steel mould, cut in house',
        lead: '7 to 10 business days',
        finishNote: 'Flat glossy enamel, flush with raised metal lines'
      },
      'soft-enamel': {
        label: 'Soft enamel',
        metal: 'Brass or iron',
        colors: 'Up to 6 Pantone',
        tooling: 'CNC steel mould, cut in house',
        lead: '7 to 10 business days',
        finishNote: 'Recessed colour fill below a raised metal rim'
      },
      'die-struck': {
        label: 'Die struck metal',
        metal: 'Solid brass, bronze or iron',
        colors: 'Metal contrast only',
        tooling: 'CNC steel die, struck in house',
        lead: '7 to 10 business days',
        finishNote: 'Polished relief against a sandblasted or antique recess'
      },
      '3d-die-cast': {
        label: '3D die cast',
        metal: 'Zinc alloy',
        colors: 'Plated, with optional painted detail',
        tooling: 'Two-part die casting mould',
        lead: '10 to 14 business days',
        finishNote: 'Multi-level relief with cast cutouts and moving parts'
      },
      'offset-print': {
        label: 'Offset printed',
        metal: 'Stainless steel or brass blank',
        colors: 'Full colour CMYK',
        tooling: 'No steel mould required',
        lead: '5 to 7 business days',
        finishNote: 'Printed under a clear non-yellowing epoxy dome'
      }
    };

    /* 数量档位只延长的工艺交期，绝不缩短。
       每个档位给出「工艺交期 + 数量带来的额外天数」，
       取两者上限，避免出现「3D 压铸 10-14 天被写成 10-12 天」这类自相矛盾。 */
    var QTY_LEAD = {
      '1': { days: [3, 5], note: 'for a single piece sample' },
      '100': { days: [7, 10], note: '' },
      '500': { days: [7, 10], note: '' },
      '1000': { days: [7, 11], note: '' },
      '5000': { days: [10, 13], note: '' },
      '50000': { days: [12, 16], note: '' }
    };

    function parseLead(text) {
      var m = /(\d+)\s*(?:to|-|–)\s*(\d+)/.exec(text);
      return m ? [parseInt(m[1], 10), parseInt(m[2], 10)] : null;
    }

    var state = { process: 'hard-enamel', size: '1.00', qty: '100', finish: 'Shiny 24K gold' };

    function bindChips(containerId, key) {
      var box = document.getElementById(containerId);
      if (!box) { return; }
      box.addEventListener('click', function (e) {
        var btn = e.target.closest('.chip');
        if (!btn || !box.contains(btn)) { return; }
        box.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        state[key] = btn.getAttribute('data-' + key);
        renderSpec();
      });
    }

    bindChips('processChips', 'process');
    bindChips('sizeChips', 'size');
    bindChips('qtyChips', 'qty');

    var finishSelect = document.getElementById('buildFinish');
    if (finishSelect) {
      finishSelect.addEventListener('change', function () {
        state.finish = finishSelect.value;
        renderSpec();
      });
    }

    function setText(id, value) {
      var el = document.getElementById(id);
      if (el) { el.textContent = value; }
    }

    function setValue(id, value) {
      var el = document.getElementById(id);
      if (el) { el.value = value; }
    }

    function renderSpec() {
      var p = PROCESS[state.process] || PROCESS['hard-enamel'];
      var band = QTY_LEAD[state.qty] || QTY_LEAD['100'];
      var pLead = parseLead(p.lead) || [7, 10];

      // 工艺交期与数量档位取上限：工艺更慢就按工艺走，数量只做加长
      var lo = Math.max(pLead[0], band.days[0]);
      var hi = Math.max(pLead[1], band.days[1]);
      var lead = lo + ' to ' + hi + ' business days';

      if (state.qty === '1') {
        lead = band.days[0] + ' to ' + band.days[1] + ' business days ' + band.note;
      }

      setText('buildHeadline', p.label + ', ' + state.size + ' inch');
      setText('buildMeta', lead + ' in production');
      setText('outMetal', p.metal);
      setText('outColors', p.colors);
      setText('outTooling', p.tooling);
      setText('outFinish', state.finish);
      setText('outBacking', state.qty === '1' ? 'Sample, polybagged' : 'Butterfly clutch, polybagged');
      setText('outQc', '100% piece by piece');
      setText('outLead', lead);

      // 把当前规格同步到表单隐藏字段，提交时随询价一起发给工厂。
      setValue('specProcess', p.label);
      setValue('specSize', state.size + ' inch');
      setValue('specQuantity', state.qty);
      setValue('specFinish', state.finish);
      setValue('specMessage', [
        'Process: ' + p.label,
        'Size: ' + state.size + ' inch',
        'Quantity per design: ' + (state.qty === '1' ? '1 piece sample' : state.qty + ' pieces'),
        'Plating finish: ' + state.finish,
        'Base metal: ' + p.metal,
        'Tooling: ' + p.tooling,
        'Lead time: ' + lead
      ].join('\n'));
    }

    renderSpec();

    /* ------------------------- 4. Carry the spec over to the RFQ page */
    var params = new URLSearchParams(window.location.search);
    if (params.get('process') && document.getElementById('rfqProcess')) {
      var rfqProcess = document.getElementById('rfqProcess');
      var wanted = params.get('process');
      Array.prototype.forEach.call(rfqProcess.options, function (opt) {
        if (opt.value === wanted) { rfqProcess.value = wanted; }
      });
    }
    if (params.get('qty') && document.getElementById('rfqQuantity')) {
      document.getElementById('rfqQuantity').value = params.get('qty');
    }
    if (params.get('size') && document.getElementById('rfqSize')) {
      document.getElementById('rfqSize').value = params.get('size') + ' inch';
    }
    if (params.get('finish') && document.getElementById('rfqFinish')) {
      document.getElementById('rfqFinish').value = params.get('finish');
    }

    /* ------------------------------------------------------- 5. FAQ accordion */
    document.querySelectorAll('.faq__item').forEach(function (item) {
      var btn = item.querySelector('.faq__q');
      if (!btn) { return; }
      btn.addEventListener('click', function () {
        var open = item.classList.toggle('open');
        btn.setAttribute('aria-expanded', String(open));
      });
    });

    /* ------------------------------------------------------ 6. RFQ submission
       表单通过 Web3Forms 提交。字段名保留业务含义，Web3Forms 会把全部字段
       原样转发到邮箱；其中 name / email 用于称呼和回复地址。
       用 fetch + Accept: application/json 拿到 JSON 响应，成功与失败都能
       在原地提示，不跳转、不刷新。 */
    var forms = [
      { form: 'homeRfqForm', success: 'homeRfqSuccess', error: 'homeRfqError' },
      { form: 'b2bRfqForm', success: 'rfqSuccessMessage', error: 'rfqErrorMessage' },
      { form: 'specRfqForm', success: 'specRfqSuccess', error: 'specRfqError', after: renderSpec },
      { form: 'contactRfqForm', success: 'contactRfqSuccess', error: 'contactRfqError' }
    ];

    forms.forEach(function (pair) {
      var form = document.getElementById(pair.form);
      var success = document.getElementById(pair.success);
      var error = document.getElementById(pair.error);
      if (!form) { return; }

      var button = form.querySelector('button[type="submit"]');
      var buttonLabel = button ? button.textContent : '';

      function show(el) {
        if (!el) { return; }
        el.classList.add('is-visible');
        el.setAttribute('tabindex', '-1');
        el.focus({ preventScroll: true });
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }

        if (success) { success.classList.remove('is-visible'); }
        if (error) { error.classList.remove('is-visible'); }

        if (button) {
          button.disabled = true;
          button.classList.add('is-loading');
          button.textContent = 'Sending';
        }

        var payload = {};
        new FormData(form).forEach(function (value, key) {
          payload[key] = value;
        });

        fetch(form.getAttribute('action'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          }).catch(function () {
            return { ok: false, data: null };
          });
        }).then(function (result) {
          if (result.ok && result.data && result.data.success) {
            show(success);
            form.reset();
            // reset() 会清空隐藏字段，规格表单需要把规格重新写回去
            if (pair.after) { pair.after(); }
            // 提交成功后进入感谢页。该页只在提交后展示，站内没有任何链接指向它，
            // 因此不写进 sitemap，也标记为 noindex。
            window.location.href = THANK_YOU_URL;
          } else {
            show(error);
          }
        }).catch(function () {
          show(error);
        }).then(function () {
          if (button) {
            button.disabled = false;
            button.classList.remove('is-loading');
            button.textContent = buttonLabel;
          }
        });
      });
    });

  });
})();
