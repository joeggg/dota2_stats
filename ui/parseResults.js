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
import { Line } from 'react-chartjs-2';


ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function ParseResults(result) {
    const radiant = result.Metadata.Radiant;
    const dire = result.Metadata.Dire;
    if (radiant === null || dire === null) {
        return <p className='MidText' >No metadata for some reason :(</p>
    }
    const size = radiant.NetWorthGraph.length;
    const xAxis = Array.from(Array(size), (_, i) => i + 1)
    const networth = Array.from(
        Array(size), (_, i) => radiant.NetWorthGraph[i] - dire.NetWorthGraph[i]
    );
    const xp = Array.from(
        Array(size), (_, i) => radiant.XPGraph[i] - dire.XPGraph[i]
    );
    const options = {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: "Advantage graph",
            },
        },
    };
    const data = {
        labels: xAxis,
        datasets: [
            {
                label: "Net worth advantage",
                data: networth,
                borderColor: "rgb(255, 216, 107)",
                backgroundColor: 'rgba(255, 216, 107, 0.5)',
            },
            {
                label: "XP advantage",
                data: xp,
                borderColor: "rgb(99, 255, 198)",
                backgroundColor: 'rgba(76, 207, 160, 0.5)',
            },
        ]
    };

    return <div>
        <Line data={data} width={"1000px"} height={"500px"} options={options} className="ParsedGraph" />
    </div>;
}

export default ParseResults;
