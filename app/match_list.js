import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function MatchList() {
    const params = useParams();
    const [matchData, setMatches] = useState([]);
    const accountId = params.accountId;
    const ip = '94.11.9.194';
    // const ip = '127.0.0.1';

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
                    <table cellSpacing={0} className="MatchData">
                        <thead>
                            <tr key="labels">
                                <th>Hero</th>
                                <th>Result</th>
                                <th>Duration</th>
                                <th>Time</th>
                            </tr>
                        </thead>
                        <tbody>{data}</tbody>
                    </table>
                );
            });
        });
    }, []);

    return (
        <div className="Page">
            <p>
                Matches:
                <br />
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
        </div>
    );
}

export default MatchList;
