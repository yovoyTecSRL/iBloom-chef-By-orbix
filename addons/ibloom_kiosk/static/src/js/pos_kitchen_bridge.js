/** @odoo-module **/

(() => {
    "use strict";

    const REFRESH_MS = 3000;

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function formatQty(value) {
        const number = Number(value || 0);

        if (Number.isInteger(number)) {
            return String(number);
        }

        return number.toFixed(2)
            .replace(/0+$/, "")
            .replace(/\.$/, "");
    }

    function stateContainer(state) {

        if (state === "preparing") {
            return document.getElementById(
                "ibloom-kitchen-preparing"
            );
        }

        if (state === "ready") {
            return document.getElementById(
                "ibloom-kitchen-ready"
            );
        }

        return document.getElementById(
            "ibloom-kitchen-new"
        );
    }

    function buttonsFor(order) {

        if (order.state === "new") {
            return `
                <button
                    class="ibloom-pos-action primary"
                    data-id="${order.id}"
                    data-state="preparing">
                    🔥 Preparar
                </button>
            `;
        }

        if (order.state === "preparing") {
            return `
                <button
                    class="ibloom-pos-action secondary"
                    data-id="${order.id}"
                    data-state="new">
                    ← Recepción
                </button>

                <button
                    class="ibloom-pos-action primary"
                    data-id="${order.id}"
                    data-state="ready">
                    ✅ Listo
                </button>
            `;
        }

        if (order.state === "ready") {
            return `
                <button
                    class="ibloom-pos-action secondary"
                    data-id="${order.id}"
                    data-state="preparing">
                    ← Preparando
                </button>

                <button
                    class="ibloom-pos-action primary"
                    data-id="${order.id}"
                    data-state="delivered">
                    🛎️ Entregado
                </button>
            `;
        }

        return "";
    }

    function renderCard(order) {

        const products = order.lines.map(
            line => `
                <div class="ibloom-pos-product">
                    <span class="ibloom-pos-qty">
                        ${escapeHtml(
                            formatQty(line.qty)
                        )} ×
                    </span>

                    <span class="ibloom-pos-product-name">
                        ${escapeHtml(line.name)}
                    </span>

                    ${
                        line.note
                        ? `
                            <div class="ibloom-pos-note">
                                📝 ${escapeHtml(
                                    line.note
                                )}
                            </div>
                        `
                        : ""
                    }
                </div>
            `
        ).join("");

        const table = order.table
            ? `
                <div class="ibloom-pos-table">
                    🪑 MESA ${escapeHtml(
                        order.table
                    )}
                </div>
            `
            : `
                <div class="ibloom-pos-table">
                    🥡 POS DELI
                </div>
            `;

        return `
            <article
                class="ibloom-pos-kitchen-card"
                data-pos-order-id="${order.id}">

                <div class="ibloom-pos-header">

                    <div>
                        ${table}

                        <div class="ibloom-pos-ref">
                            ${escapeHtml(
                                order.name
                            )}
                        </div>
                    </div>

                    <div class="ibloom-pos-time">
                        🕒 ${escapeHtml(
                            order.time
                        )}
                    </div>

                </div>

                <div class="ibloom-pos-products">
                    ${products}
                </div>

                <div class="ibloom-pos-footer">
                    ${buttonsFor(order)}
                </div>

            </article>
        `;
    }

    async function fetchOrders() {

        const response = await fetch(
            "/ibloom/pos-kitchen/orders",
            {
                method: "GET",
                cache: "no-store",
                headers: {
                    "Accept":
                        "application/json",
                },
            }
        );

        if (!response.ok) {
            throw new Error(
                "No fue posible leer POS Cocina"
            );
        }

        const data =
            await response.json();

        if (!data.ok) {
            throw new Error(
                data.error ||
                "Error POS Cocina"
            );
        }

        return data.orders || [];
    }

    async function changeState(
        orderId,
        state
    ) {

        const response = await fetch(
            "/ibloom/pos-kitchen/state",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                },

                body:
                    JSON.stringify({
                        order_id:
                            Number(orderId),
                        state:
                            state,
                    }),
            }
        );

        const data =
            await response.json();

        if (!response.ok || !data.ok) {
            throw new Error(
                data.error ||
                "No fue posible actualizar"
            );
        }

        return data;
    }

    async function render() {

        const root =
            document.getElementById(
                "ibloom-kitchen"
            );

        if (!root) {
            return;
        }

        document
            .querySelectorAll(
                ".ibloom-pos-kitchen-card"
            )
            .forEach(
                card => card.remove()
            );

        try {

            const orders =
                await fetchOrders();

            for (const order of orders) {

                const target =
                    stateContainer(
                        order.state
                    );

                if (!target) {
                    continue;
                }

                target.insertAdjacentHTML(
                    "beforeend",
                    renderCard(order)
                );
            }

        } catch (error) {
            console.error(
                "[iBLOOM POS Cocina]",
                error
            );
        }
    }

    document.addEventListener(
        "click",
        async event => {

            const button =
                event.target.closest(
                    ".ibloom-pos-action"
                );

            if (!button) {
                return;
            }

            button.disabled = true;

            try {

                await changeState(
                    button.dataset.id,
                    button.dataset.state
                );

                await render();

            } catch (error) {

                console.error(
                    "[iBLOOM POS Cocina]",
                    error
                );

                alert(
                    error.message ||
                    "No fue posible actualizar"
                );

            } finally {
                button.disabled = false;
            }
        }
    );

    function start() {

        const root =
            document.getElementById(
                "ibloom-kitchen"
            );

        if (!root) {
            return;
        }

        render();

        window.setInterval(
            render,
            REFRESH_MS
        );
    }

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            start
        );
    } else {
        start();
    }

})();
