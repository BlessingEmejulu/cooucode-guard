/**
 * COOUCodeGuard Editorial Canvas Chart Engine
 * High-contrast, brutalist technical charts with precise monospace coordinate labels.
 */
class OfflineChart {
    constructor(canvasId, config) {
        this.canvas = typeof canvasId === 'string' ? document.getElementById(canvasId) : canvasId;
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.config = config;
        this.render();
    }

    render() {
        if (!this.ctx) return;
        const width = this.canvas.width = this.canvas.parentElement.clientWidth || 320;
        const height = this.canvas.height = this.canvas.parentElement.clientHeight || 210;
        this.ctx.clearRect(0, 0, width, height);

        const type = this.config.type || 'doughnut';
        if (type === 'doughnut') {
            this.renderDoughnut(width, height);
        } else if (type === 'bar') {
            this.renderBar(width, height);
        }
    }

    renderDoughnut(width, height) {
        const { labels, datasets } = this.config.data;
        const data = datasets[0].data;
        const colors = datasets[0].backgroundColor;
        const total = data.reduce((a, b) => a + b, 0) || 1;

        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 18;
        const innerRadius = radius * 0.65;

        let startAngle = -Math.PI / 2;

        for (let i = 0; i < data.length; i++) {
            const sliceAngle = (data[i] / total) * 2 * Math.PI;
            if (data[i] > 0) {
                this.ctx.beginPath();
                this.ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
                this.ctx.arc(centerX, centerY, innerRadius, startAngle + sliceAngle, startAngle, true);
                this.ctx.closePath();
                this.ctx.fillStyle = colors[i % colors.length];
                this.ctx.fill();

                // Crisp border separation between segments
                this.ctx.strokeStyle = '#171717';
                this.ctx.lineWidth = 1.5;
                this.ctx.stroke();
            }
            startAngle += sliceAngle;
        }

        // Center total number in monospace
        this.ctx.font = 'bold 20px "IBM Plex Mono", monospace';
        this.ctx.fillStyle = '#111111';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(total.toString(), centerX, centerY - 6);

        this.ctx.font = '700 9px "IBM Plex Mono", monospace';
        this.ctx.fillStyle = '#66645F';
        this.ctx.fillText('TOTAL_SCANS', centerX, centerY + 14);
    }

    renderBar(width, height) {
        const { labels, datasets } = this.config.data;
        const data = datasets[0].data;
        const colors = datasets[0].backgroundColor;
        const maxVal = Math.max(...data, 5);

        const padding = 30;
        const chartWidth = width - padding * 2;
        const chartHeight = height - padding * 2;
        const barWidth = Math.min(42, (chartWidth / data.length) - 18);

        // Draw horizontal grid lines with technical coordinate values
        this.ctx.strokeStyle = '#D8D4CA';
        this.ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = padding + (chartHeight / 4) * i;
            this.ctx.beginPath();
            this.ctx.moveTo(padding, y);
            this.ctx.lineTo(width - padding, y);
            this.ctx.stroke();

            const val = Math.round(maxVal - (maxVal / 4) * i);
            this.ctx.font = '9px "IBM Plex Mono", monospace';
            this.ctx.fillStyle = '#99968F';
            this.ctx.textAlign = 'right';
            this.ctx.fillText(val.toString(), padding - 6, y + 3);
        }

        // Draw Bars with 2px hard outline
        for (let i = 0; i < data.length; i++) {
            const x = padding + 16 + i * (chartWidth / data.length);
            const barH = (data[i] / maxVal) * chartHeight;
            const y = height - padding - barH;

            this.ctx.fillStyle = Array.isArray(colors) ? colors[i % colors.length] : colors;
            this.ctx.fillRect(x, y, barWidth, barH);

            this.ctx.strokeStyle = '#171717';
            this.ctx.lineWidth = 1.5;
            this.ctx.strokeRect(x, y, barWidth, barH);

            // Label
            this.ctx.font = '700 10px "IBM Plex Mono", monospace';
            this.ctx.fillStyle = '#111111';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(labels[i], x + barWidth / 2, height - padding + 16);

            // Value
            this.ctx.font = 'bold 11px "IBM Plex Mono", monospace';
            this.ctx.fillStyle = '#111111';
            this.ctx.fillText(data[i].toString(), x + barWidth / 2, y - 6);
        }
    }
}

window.Chart = OfflineChart;
