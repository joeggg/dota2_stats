import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js'
import type { ChartData, ChartOptions } from 'chart.js';
import { Line } from 'react-chartjs-2';
import * as React from 'react';


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface Metadata {
    Radiant?: Team,
    Dire?: Team
}

interface Team {
    NetWorthGraph: number[],
    XPGraph: number[],
}

function ParseResults(result: any): React.ReactElement {
    const metadata: Metadata = result.Metadata;
    const radiant = metadata.Radiant;
    const dire = metadata.Dire;
    if (radiant === undefined || dire === undefined) {
        return <p className='MidText' > No metadata for some reason : (</p>
    }
    const size = radiant.NetWorthGraph.length;
    const xAxis = Array.from(Array(size), (_, i) => i + 1)
    const networth = Array.from(
        Array(size), (_, i) => 10 * (radiant.NetWorthGraph[i] - dire.NetWorthGraph[i])
    );
    const xp = Array.from(
        Array(size), (_, i) => 10 * (radiant.XPGraph[i] - dire.XPGraph[i])
    );
    const options: ChartOptions<'line'> = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Advantage graph',
            },
        },
    };
    const data: ChartData<'line'> = {
        labels: xAxis,
        datasets: [
            {
                label: 'Net worth advantage',
                data: networth,
                borderColor: 'rgb(255, 216, 107)',
                backgroundColor: 'rgba(255, 216, 107, 0.5)',
            },
            {
                label: 'XP advantage',
                data: xp,
                borderColor: 'rgb(99, 255, 198)',
                backgroundColor: 'rgba(76, 207, 160, 0.5)',
            },
        ]
    };

    return <div className='ParsedGraph Centre'>
        <Line data={data} style={{ height: '400px' }} options={options} />
    </div>;
}

export default ParseResults;
