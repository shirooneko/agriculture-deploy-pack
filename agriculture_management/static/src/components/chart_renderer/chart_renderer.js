/** @odoo-module **/

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart, useRef, onMounted, onWillUnmount } = owl;
import { useService } from "@web/core/utils/hooks";

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef('chart');
        this.actionService = useService('action');
        
        // Load Chart.js library
        onWillStart(async () => {
            await loadJS('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js');
        });
        
        // Use onMounted to render chart after component is mounted
        onMounted(() => {
            this.renderChart();
        });

        // Clean up chart on unmount
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.props.config && this.props.config.data) {
            if (this.chart) {
                this.chart.destroy();
            }
            this.chart = new Chart(this.chartRef.el, {
                type: this.props.type,
                data: this.props.config.data,
                options: {
                    onClick: (e) => {
                        const active = e.chart.getActiveElements();
                        if (active.length > 0) {
                            const label = e.chart.data.labels[active[0].index];
                            const dataset = e.chart.data.datasets[active[0].datasetIndex].label;

                            const { label_field, domain } = this.props.config;
                            let new_domain = domain ? domain : [];

                            if (label_field) {
                                if (label_field.includes('date')) {
                                    const selected_month = new Date(label);
                                    const month_start = new Date(selected_month.getFullYear(), selected_month.getMonth(), 1)
                                        .toISOString().split('T')[0];
                                    const month_end = new Date(selected_month.getFullYear(), selected_month.getMonth() + 1, 0)
                                        .toISOString().split('T')[0];
                                    new_domain.push(
                                        ['date', '>=', month_start],
                                        ['date', '<=', month_end]
                                    );
                                } else {
                                    new_domain.push([label_field, '=', label]);
                                }
                            }

                            if (dataset === 'Quotations') {
                                new_domain.push(['state', 'in', ['draft', 'sent']]);
                            }

                            if (dataset === 'Orders') {
                                new_domain.push(['state', 'in', ['sale', 'done']]);
                            }

                            this.actionService.doAction({
                                type: 'ir.actions.act_window',
                                name: this.props.title,
                                res_model: 'sale.report',
                                domain: new_domain,
                                views: [
                                    [false, 'list'],
                                    [false, 'form'],
                                ],
                            });

                            console.log(label);
                        } else {
                            console.log('Tidak ada elemen aktif yang diklik');
                        }
                    },
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: this.props.title,
                            position: 'bottom',
                        },
                    },
                    scales: this.props.config.scales || {},
                },
            });
        }
    }
}

ChartRenderer.template = 'agriculture_management.ChartRendererTemplate';
