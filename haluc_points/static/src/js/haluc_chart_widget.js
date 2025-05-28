/* filepath: x:\_DEV\odoo-haluc-pontok\haluc_points\static\src\js\haluc_chart_widget.js */
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillUpdateProps, onMounted, onWillUnmount, useRef } = owl;

export class HalucChartWidget extends Component {
    static template = "haluc_points.HalucChartWidget";
    static props = {
        ...CharField.props,
        value: { type: String, optional: true },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onMounted(this.renderChart.bind(this));
        onWillUpdateProps(this.renderChart.bind(this));
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        if (!this.props.value || !this.canvasRef.el) {
            return;
        }
        try {
            const chartData = JSON.parse(this.props.value);
            if (chartData && chartData.labels && chartData.datasets) {
                this.chart = new Chart(this.canvasRef.el, {
                    type: 'line',
                    data: {
                        labels: chartData.labels,
                        datasets: chartData.datasets.map(ds => ({
                            label: ds.label,
                            data: ds.data,
                            borderColor: ds.borderColor,
                            backgroundColor: ds.backgroundColor,
                            fill: ds.fill,
                            tension: 0.1
                        }))
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        } catch (e) {
            console.error("Error parsing chart data or rendering chart:", e);
        }
    }
}

registry.category("fields").add("haluc_chart_widget", HalucChartWidget);
