document.addEventListener("DOMContentLoaded", () => {

    const DELI_URL =
        "/shop/category/ibloom-deli-2";

    const COMBOS_URL =
        "/combos";


    // ========================================================
    // BOTONES FLOTANTES
    // ========================================================

    function createFloatingButtons() {

        if (
            document.getElementById(
                "ibloom-shop-floating"
            )
        ) {
            return;
        }

        const container =
            document.createElement("div");

        container.id =
            "ibloom-shop-floating";

        container.innerHTML = `

            <a
                class="ibloom-float ibloom-float-more"
                href="${DELI_URL}">
                ＋ Agregar más
            </a>

            <a
                class="ibloom-float ibloom-float-combos"
                href="${COMBOS_URL}">
                🍱 Combos
            </a>

        `;

        document.body.appendChild(
            container
        );
    }


    // ========================================================
    // INSERTAR "AGREGAR MÁS" AL LADO DE "VER CARRITO"
    // ========================================================

    function enhanceCartNotification() {

        const elements =
            document.querySelectorAll(
                "a, button"
            );

        elements.forEach(element => {

            const text =
                (
                    element.textContent ||
                    ""
                )
                .trim()
                .toLowerCase();

            if (
                text !== "ver carrito"
            ) {
                return;
            }

            const parent =
                element.parentElement;

            if (!parent) {
                return;
            }

            if (
                parent.querySelector(
                    ".ibloom-add-more"
                )
            ) {
                return;
            }


            // Contenedor de botones
            parent.classList.add(
                "ibloom-cart-actions"
            );


            const more =
                document.createElement(
                    "a"
                );

            more.href =
                DELI_URL;

            more.className =
                "ibloom-add-more";

            more.textContent =
                "＋ Agregar más";

            parent.appendChild(
                more
            );
        });
    }


    // ========================================================
    // BOTÓN COMBOS CERCA DEL BUSCADOR
    // ========================================================

    function addCombosShortcut() {

        if (
            document.getElementById(
                "ibloom-combos-shortcut"
            )
        ) {
            return;
        }


        const candidates = [
            document.querySelector(
                ".o_wsale_products_searchbar_form"
            ),

            document.querySelector(
                "form[role='search']"
            ),

            document.querySelector(
                ".o_wsale_products_main_row"
            ),
        ];


        const target =
            candidates.find(Boolean);

        if (!target) {
            return;
        }


        const button =
            document.createElement(
                "a"
            );

        button.id =
            "ibloom-combos-shortcut";

        button.href =
            COMBOS_URL;

        button.innerHTML =
            "🍱 Ver Combos";

        target.parentNode.insertBefore(
            button,
            target
        );
    }


    // ========================================================
    // OBSERVAR POPUP/OFFCANVAS DE ODOO
    // ========================================================

    const observer =
        new MutationObserver(() => {

            enhanceCartNotification();
            addCombosShortcut();

        });


    observer.observe(
        document.body,
        {
            childList: true,
            subtree: true,
        }
    );


    // Primera ejecución
    createFloatingButtons();
    enhanceCartNotification();
    addCombosShortcut();

});
