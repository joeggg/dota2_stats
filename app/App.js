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
                        <h5 key={match.match_id}>
                            {match.hero} | {match.result} | {match.length} |{' '}
                            {match.start_time}
                        </h5>
                    );
                });
                setMatches(<div>{data}</div>);
                console.log(matches);
            });
        });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <p>
                    Dota stuff goes here <br></br>
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
