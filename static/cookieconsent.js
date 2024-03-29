/*!
 * CookieConsent v2.9.2
 * https://www.github.com/orestbida/cookieconsent
 * Author Orest Bida
 * Released under the MIT License
 */
!(function () {
  "use strict";
  var n = "initCookieConsent";
  "undefined" != typeof window &&
    "function" != typeof window[n] &&
    (window[n] = function (n) {
      var t,
        o,
        e,
        i,
        r,
        a,
        c,
        u,
        f,
        d,
        v,
        l,
        s,
        p,
        b,
        m,
        y,
        g,
        h,
        _,
        w,
        k,
        x,
        S,
        J,
        O,
        j,
        N,
        T,
        D,
        C,
        U,
        z,
        E,
        I,
        L = {
          mode: "opt-in",
          current_lang: "en",
          auto_language: null,
          autorun: !0,
          page_scripts: !0,
          hide_from_bots: !0,
          cookie_name: "cc_cookie",
          cookie_expiration: 182,
          cookie_domain: location.hostname,
          cookie_path: "/",
          cookie_same_site: "Lax",
          use_rfc_cookie: !1,
          autoclear_cookies: !0,
          revision: 0,
          script_selector: "data-cookiecategory",
        },
        M = {},
        R = {},
        A = null,
        G = !0,
        H = !1,
        P = !1,
        q = !1,
        B = !1,
        F = !0,
        K = [],
        Q = !1,
        V = [],
        W = [],
        X = [],
        Y = !1,
        Z = [],
        $ = [],
        nn = [],
        tn = [],
        on = [],
        en = document.documentElement,
        rn = function (n) {
          "number" == typeof (t = n).cookie_expiration &&
            (L.cookie_expiration = t.cookie_expiration),
            "number" == typeof t.cookie_necessary_only_expiration &&
              (L.cookie_necessary_only_expiration =
                t.cookie_necessary_only_expiration),
            "boolean" == typeof t.autorun && (L.autorun = t.autorun),
            "string" == typeof t.cookie_domain &&
              (L.cookie_domain = t.cookie_domain),
            "string" == typeof t.cookie_same_site &&
              (L.cookie_same_site = t.cookie_same_site),
            "string" == typeof t.cookie_path && (L.cookie_path = t.cookie_path),
            "string" == typeof t.cookie_name && (L.cookie_name = t.cookie_name),
            "function" == typeof t.onAccept && (v = t.onAccept),
            "function" == typeof t.onFirstAction && (s = t.onFirstAction),
            "function" == typeof t.onChange && (l = t.onChange),
            "opt-out" === t.mode && (L.mode = "opt-out"),
            "number" == typeof t.revision &&
              (t.revision > -1 && (L.revision = t.revision), (B = !0)),
            "boolean" == typeof t.autoclear_cookies &&
              (L.autoclear_cookies = t.autoclear_cookies),
            !0 === t.use_rfc_cookie && (L.use_rfc_cookie = !0),
            "boolean" == typeof t.hide_from_bots &&
              (L.hide_from_bots = t.hide_from_bots),
            L.hide_from_bots &&
              (Y =
                navigator &&
                ((navigator.userAgent &&
                  /bot|crawl|spider|slurp|teoma/i.test(navigator.userAgent)) ||
                  navigator.webdriver)),
            (L.page_scripts = !0 === t.page_scripts),
            "browser" === t.auto_language || !0 === t.auto_language
              ? (L.auto_language = "browser")
              : "document" === t.auto_language &&
                (L.auto_language = "document"),
            L.auto_language,
            (L.current_lang = sn(t.languages, t.current_lang));
        },
        an = function (n) {
          for (
            var t = "accept-",
              o = c("c-settings"),
              e = c(t + "all"),
              i = c(t + "necessary"),
              r = c(t + "custom"),
              a = 0;
            a < o.length;
            a++
          )
            o[a].setAttribute("aria-haspopup", "dialog"),
              wn(o[a], "click", function (n) {
                n.preventDefault(), M.showSettings(0);
              });
          for (a = 0; a < e.length; a++)
            wn(e[a], "click", function (n) {
              u(n, "all");
            });
          for (a = 0; a < r.length; a++)
            wn(r[a], "click", function (n) {
              u(n);
            });
          for (a = 0; a < i.length; a++)
            wn(i[a], "click", function (n) {
              u(n, []);
            });
          function c(t) {
            return (n || document).querySelectorAll('[data-cc="' + t + '"]');
          }
          function u(n, t) {
            n.preventDefault(), M.accept(t), M.hideSettings(), M.hide();
          }
        },
        cn = function (n, t) {
          return t.hasOwnProperty(n)
            ? n
            : kn(t).length > 0
            ? t.hasOwnProperty(L.current_lang)
              ? L.current_lang
              : kn(t)[0]
            : void 0;
        },
        un = function (n) {
          if ((!0 === t.force_consent && xn(en, "force--consent"), !h)) {
            h = ln("div");
            var o = ln("div"),
              e = ln("div");
            (h.id = "cm"),
              (o.id = "c-inr-i"),
              (e.id = "cm-ov"),
              (h.tabIndex = -1),
              h.setAttribute("role", "dialog"),
              h.setAttribute("aria-modal", "true"),
              h.setAttribute("aria-hidden", "false"),
              h.setAttribute("aria-labelledby", "c-ttl"),
              h.setAttribute("aria-describedby", "c-txt"),
              g.appendChild(h),
              g.appendChild(e),
              (h.style.visibility = e.style.visibility = "hidden"),
              (e.style.opacity = 0);
          }
          var i = t.languages[n].consent_modal.title;
          i &&
            (_ || (((_ = ln("h2")).id = "c-ttl"), o.appendChild(_)),
            (_.innerHTML = i));
          var r = t.languages[n].consent_modal.description;
          B &&
            (r = F
              ? r.replace("{{revision_message}}", "")
              : r.replace(
                  "{{revision_message}}",
                  t.languages[n].consent_modal.revision_message || ""
                )),
            w || (((w = ln("div")).id = "c-txt"), o.appendChild(w)),
            (w.innerHTML = r);
          var a,
            c = t.languages[n].consent_modal.primary_btn,
            u = t.languages[n].consent_modal.secondary_btn;
          c &&
            (k ||
              (((k = ln("button")).id = "c-p-bn"),
              (k.className = "c-bn"),
              k.appendChild(On(1)),
              "accept_all" === c.role && (a = "all"),
              wn(k, "click", function () {
                M.hide(), M.accept(a);
              })),
            (k.firstElementChild.innerHTML =
              t.languages[n].consent_modal.primary_btn.text)),
            u &&
              (x ||
                (((x = ln("button")).id = "c-s-bn"),
                (x.className = "c-bn c_link"),
                x.appendChild(On(1)),
                "accept_necessary" === u.role
                  ? wn(x, "click", function () {
                      M.hide(), M.accept([]);
                    })
                  : wn(x, "click", function () {
                      M.showSettings(0);
                    })),
              (x.firstElementChild.innerHTML =
                t.languages[n].consent_modal.secondary_btn.text));
          var f = t.gui_options;
          J || (((J = ln("div")).id = "c-inr"), J.appendChild(o)),
            S ||
              (((S = ln("div")).id = "c-bns"),
              f && f.consent_modal && !0 === f.consent_modal.swap_buttons
                ? (u && S.appendChild(x),
                  c && S.appendChild(k),
                  (S.className = "swap"))
                : (c && S.appendChild(k), u && S.appendChild(x)),
              (c || u) && J.appendChild(S),
              h.appendChild(J)),
            (H = !0),
            an(J);
        },
        fn = function (n) {
          if (O) (C = ln("div")).id = "s-bl";
          else {
            (O = ln("div")).tabIndex = -1;
            var o = ln("div"),
              e = ln("div"),
              i = ln("div");
            (j = ln("div")), (N = ln("h2"));
            var r = ln("div");
            (T = ln("button")).appendChild(On(2));
            var a = ln("div");
            D = ln("div");
            var c = ln("div"),
              u = !1;
            wn(O, "mouseup", function (n) {
              !q || u || j.contains(n.target) || M.hideSettings();
            }),
              wn(O, "mousedown", function (n) {
                q && (u = j.contains(n.target));
              }),
              (O.id = "s-cnt"),
              (o.id = "c-vln"),
              (i.id = "c-s-in"),
              (e.id = "cs"),
              (N.id = "s-ttl"),
              (j.id = "s-inr"),
              (r.id = "s-hdr"),
              (D.id = "s-bl"),
              (T.id = "s-c-bn"),
              (c.id = "cs-ov"),
              (a.id = "s-c-bnc"),
              (T.className = "c-bn"),
              O.setAttribute("role", "dialog"),
              O.setAttribute("aria-modal", "true"),
              O.setAttribute("aria-hidden", "true"),
              O.setAttribute("aria-labelledby", "s-ttl"),
              (O.style.visibility = c.style.visibility = "hidden"),
              (c.style.opacity = 0),
              a.appendChild(T),
              wn(
                document,
                "keydown",
                function (n) {
                  27 === n.keyCode && q && M.hideSettings();
                },
                !0
              ),
              wn(T, "click", function () {
                M.hideSettings();
              });
          }
          var v = t.languages[n].settings_modal;
          T.setAttribute("aria-label", v.close_btn_label || "Close"),
            (d = v.blocks),
            (f = v.cookie_table_headers);
          var l = v.cookie_table_caption,
            s = d.length;
          N.innerHTML = v.title;
          for (var p = 0; p < s; ++p) {
            var b = d[p].title,
              m = d[p].description,
              y = d[p].toggle,
              h = d[p].cookie_table,
              _ = !0 === t.remove_cookie_tables,
              w = !!m || (!_ && !!h),
              k = ln("div"),
              x = ln("div");
            if (m) {
              var S = ln("div");
              (S.className = "p"), S.insertAdjacentHTML("beforeend", m);
            }
            var J = ln("div");
            if (
              ((J.className = "title"),
              (k.className = "c-bl"),
              (x.className = "desc"),
              void 0 !== y)
            ) {
              var L = "c-ac-" + p,
                A = ln(w ? "button" : "div"),
                H = ln("label"),
                P = ln("input"),
                B = ln("span"),
                F = ln("span"),
                K = ln("span"),
                Q = ln("span");
              (A.className = w ? "b-tl exp" : "b-tl"),
                (H.className = "b-tg"),
                (P.className = "c-tgl"),
                (K.className = "on-i"),
                (Q.className = "off-i"),
                (B.className = "c-tg"),
                (F.className = "t-lb"),
                w &&
                  (A.setAttribute("aria-expanded", "false"),
                  A.setAttribute("aria-controls", L)),
                (P.type = "checkbox"),
                B.setAttribute("aria-hidden", "true");
              var V = y.value;
              (P.value = V),
                (F.textContent = b),
                A.insertAdjacentHTML("beforeend", b),
                J.appendChild(A),
                B.appendChild(K),
                B.appendChild(Q),
                G
                  ? y.enabled
                    ? ((P.checked = !0),
                      !C && nn.push(!0),
                      y.enabled && !C && X.push(V))
                    : !C && nn.push(!1)
                  : vn(R.categories, V) > -1
                  ? ((P.checked = !0), !C && nn.push(!0))
                  : !C && nn.push(!1),
                !C && tn.push(V),
                y.readonly &&
                  ((P.disabled = !0), xn(B, "c-ro"), !C && on.push(V)),
                xn(x, "b-acc"),
                xn(J, "b-bn"),
                xn(k, "b-ex"),
                (x.id = L),
                x.setAttribute("aria-hidden", "true"),
                H.appendChild(P),
                H.appendChild(B),
                H.appendChild(F),
                J.appendChild(H),
                w &&
                  (function (n, t, o) {
                    wn(
                      A,
                      "click",
                      function () {
                        Jn(t, "act")
                          ? (Sn(t, "act"),
                            o.setAttribute("aria-expanded", "false"),
                            n.setAttribute("aria-hidden", "true"))
                          : (xn(t, "act"),
                            o.setAttribute("aria-expanded", "true"),
                            n.setAttribute("aria-hidden", "false"));
                      },
                      !1
                    );
                  })(x, k, A);
            } else if (b) {
              var W = ln("div");
              (W.className = "b-tl"),
                W.setAttribute("role", "heading"),
                W.setAttribute("aria-level", "3"),
                W.insertAdjacentHTML("beforeend", b),
                J.appendChild(W);
            }
            if (
              (b && k.appendChild(J), m && x.appendChild(S), !_ && void 0 !== h)
            ) {
              for (
                var Y = document.createDocumentFragment(), Z = 0;
                Z < f.length;
                ++Z
              ) {
                var $ = ln("th"),
                  en = f[Z];
                if (($.setAttribute("scope", "col"), en)) {
                  var rn = en && kn(en)[0];
                  ($.textContent = f[Z][rn]), Y.appendChild($);
                }
              }
              var an = ln("tr");
              an.appendChild(Y);
              var cn = ln("thead");
              cn.appendChild(an);
              var un = ln("table");
              if (l) {
                var fn = ln("caption");
                (fn.innerHTML = l), un.appendChild(fn);
              }
              un.appendChild(cn);
              for (
                var dn = document.createDocumentFragment(), sn = 0;
                sn < h.length;
                sn++
              ) {
                for (var pn = ln("tr"), bn = 0; bn < f.length; ++bn)
                  if ((en = f[bn])) {
                    rn = kn(en)[0];
                    var mn = ln("td");
                    mn.insertAdjacentHTML("beforeend", h[sn][rn]),
                      mn.setAttribute("data-column", en[rn]),
                      pn.appendChild(mn);
                  }
                dn.appendChild(pn);
              }
              var yn = ln("tbody");
              yn.appendChild(dn), un.appendChild(yn), x.appendChild(un);
            }
            ((y && b) || (!y && (b || m))) &&
              (k.appendChild(x), C ? C.appendChild(k) : D.appendChild(k));
          }
          U || ((U = ln("div")).id = "s-bns"),
            E ||
              (((E = ln("button")).id = "s-all-bn"),
              (E.className = "c-bn"),
              U.appendChild(E),
              wn(E, "click", function () {
                M.accept("all"), M.hideSettings(), M.hide();
              })),
            (E.innerHTML = v.accept_all_btn);
          var gn = v.reject_all_btn;
          if (
            (gn &&
              (I ||
                (((I = ln("button")).id = "s-rall-bn"),
                (I.className = "c-bn"),
                wn(I, "click", function () {
                  M.accept([]), M.hideSettings(), M.hide();
                }),
                (j.className = "bns-t"),
                U.appendChild(I)),
              (I.innerHTML = gn)),
            z ||
              (((z = ln("button")).id = "s-sv-bn"),
              (z.className = "c-bn"),
              U.appendChild(z),
              wn(z, "click", function () {
                M.accept(), M.hideSettings(), M.hide();
              })),
            (z.innerHTML = v.save_settings_btn),
            C)
          )
            return j.replaceChild(C, D), void (D = C);
          r.appendChild(N),
            r.appendChild(a),
            j.appendChild(r),
            j.appendChild(D),
            j.appendChild(U),
            i.appendChild(j),
            e.appendChild(i),
            o.appendChild(e),
            O.appendChild(o),
            g.appendChild(O),
            g.appendChild(c);
        };
      M.updateLanguage = function (n, o) {
        if ("string" == typeof n) {
          var e = cn(n, t.languages);
          return (
            (e !== L.current_lang || !0 === o) &&
            ((L.current_lang = e), H && un(e), fn(e), !0)
          );
        }
      };
      var dn = function (n) {
          var t = d.length,
            o = -1;
          Q = !1;
          var e = hn("", "all"),
            i = [L.cookie_domain, "." + L.cookie_domain];
          if ("www." === L.cookie_domain.slice(0, 4)) {
            var r = L.cookie_domain.substr(4);
            i.push(r), i.push("." + r);
          }
          for (var a = 0; a < t; a++) {
            var c = d[a];
            if (c.hasOwnProperty("toggle")) {
              var u = vn(K, c.toggle.value) > -1;
              if (!nn[++o] && c.hasOwnProperty("cookie_table") && (n || u)) {
                var v = c.cookie_table,
                  l = kn(f[0])[0],
                  s = v.length;
                "on_disable" === c.toggle.reload && u && (Q = !0);
                for (var p = 0; p < s; p++) {
                  var b = i,
                    m = v[p],
                    y = [],
                    g = m[l],
                    h = m.is_regex || !1,
                    _ = m.domain || null,
                    w = m.path || !1;
                  if ((_ && (b = [_, "." + _]), h))
                    for (var k = 0; k < e.length; k++)
                      e[k].match(g) && y.push(e[k]);
                  else {
                    var x = vn(e, g);
                    x > -1 && y.push(e[x]);
                  }
                  y.length > 0 &&
                    (_n(y, w, b), "on_clear" === c.toggle.reload && (Q = !0));
                }
              }
            }
          }
        },
        vn = function (n, t) {
          return n.indexOf(t);
        },
        ln = function (n) {
          var t = document.createElement(n);
          return "button" === n && t.setAttribute("type", n), t;
        },
        sn = function (n, t) {
          return "browser" === L.auto_language
            ? cn(pn(), n)
            : "document" === L.auto_language
            ? cn(document.documentElement.lang, n)
            : "string" == typeof t
            ? (L.current_lang = cn(t, n))
            : (L.current_lang, L.current_lang);
        },
        pn = function () {
          var n = navigator.language || navigator.browserLanguage;
          return n.length > 2 && (n = n[0] + n[1]), n.toLowerCase();
        };
      (M.allowedCategory = function (n) {
        if (G && "opt-in" !== L.mode) t = X;
        else
          var t =
            JSON.parse(hn(L.cookie_name, "one", !0) || "{}").categories || [];
        return vn(t, n) > -1;
      }),
        (M.run = function (t) {
          if (!document.getElementById("cc_div")) {
            if ((rn(t), Y)) return;
            R = JSON.parse(hn(L.cookie_name, "one", !0) || "{}");
            var c = void 0 !== (i = R.consent_uuid);
            if (
              ((o = R.consent_date) && (o = new Date(o)),
              (e = R.last_consent_update) && (e = new Date(e)),
              (A = void 0 !== R.data ? R.data : null),
              B && R.revision !== L.revision && (F = !1),
              (H = G = !(c && F && o && e && i)),
              (function () {
                ((y = ln("div")).id = "cc--main"),
                  (y.style.position = "fixed"),
                  (y.innerHTML = '<div id="cc_div" class="cc_div"></div>'),
                  (g = y.children[0]);
                var t = L.current_lang;
                H && un(t), fn(t), (n || document.body).appendChild(y);
              })(),
              (function () {
                var n = [
                  "[href]",
                  "button",
                  "input",
                  "details",
                  '[tabindex="0"]',
                ];
                function t(t, o) {
                  try {
                    var e = t.querySelectorAll(
                      n.join(':not([tabindex="-1"]), ')
                    );
                  } catch (o) {
                    return t.querySelectorAll(n.join(", "));
                  }
                  (o[0] = e[0]), (o[1] = e[e.length - 1]);
                }
                t(j, $), H && t(h, Z);
              })(),
              (function (n, t) {
                if ("object" == typeof n) {
                  var o = n.consent_modal,
                    e = n.settings_modal;
                  H &&
                    o &&
                    i(
                      h,
                      ["box", "bar", "cloud"],
                      ["top", "middle", "bottom"],
                      ["zoom", "slide"],
                      o.layout,
                      o.position,
                      o.transition
                    ),
                    e &&
                      i(
                        O,
                        ["bar"],
                        ["left", "right"],
                        ["zoom", "slide"],
                        e.layout,
                        e.position,
                        e.transition
                      );
                }
                function i(n, t, o, e, i, r, a) {
                  if (
                    ((r = (r && r.split(" ")) || []),
                    vn(t, i) > -1 &&
                      (xn(n, i),
                      ("bar" !== i || "middle" !== r[0]) && vn(o, r[0]) > -1))
                  )
                    for (var c = 0; c < r.length; c++) xn(n, r[c]);
                  vn(e, a) > -1 && xn(n, a);
                }
              })(t.gui_options),
              an(),
              L.autorun && H && M.show(t.delay || 0),
              setTimeout(function () {
                xn(y, "c--anim");
              }, 30),
              setTimeout(function () {
                wn(document, "keydown", function (n) {
                  if ("Tab" === n.key && (P || q) && r) {
                    var t = Tn();
                    n.shiftKey
                      ? (t !== r[0] && a.contains(t)) ||
                        (n.preventDefault(), jn(r[1]))
                      : (t !== r[1] && a.contains(t)) ||
                        (n.preventDefault(), jn(r[0]));
                  }
                });
              }, 100),
              G)
            )
              "opt-out" === L.mode && (L.mode, bn());
            else {
              var u = "boolean" == typeof R.rfc_cookie;
              (!u || (u && R.rfc_cookie !== L.use_rfc_cookie)) &&
                ((R.rfc_cookie = L.use_rfc_cookie),
                gn(L.cookie_name, JSON.stringify(R))),
                (p = yn(mn())),
                bn(),
                "function" == typeof v && v(R);
            }
          }
        });
      var bn = function () {
        if (L.page_scripts) {
          var n = R.categories || [];
          G && "opt-out" === L.mode && (n = X);
          var t = document.querySelectorAll(
              "script[" + L.script_selector + "]"
            ),
            o = function (t, e) {
              if (e < t.length) {
                var i = t[e],
                  r = i.getAttribute(L.script_selector);
                if (vn(n, r) > -1) {
                  (i.type = i.getAttribute("data-type") || "text/javascript"),
                    i.removeAttribute(L.script_selector);
                  var a = i.getAttribute("data-src");
                  a && i.removeAttribute("data-src");
                  var c = ln("script");
                  if (
                    ((c.textContent = i.innerHTML),
                    (function (n, t) {
                      for (
                        var o = t.attributes, e = o.length, i = 0;
                        i < e;
                        i++
                      ) {
                        var r = o[i].nodeName;
                        n.setAttribute(r, t[r] || t.getAttribute(r));
                      }
                    })(c, i),
                    a ? (c.src = a) : (a = i.src),
                    a &&
                      (c.readyState
                        ? (c.onreadystatechange = function () {
                            ("loaded" !== c.readyState &&
                              "complete" !== c.readyState) ||
                              ((c.onreadystatechange = null), o(t, ++e));
                          })
                        : (c.onload = function () {
                            (c.onload = null), o(t, ++e);
                          })),
                    i.parentNode.replaceChild(c, i),
                    a)
                  )
                    return;
                }
                o(t, ++e);
              }
            };
          o(t, 0);
        }
      };
      (M.set = function (n, t) {
        return (
          "data" === n &&
          (function (n, t) {
            var o = !1;
            if ("update" === t) {
              var e = typeof (A = M.get("data")) == typeof n;
              if (e && "object" == typeof A)
                for (var i in (!A && (A = {}), n))
                  A[i] !== n[i] && ((A[i] = n[i]), (o = !0));
              else (!e && A) || A === n || ((A = n), (o = !0));
            } else (A = n), (o = !0);
            return o && ((R.data = A), gn(L.cookie_name, JSON.stringify(R))), o;
          })(t.value, t.mode)
        );
      }),
        (M.get = function (n, t) {
          return JSON.parse(hn(t || L.cookie_name, "one", !0) || "{}")[n];
        }),
        (M.getConfig = function (n) {
          return L[n] || t[n];
        });
      var mn = function () {
          return (
            (V = R.categories || []),
            (W = tn.filter(function (n) {
              return -1 === vn(V, n);
            })),
            { accepted: V, rejected: W }
          );
        },
        yn = function (n) {
          var t = "custom",
            o = on.length;
          return (
            n.accepted.length === tn.length
              ? (t = "all")
              : n.accepted.length === o && (t = "necessary"),
            t
          );
        };
      (M.getUserPreferences = function () {
        var n = mn();
        return {
          accept_type: yn(n),
          accepted_categories: n.accepted,
          rejected_categories: n.rejected,
        };
      }),
        (M.loadScript = function (n, t, o) {
          var e = "function" == typeof t;
          if (document.querySelector('script[src="' + n + '"]')) e && t();
          else {
            var i = ln("script");
            if (o && o.length > 0)
              for (var r = 0; r < o.length; ++r)
                o[r] && i.setAttribute(o[r].name, o[r].value);
            e && (i.onload = t), (i.src = n), document.head.appendChild(i);
          }
        }),
        (M.updateScripts = function () {
          bn();
        }),
        (M.show = function (n, t) {
          !0 === t && un(L.current_lang),
            H &&
              ((b = Tn()),
              (r = Z),
              (a = h),
              (P = !0),
              h.removeAttribute("aria-hidden"),
              setTimeout(
                function () {
                  xn(en, "show--consent");
                },
                n > 0 ? n : t ? 30 : 0
              ));
        }),
        (M.hide = function () {
          H &&
            ((P = !1),
            jn(c),
            h.setAttribute("aria-hidden", "true"),
            Sn(en, "show--consent"),
            jn(b),
            (b = null));
        }),
        (M.showSettings = function (n) {
          (q = !0),
            O.removeAttribute("aria-hidden"),
            P ? (m = Tn()) : (b = Tn()),
            (a = O),
            (r = $),
            setTimeout(
              function () {
                xn(en, "show--settings");
              },
              n > 0 ? n : 0
            );
        }),
        (M.hideSettings = function () {
          (q = !1),
            Nn(),
            jn(u),
            O.setAttribute("aria-hidden", "true"),
            Sn(en, "show--settings"),
            P ? (jn(m), (m = null), (a = h), (r = Z)) : (jn(b), (b = null));
        }),
        (M.accept = function (n, t) {
          var r = n || void 0,
            a = t || [],
            c = [];
          if (r)
            if ("object" == typeof r && "number" == typeof r.length)
              for (var u = 0; u < r.length; u++)
                -1 !== vn(tn, r[u]) && c.push(r[u]);
            else
              "string" == typeof r &&
                ("all" === r
                  ? (c = tn.slice())
                  : -1 !== vn(tn, r) && c.push(r));
          else
            c = (function () {
              for (
                var n = document.querySelectorAll(".c-tgl") || [],
                  t = [],
                  o = 0;
                o < n.length;
                o++
              )
                n[o].checked && t.push(n[o].value);
              return t;
            })();
          if (a.length >= 1)
            for (u = 0; u < a.length; u++)
              c = c.filter(function (n) {
                return n !== a[u];
              });
          for (u = 0; u < tn.length; u++)
            !0 === on.includes(tn[u]) && -1 === vn(c, tn[u]) && c.push(tn[u]);
          !(function (n) {
            K = [];
            var t = O.querySelectorAll(".c-tgl") || [];
            if (t.length > 0)
              for (var r = 0; r < t.length; r++)
                -1 !== vn(n, tn[r])
                  ? ((t[r].checked = !0),
                    nn[r] || (K.push(tn[r]), (nn[r] = !0)))
                  : ((t[r].checked = !1),
                    nn[r] && (K.push(tn[r]), (nn[r] = !1)));
            !G && L.autoclear_cookies && K.length > 0 && dn(),
              o || (o = new Date()),
              i ||
                (i = ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(
                  /[018]/g,
                  function (n) {
                    try {
                      return (
                        n ^
                        ((window.crypto || window.msCrypto).getRandomValues(
                          new Uint8Array(1)
                        )[0] &
                          (15 >> (n / 4)))
                      ).toString(16);
                    } catch (n) {
                      return "";
                    }
                  }
                )),
              (R = {
                categories: n,
                level: n,
                revision: L.revision,
                data: A,
                rfc_cookie: L.use_rfc_cookie,
                consent_date: o.toISOString(),
                consent_uuid: i,
              }),
              (G || K.length > 0) &&
                ((F = !0),
                (e = e ? new Date() : o),
                (R.last_consent_update = e.toISOString()),
                (p = yn(mn())),
                gn(L.cookie_name, JSON.stringify(R)),
                bn()),
              (G &&
                (L.autoclear_cookies && dn(!0),
                "function" == typeof s && s(M.getUserPreferences(), R),
                "function" == typeof v && v(R),
                (G = !1),
                "opt-in" === L.mode)) ||
                ("function" == typeof l && K.length > 0 && l(R, K),
                Q && location.reload());
          })(c);
        }),
        (M.eraseCookies = function (n, t, o) {
          var e = [],
            i = o ? [o, "." + o] : [L.cookie_domain, "." + L.cookie_domain];
          if ("object" == typeof n && n.length > 0)
            for (var r = 0; r < n.length; r++)
              this.validCookie(n[r]) && e.push(n[r]);
          else this.validCookie(n) && e.push(n);
          _n(e, t, i);
        });
      var gn = function (n, t) {
          var o = L.cookie_expiration;
          "number" == typeof L.cookie_necessary_only_expiration &&
            "necessary" === p &&
            (o = L.cookie_necessary_only_expiration),
            (t = L.use_rfc_cookie ? encodeURIComponent(t) : t);
          var e = new Date();
          e.setTime(e.getTime() + 24 * o * 60 * 60 * 1e3);
          var i =
            n +
            "=" +
            (t || "") +
            "; expires=" +
            e.toUTCString() +
            "; Path=" +
            L.cookie_path +
            ";";
          (i += " SameSite=" + L.cookie_same_site + ";"),
            location.hostname.indexOf(".") > -1 &&
              L.cookie_domain &&
              (i += " Domain=" + L.cookie_domain + ";"),
            "https:" === location.protocol && (i += " Secure;"),
            (document.cookie = i);
        },
        hn = function (n, t, o) {
          var e;
          if ("one" === t) {
            if (
              (e = (e = document.cookie.match(
                "(^|;)\\s*" + n + "\\s*=\\s*([^;]+)"
              ))
                ? o
                  ? e.pop()
                  : n
                : "") &&
              n === L.cookie_name
            ) {
              try {
                e = JSON.parse(e);
              } catch (n) {
                try {
                  e = JSON.parse(decodeURIComponent(e));
                } catch (n) {
                  e = {};
                }
              }
              e = JSON.stringify(e);
            }
          } else if ("all" === t) {
            var i = document.cookie.split(/;\s*/);
            e = [];
            for (var r = 0; r < i.length; r++) e.push(i[r].split("=")[0]);
          }
          return e;
        },
        _n = function (n, t, o) {
          for (var e = t || "/", i = 0; i < n.length; i++) {
            for (var r = 0; r < o.length; r++)
              document.cookie =
                n[i] +
                "=; path=" +
                e +
                (0 == o[r].indexOf(".") ? "; domain=" + o[r] : "") +
                "; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
            n[i];
          }
        };
      (M.validCookie = function (n) {
        return "" !== hn(n, "one", !0);
      }),
        (M.validConsent = function () {
          return !G;
        });
      var wn = function (n, t, o, e) {
          n.addEventListener(t, o, !0 === e && { passive: !0 });
        },
        kn = function (n) {
          if ("object" == typeof n) return Object.keys(n);
        },
        xn = function (n, t) {
          n.classList.add(t);
        },
        Sn = function (n, t) {
          n.classList.remove(t);
        },
        Jn = function (n, t) {
          return n.classList.contains(t);
        },
        On = function (n) {
          var t = ln("span");
          return (t.tabIndex = -1), 1 === n ? (c = t) : (u = t), t;
        },
        jn = function (n) {
          n && n instanceof HTMLElement && n.focus();
        },
        Nn = function () {
          for (var n = j.querySelectorAll(".c-tgl"), t = 0; t < n.length; t++) {
            var o = n[t].value,
              e = on.includes(o);
            n[t].checked = e || M.allowedCategory(o);
          }
        },
        Tn = function () {
          return document.activeElement;
        };
      return M;
    });
})();
