
document.addEventListener(
"DOMContentLoaded",
() => {

    const root =
        document.getElementById(
            "ibloom-kitchen"
        );

    if (!root) return;


    const zones = {

        new:
            document.getElementById(
                "ibloom-kitchen-new"
            ),

        preparing:
            document.getElementById(
                "ibloom-kitchen-preparing"
            ),

        ready:
            document.getElementById(
                "ibloom-kitchen-ready"
            ),
    };


    let previousIds = new Set();


    function actionFor(state) {

        if (state === "new") {

            return {
                next: "preparing",
                label:
                    "🔥 COMENZAR",
                cls: "",
                prev: null,
            };
        }

        if (state === "preparing") {

            return {
                next: "ready",
                label:
                    "✅ LISTO",
                cls: "kds-ready",
                prev: "new",
            };
        }

        return {
            next: "delivered",
            label:
                "📦 YA SALIÓ",
            cls: "kds-delivered",
            prev: "preparing",
        };
    }


    function makeCard(order) {

        const action =
            actionFor(order.state);

        const card =
            document.createElement(
                "article"
            );

        card.className =
            "kds-card";

        if (order.elapsed >= 20) {

            card.classList.add(
                "late"
            );

        } else if (
            order.elapsed >= 10
        ) {

            card.classList.add(
                "warning"
            );
        }


        const mode =
            order.mode === "takeaway"
                ? "🥡 PARA LLEVAR"
                : "🍽️ AQUÍ";


        const products =
            order.lines
                .map(line => `
                    <li>
                        <span class="kds-qty">
                            ${line.qty}×
                        </span>

                        <span>
                            ${line.name}
                        </span>
                    </li>
                `)
                .join("");


        let actions = "";

        if (action.prev) {

            actions = `
                <div class="kds-actions">

                    <button
                        class="
                            kds-action
                            kds-prev"
                        data-order="${order.id}"
                        data-state="${action.prev}">

                        ↶
                    </button>

                    <button
                        class="
                            kds-action
                            kds-next
                            ${action.cls}"
                        data-order="${order.id}"
                        data-state="${action.next}">

                        ${action.label}

                    </button>

                </div>
            `;

        } else {

            actions = `
                <div class="
                    kds-actions
                    one">

                    <button
                        class="
                            kds-action
                            kds-next"
                        data-order="${order.id}"
                        data-state="${action.next}">

                        ${action.label}

                    </button>

                </div>
            `;
        }


        card.innerHTML = `

            <div class="kds-card-head">

                <div
                    class="kds-order-number">

                    ${order.name}

                </div>

                <div
                    class="kds-elapsed">

                    ${order.elapsed} min

                </div>

            </div>

            <div class="kds-meta">

                ${order.time}

                ${
                    order.partner
                    ? " · " +
                      order.partner
                    : ""
                }

            </div>

            <div class="kds-mode">

                ${mode}

            </div>

            <ul class="kds-products">

                ${products}

            </ul>

            ${actions}
        `;

        return card;
    }


    function empty(zone) {

        if (zone.children.length)
            return;

        const node =
            document.createElement(
                "div"
            );

        node.className =
            "kds-empty";

        node.innerHTML =
            "Sin pedidos";

        zone.appendChild(node);
    }


    function updateCounts(orders) {

        const counts = {
            new: 0,
            preparing: 0,
            ready: 0,
        };

        orders.forEach(
            order => {

                if (
                    counts[
                        order.state
                    ] !== undefined
                ) {
                    counts[
                        order.state
                    ]++;
                }
            }
        );

        for (
            const state
            of Object.keys(counts)
        ) {

            const a =
                document.getElementById(
                    "count-" + state
                );

            const b =
                document.getElementById(
                    "badge-" + state
                );

            if (a)
                a.textContent =
                    counts[state];

            if (b)
                b.textContent =
                    counts[state];
        }
    }


    async function refreshOrders() {

        const indicator =
            document.getElementById(
                "kds-connection"
            );

        try {

            const response =
                await fetch(
                    "/ibloom/kitchen/all-orders",
                    {
                    credentials: "same-origin",
                        cache: "no-store",
                    }
                );

            if (!response.ok)
                throw new Error(
                    "HTTP " +
                    response.status
                );

            const data =
                await response.json();

            if (!data.ok)
                throw new Error(
                    "Respuesta inválida"
                );


            Object
                .values(zones)
                .forEach(
                    zone => {
                        zone.innerHTML = "";
                    }
                );


            const currentIds =
                new Set(
                    data.orders.map(
                        order =>
                            order.id
                    )
                );


            data.orders.forEach(
                order => {

                    const zone =
                        zones[
                            order.state
                        ];

                    if (zone) {

                        zone.appendChild(
                            makeCard(order)
                        );
                    }
                }
            );


            Object
                .values(zones)
                .forEach(empty);


            updateCounts(
                data.orders
            );


            previousIds =
                currentIds;


            indicator.textContent =
                "● EN LÍNEA";

            indicator.classList.remove(
                "kds-offline"
            );

        } catch (error) {

            console.error(
                "KDS iBLOOM:",
                error
            );

            indicator.textContent =
                "● SIN CONEXIÓN";

            indicator.classList.add(
                "kds-offline"
            );
        }
    }


    async function changeState(
        orderId,
        state
    ) {

        const response =
            await fetch(
                "/ibloom/kitchen/state",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify({
                            order_id:
                                Number(
                                    orderId
                                ),
                            state:
                                state,
                        }),
                }
            );

        const data =
            await response.json();

        if (!response.ok ||
            !data.ok) {

            throw new Error(
                data.error ||
                "No fue posible actualizar"
            );
        }
    }


    root.addEventListener(
        "click",
        async event => {

            const button =
                event.target.closest(
                    ".kds-action"
                );

            if (!button)
                return;

            button.disabled = true;

            try {

                await changeState(
                    button.dataset.order,
                    button.dataset.state
                );

                await refreshOrders();

            } catch (error) {

                alert(
                    "No fue posible " +
                    "actualizar el pedido."
                );

            } finally {

                button.disabled =
                    false;
            }
        }
    );


    document
        .getElementById(
            "kds-refresh"
        )
        .addEventListener(
            "click",
            refreshOrders
        );


    document
        .getElementById(
            "kds-fullscreen"
        )
        .addEventListener(
            "click",
            async () => {

                try {

                    if (
                        !document
                            .fullscreenElement
                    ) {

                        await document
                            .documentElement
                            .requestFullscreen();

                    } else {

                        await document
                            .exitFullscreen();
                    }

                } catch (e) {

                    console.error(e);
                }
            }
        );


    async function loadHistory() {

        const response =
            await fetch(
                "/ibloom/kitchen/history",
                {
                    cache: "no-store",
                }
            );

        const data =
            await response.json();

        const container =
            document.getElementById(
                "kds-history-list"
            );

        container.innerHTML = "";

        if (
            !data.orders ||
            !data.orders.length
        ) {

            container.innerHTML =
                "<p>No hay pedidos entregados.</p>";

            return;
        }

        data.orders.forEach(
            order => {

                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "kds-history-item";

                row.innerHTML = `
                    <strong>
                        ${order.name}
                    </strong>

                    · ${order.time}

                    <br/>

                    ${
                        order.products
                            .map(
                                p =>
                                `${p.qty}× ${p.name}`
                            )
                            .join(", ")
                    }
                `;

                container.appendChild(
                    row
                );
            }
        );
    }


    document
        .getElementById(
            "kds-history"
        )
        .addEventListener(
            "click",
            async () => {

                await loadHistory();

                document
                    .getElementById(
                        "kds-history-modal"
                    )
                    .classList.add(
                        "open"
                    );
            }
        );


    document
        .getElementById(
            "kds-history-close"
        )
        .addEventListener(
            "click",
            () => {

                document
                    .getElementById(
                        "kds-history-modal"
                    )
                    .classList.remove(
                        "open"
                    );
            }
        );


    function clock() {

        const node =
            document.getElementById(
                "kds-clock"
            );

        node.textContent =
            new Date()
                .toLocaleTimeString(
                    "es-CR",
                    {
                        hour:
                            "2-digit",
                        minute:
                            "2-digit",
                    }
                );
    }


    clock();
    refreshOrders();

    setInterval(
        clock,
        1000
    );

    setInterval(
        refreshOrders,
        3000
    );

});
