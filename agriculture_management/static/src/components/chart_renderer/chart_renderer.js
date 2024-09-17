/** @odoo-module **/

import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets";
const { Component, onWillStart, useRef, onMounted, onWillUnmount, onPatched } = owl;

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef('chart');
        this.chart = null;

        onWillStart(async () => {
            await loadJS('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js');
        });

        onMounted(() => {
            console.log('ChartRenderer mounted. Props:', this.props);
            this.renderChart();
        });

        onPatched(() => {
            console.log('ChartRenderer patched. New props:', this.props);
            this.updateChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        console.log('Rendering chart with config:', this.props.config);
        if (this.props.config && this.props.config.data) {
            if (this.chart) {
                this.chart.destroy();
            }
            this.chart = new Chart(this.chartRef.el, {
                type: this.props.type,
                data: this.props.config.data,
                options: {
                    responsive: true,
                    animation: {
                        radius: {
                            duration: 400,
                            easing: 'linear',
                            loop: (context) => context.active
                        }
                    },
                    hoverRadius: 12,
                    hoverBackgroundColor: 'yellow',
                    interaction: {
                        mode: 'nearest',
                        intersect: false,
                        axis: 'x'
                    },
                    plugins: {
                        tooltip: {
                            enabled: false
                        }
                    },
                    scales: this.props.config.scales || {},
                },
            });
        } else {
            console.error('Invalid chart configuration:', this.props.config);
        }
    }

    updateChart() {
        console.log('Updating chart with new data:', this.props.config);
        if (this.chart && this.props.config && this.props.config.data) {
            this.chart.data = this.props.config.data;
            this.chart.update();
        }
    }
}

ChartRenderer.props = {
    type: String,
    title: String,
    config: Object,
};

ChartRenderer.template = 'agriculture_management.ChartRendererTemplate';
