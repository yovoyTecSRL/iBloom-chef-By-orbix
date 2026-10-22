/** @odoo-module **/

console.log("[iBLOOM KDS] Contrast Fix V4 loaded");

(function () {
    "use strict";

    if (
        window.location.pathname !== "/cocina" &&
        !window.location.pathname.startsWith("/cocina/")
    ) {
        return;
    }

    document.body.classList.add(
        "ibloom-kitchen-contrast-active"
    );

    function rgbValues(value) {
        if (!value) {
            return null;
        }

        const match = value.match(
            /rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)/
        );

        if (!match) {
            return null;
        }

        return {
            r: Number(match[1]),
            g: Number(match[2]),
            b: Number(match[3]),
        };
    }

    function luminance(rgb) {
        if (!rgb) {
            return null;
        }

        return (
            0.2126 * rgb.r +
            0.7152 * rgb.g +
            0.0722 * rgb.b
        );
    }

    function isVeryLightColor(value) {
        const rgb = rgbValues(value);

        if (!rgb) {
            return false;
        }

        return luminance(rgb) > 190;
    }

    function isLightBackground(element) {
        let node = element;

        for (let i = 0; node && i < 6; i++) {
            const style = window.getComputedStyle(node);
            const bg = rgbValues(style.backgroundColor);

            if (
                bg &&
                style.backgroundColor !==
                    "rgba(0, 0, 0, 0)"
            ) {
                return luminance(bg) > 175;
            }

            node = node.parentElement;
        }

        return false;
    }

    function shouldIgnore(element) {
        if (!element || element.nodeType !== 1) {
            return true;
        }

        if (
            element.closest(
                "header, nav, footer, .o_header_standard, " +
                ".navbar, .o_footer"
            )
        ) {
            return true;
        }

        /*
         * Botones coloreados:
         * no cambiamos su color blanco.
         */
        if (
            element.matches(
                "button, .btn, a.btn, [role='button']"
            ) ||
            element.closest(
                "button, .btn, a.btn, [role='button']"
            )
        ) {
            return true;
        }

        return false;
    }

    function forceDark(element) {
        element.classList.add("ibloom-force-dark");

        /*
         * setProperty(..., important) vence incluso
         * estilos declarados inline.
         */
        element.style.setProperty(
            "color",
            "#111111",
            "important"
        );

        element.style.setProperty(
            "-webkit-text-fill-color",
            "#111111",
            "important"
        );

        element.style.setProperty(
            "text-shadow",
            "none",
            "important"
        );

        element.style.setProperty(
            "opacity",
            "1",
            "important"
        );
    }

    function processElement(element) {
        if (shouldIgnore(element)) {
            return;
        }

        const text =
            (element.textContent || "").trim();

        if (!text) {
            return;
        }

        /*
         * No procesamos grandes contenedores.
         */
        if (element.children.length > 12) {
            return;
        }

        const style =
            window.getComputedStyle(element);

        const color = style.color;

        /*
         * Caso principal:
         * texto claro/blanco sobre fondo claro.
         */
        if (
            isVeryLightColor(color) &&
            isLightBackground(element)
        ) {
            forceDark(element);

            const card = element.closest(
                ".card, article, section, " +
                "[class*='ticket'], " +
                "[class*='kitchen'], " +
                "[class*='order'], " +
                "[class*='mesa'], " +
                "[class*='table']"
            );

            if (card) {
                card.classList.add(
                    "ibloom-light-kds-card"
                );
            }
        }
    }

    function scan(root = document) {
        const elements =
            root.querySelectorAll
                ? root.querySelectorAll(
                      "div, span, p, strong, b, " +
                      "small, label, h1, h2, h3, " +
                      "h4, h5, h6, li"
                  )
                : [];

        elements.forEach(processElement);
    }

    /*
     * Primera pasada.
     */
    function initialScan() {
        scan(document);

        /*
         * Algunos componentes OWL llegan
         * algunos milisegundos después.
         */
        setTimeout(() => scan(document), 300);
        setTimeout(() => scan(document), 1000);
        setTimeout(() => scan(document), 2500);
    }

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialScan
        );
    } else {
        initialScan();
    }

    /*
     * Los pedidos cambian dinámicamente.
     * Corregir automáticamente cualquier ticket nuevo.
     */
    const observer = new MutationObserver(
        (mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach(
                    (node) => {
                        if (
                            node.nodeType !==
                            Node.ELEMENT_NODE
                        ) {
                            return;
                        }

                        processElement(node);
                        scan(node);
                    }
                );

                if (
                    mutation.type === "attributes" &&
                    mutation.target
                ) {
                    processElement(
                        mutation.target
                    );
                }
            });
        }
    );

    observer.observe(document.documentElement, {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: [
            "class",
            "style",
        ],
    });

    /*
     * Rescan periódico de respaldo.
     */
    window.setInterval(
        () => scan(document),
        3000
    );

    console.log(
        "[iBLOOM KDS] Contrast observer active"
    );
})();
