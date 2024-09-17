/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState, onWillUnmount } = owl;

export class IoTDashboard extends Component {
    setup() {
        this.state = useState({
            iotData: { labels: [], datasets: [] },
            dataPoints: [], // Array untuk menyimpan data WebSocket
        });

        this.actionService = useService("action");

        onWillStart(() => {
            this.initWebSocket();
        });

        onWillUnmount(() => {
            this.closeWebSocket();
        });
    }

    initWebSocket() {
        this.ws = new WebSocket('ws://localhost:6789');

        this.ws.onopen = () => {
            console.log('WebSocket connection established');
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received WebSocket data:', data);  // Debug log
            this.addDataPoint(data);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket connection closed');
        };
    }

    closeWebSocket() {
        if (this.ws) {
            this.ws.close();
        }
    }

    addDataPoint(newData) {
        const oneDayInMs = 24 * 60 * 60 * 1000; // 1 hari dalam milidetik
        const now = Date.now(); // Waktu saat ini dalam milidetik
    
        // Tambahkan data baru ke array dataPoints
        this.state.dataPoints.push(newData);
    
        // Filter dataPoints untuk hanya menyimpan data dari 1 hari terakhir
        this.state.dataPoints = this.state.dataPoints.filter(data => {
            const dataTimestamp = new Date(data.timestamp).getTime();
            return (now - dataTimestamp) <= oneDayInMs;
        });
    
        // Update data chart setelah filter
        this.updateChartData();
    }
    
    

    updateChartData() {
        console.log('Updating chart with new data:', this.state.dataPoints);  // Debug log
    
        const updatedData = {
            data: {
                labels: this.state.dataPoints.map(data => data.timestamp),
                datasets: [
                    {
                        label: "Suhu",
                        data: this.state.dataPoints.map(data => data.suhu),
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                        tension: 0.1,
                        // Disable animation
                        animation: {
                            duration: 0, // Set duration to 0 to disable animation
                        }
                    },
                ],
            },
            label_field: "timestamp",
        };
    
        console.log('Updated iotData:', updatedData);  // Debug log
    
        this.state.iotData = updatedData;
    }    
}

IoTDashboard.template = "agriculture_management.IoTDashboardTemplate";
IoTDashboard.components = { ChartRenderer };

registry
    .category("actions")
    .add("agriculture_management.iot_dashboard_action", IoTDashboard);
