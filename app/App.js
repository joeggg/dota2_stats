import { useEffect, useState } from 'react';
import logo from './dota2.svg';
import './App.css';

function App() {
    const [matchData, setMatches] = useState([]);
    const accountId = 54269634;
    // const ip = '94.11.9.194';
    const ip = '127.0.0.1';

    useEffect(() => {
        fetch(`http://${ip}:5656/matches/${accountId}`).then((res) => {
            res.text().then((text) => {
                const matches = JSON.parse(text).results;
                const data = matches.map((match) => {
                    return (
                        <tr key={match.match_id}>
                            <td>{match.hero}</td>
                            <td
                                style={{
                                    color:
                                        match.result === 'won'
                                            ? 'darkgreen'
                                            : 'darkred',
                                }}
                            >
                                {match.result}
                            </td>
                            <td>{match.length}</td>
                            <td>{match.start_time}</td>
                        </tr>
                    );
                });
                setMatches(
                    <table key="match-data">
                        <tr key="labels">
                            <th>Hero</th>
                            <th>Result</th>
                            <th>Duration</th>
                            <th>Time</th>
                        </tr>
                        {data}
                    </table>
                );
                console.log(matches);
            });
        });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Dota stuff goes here
                    <br></br>
                    <br></br>
                    Matches:
                </p>
                {matchData}
                <a
                    className="App-link"
                    href="https://dota2.com"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Dota 2 site
                </a>
            </header>
        </div>
    );
}

export default App;
