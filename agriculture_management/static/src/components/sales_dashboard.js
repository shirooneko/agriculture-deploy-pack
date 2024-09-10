/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState } = owl;

export class SalesDashboard extends Component {
    setup() {
        this.state = useState({
            period: 90,
            quotations: { value: 0, percentage: 0 },
            orders: { value: 0, percentage: 0, revenue: 0, revenue_percentage: 0, average: 0, average_percentage: 0 },
            topProducts: { labels: [], datasets: [] },
            topSalesPeople: { labels: [], datasets: [] },
            topMonthlySales: { labels: [], datasets: [] },
            partnerOrders: { labels: [], datasets: [] },
        });

        this.orm = useService("orm");
        this.actionService = useService("action");

        onWillStart(async () => {
            this.getDates();
            await this.getQuotations();
            await this.getOrders();
            await this.getTopProducts();
            await this.getTopSalesPeople();
            await this.getTopMonthlySales();
            await this.getPartnerOrders();
        });
    }

    getDates() {
        let currentDate = new Date();
        currentDate.setDate(currentDate.getDate() - this.state.period);
        this.state.current_date = currentDate.toISOString().split("T")[0];

        let previousDate = new Date();
        previousDate.setDate(previousDate.getDate() - this.state.period * 2);
        this.state.previous_date = previousDate.toISOString().split("T")[0];
    }

    async getQuotations() {
        let domain = [["state", "in", ["sent", "draft"]]];
        if (this.state.period > 0) {
            domain.push(["date_order", ">", this.state.current_date]);
        }
        const data = await this.orm.searchCount("sale.order", domain);
        this.state.quotations.value = data;

        let prev_domain = [["state", "in", ["sent", "draft"]]];
        if (this.state.period > 0) {
            prev_domain.push(
                ["date_order", ">", this.state.previous_date],
                ["date_order", "<=", this.state.current_date]
            );
        }
        const prev_data = await this.orm.searchCount("sale.order", prev_domain);
        const percentage = ((data - prev_data) / prev_data) * 100;
        this.state.quotations.percentage = percentage.toFixed(2);
    }

    async getOrders() {
        let domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date_order", ">", this.state.current_date]);
        }
        const data = await this.orm.searchCount("sale.order", domain);

        let prev_domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            prev_domain.push(
                ["date_order", ">", this.state.previous_date],
                ["date_order", "<=", this.state.current_date]
            );
        }
        const prev_data = await this.orm.searchCount("sale.order", prev_domain);
        const percentage = ((data - prev_data) / prev_data) * 100;

        const current_revenue = await this.orm.readGroup(
            "sale.order",
            domain,
            ["amount_total:sum"],
            []
        );
        const prev_revenue = await this.orm.readGroup(
            "sale.order",
            prev_domain,
            ["amount_total:sum"],
            []
        );
        const revenue_percentage =
            ((current_revenue[0].amount_total - prev_revenue[0].amount_total) /
                prev_revenue[0].amount_total) *
            100;

        const current_average = await this.orm.readGroup(
            "sale.order",
            domain,
            ["amount_total:avg"],
            []
        );
        const prev_average = await this.orm.readGroup(
            "sale.order",
            prev_domain,
            ["amount_total:avg"],
            []
        );
        const average_percentage =
            ((current_average[0].amount_total - prev_average[0].amount_total) /
                prev_average[0].amount_total) *
            100;

        // Ubah simbol mata uang ke Rupiah
        this.state.orders = {
            value: data,
            percentage: percentage.toFixed(2),
            revenue: `Rp ${(current_revenue[0].amount_total / 1000).toFixed(2)}K`,
            revenue_percentage: revenue_percentage.toFixed(2),
            average: `Rp ${(current_average[0].amount_total / 1000).toFixed(2)}K`,
            average_percentage: average_percentage.toFixed(2),
        };
    }

    async getTopProducts() {
        let domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date", ">", this.state.current_date]);
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["product_id", "price_total"],
            ["product_id"],
            { limit: 5, orderby: "price_total desc" }
        );

        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#C7C7C7", "#5376FF", "#FF63FF", "#63FF84",
        ];

        this.state.topProducts = {
            data: {
                labels: data.map((d) => d.product_id[1]),
                datasets: [
                    {
                        label: "Total",
                        data: data.map((d) => d.price_total),
                        hoverOffset: 4,
                        backgroundColor: colors.slice(0, data.length),
                    },
                    {
                        label: "Count",
                        data: data.map((d) => d.product_id_count),
                        hoverOffset: 4,
                        backgroundColor: colors.slice(0, data.length),
                    },
                ],
            },
            domain,
            label_field: "product_id",
        };
    }

    async getTopSalesPeople() {
        let domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date", ">", this.state.current_date]);
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["user_id", "price_total"],
            ["user_id"],
            { limit: 5, orderby: "price_total desc" }
        );

        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#C7C7C7", "#5376FF", "#FF63FF", "#63FF84",
        ];

        this.state.topSalesPeople = {
            data: {
                labels: data.map((d) => d.user_id[1]),
                datasets: [
                    {
                        label: "Total",
                        data: data.map((d) => d.price_total),
                        hoverOffset: 4,
                        backgroundColor: colors.slice(0, data.length),
                    },
                ],
            },
            domain,
            label_field: 'user_id',
        };
    }

    async getTopMonthlySales() {
        let domain = [["state", "in", ["draft", "sent", "sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date", ">", this.state.current_date]);
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["date", "state", "price_total"],
            ["date", "state"],
            { orderby: "date", lazy: false }
        );

        const labels = [... new Set(data.map(d => d.date))];
        const quotations = data.filter(d => d.state == 'draft' || d.state == 'sent');
        const orders = data.filter(d => ['sale', 'done'].includes(d.state));

        this.state.topMonthlySales = {
            data: {
                labels,
                datasets: [
                    {
                        label: "Quotations",
                        data: labels.map(l => quotations.filter(q => l == q.date).map(j => j.price_total).reduce((a, c) => a + c, 0)),
                        hoverOffset: 4,
                        backgroundColor: "aqua",
                    },
                    {
                        label: "Orders",
                        data: labels.map(l => orders.filter(q => l == q.date).map(j => j.price_total).reduce((a, c) => a + c, 0)),
                        hoverOffset: 4,
                        backgroundColor: "red",
                    },
                ],
            },
            domain,
            label_field: 'date',
        };
    }

    async getPartnerOrders() {
        let domain = [["state", "in", ["draft", "sent", "sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date", ">", this.state.current_date]);
        }

        const data = await this.orm.readGroup(
            "sale.report",
            domain,
            ["partner_id", "price_total", "product_uom_qty"],
            ["partner_id"],
            { orderby: "partner_id", lazy: false }
        );

        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#C7C7C7", "#5376FF", "#FF63FF", "#63FF84",
        ];

        this.state.partnerOrders = {
            data: {
                labels: data.map((d) => d.partner_id[1]),
                datasets: [
                    {
                        label: "Total Amount",
                        data: data.map((d) => d.price_total),
                        hoverOffset: 4,
                        backgroundColor: "aqua",
                        yAxisID: "Total",
                        order: 1,
                    },
                    {
                        label: "Ordered Qty",
                        data: data.map((d) => d.product_uom_qty),
                        hoverOffset: 4,
                        backgroundColor: "red",
                        type: "line",
                        borderColor: "blue",
                        yAxisID: "Qty",
                        order: 0,
                    },
                ],
            },
            scales: {
                Qty: {
                    position: "right",
                },
            },
            domain,
            label_field: 'partner_id',
        };
    }

    async onChangePeriod() {
        try {
            this.getDates();
            await this.getQuotations();
            await this.getOrders();
            await this.getTopProducts();
            await this.getTopSalesPeople();
            await this.getTopMonthlySales();
            await this.getPartnerOrders();
        } catch (error) {
            console.error("Error changing period: ", error);
        }
    }

    viewQuotations() {
        let domain = [["state", "in", ["sent", "draft"]]];
        if (this.state.period > 0) {
            domain.push(["date_order", ">", this.state.current_date]);
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "sale.order",
            domain,
            views: [[false, "list"], [false, "form"]],
        });
    }

    viewOrders() {
        let domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date_order", ">", this.state.current_date]);
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Orders",
            res_model: "sale.order",
            domain,
            context: { group_by: ["date_order"] },
            views: [[false, "list"], [false, "form"]],
        });
    }

    viewRevenues() {
        let domain = [["state", "in", ["sale", "done"]]];
        if (this.state.period > 0) {
            domain.push(["date_order", ">", this.state.current_date]);
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Revenues",
            res_model: "sale.order",
            domain,
            context: { group_by: ["date_order"] },
            views: [[false, "pivot"], [false, "form"]],
        });
    }
}

SalesDashboard.template = "agriculture_management.SalesDashboard";
SalesDashboard.components = { KpiCard, ChartRenderer };

registry.category("actions").add("agriculture_management.sales_dashboard_action", SalesDashboard);
