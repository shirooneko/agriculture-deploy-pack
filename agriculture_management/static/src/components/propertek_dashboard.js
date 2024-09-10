/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState } = owl;

export class AgricultureManagementDashboard extends Component {
  setup() {
    this.state = useState({
      harvestPerPeriod: { labels: [], datasets: [] },
      harvestPerProject: { labels: [], datasets: [] }, // Tambahkan state untuk hasil panen per musim

    });

    this.orm = useService("orm");
    this.actionService = useService("action");

    onWillStart(async () => {
      await this.getHarvestPerPeriod();
      await this.getHarvestDataPerProject();
    });
  }

  // Fungsi untuk mendapatkan hasil panen per periode
  async getHarvestPerPeriod() {
    try {
      const data = await this.orm.readGroup(
        "crop.harvest", // Model hasil panen
        [], // Domain bisa dikosongkan jika tidak ada filter
        ["date", "quantity"], // Fields untuk dibaca
        ["date"], // Group by field "date" dalam bentuk list
        { orderby: "date", lazy: false } // Urutkan berdasarkan "date"
      );

      const colors = [
        "#FF6384",
        "#36A2EB",
        "#FFCE56",
        "#4BC0C0",
        "#9966FF",
        "#FF9F40",
        "#C7C7C7",
        "#5376FF",
        "#FF63FF",
        "#63FF84",
      ];

      this.state.harvestPerPeriod = {
        data: {
          labels: data.map((d) => d.date),
          datasets: [
            {
              label: "Quantity",
              data: data.map((d) => d.quantity),
              backgroundColor: colors.slice(0, data.length),
              borderColor: "blue",
              borderWidth: 1,
              hoverOffset: 4,
            },
          ],
        },
        label_field: "date",
      };
    } catch (error) {
      console.error("Error fetching harvest data:", error);
    }
  }
  
  async getHarvestDataPerProject() {
    try {
        // Ambil data dari model 'project.project' dan group berdasarkan nama proyek
        const data = await this.orm.readGroup(
            "project.project", // Model proyek
            [], // Domain bisa dikosongkan jika tidak ada filter
            ["name", "total_harvest_quantity"], // Fields untuk dibaca
            ["name"], // Group by field "name"
            { orderby: "name", lazy: false } // Urutkan berdasarkan "name"
        );

        const colors = [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
            "#C7C7C7",
            "#5376FF",
            "#FF63FF",
            "#63FF84",
        ];

        this.state.harvestPerProject = {
            data: {
                labels: data.map((d) => d.name), // Ambil nama proyek dari 'name'
                datasets: [
                    {
                        label: "Total Harvest Quantity",
                        data: data.map((d) => d.total_harvest_quantity),
                        backgroundColor: colors.slice(0, data.length),
                        borderColor: "blue",
                        borderWidth: 1,
                        hoverOffset: 4,
                    },
                ],
            },
            label_field: "name",
        };
    } catch (error) {
        console.error("Error fetching harvest data per project:", error);
    }
}

}

AgricultureManagementDashboard.template =
  "agriculture_management.DashboardTemplate";
AgricultureManagementDashboard.components = { KpiCard, ChartRenderer };

registry
  .category("actions")
  .add(
    "agriculture_management.dashboard_action",
    AgricultureManagementDashboard
  );
