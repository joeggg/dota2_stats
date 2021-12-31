import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function MatchList() {
    const params = useParams();
    const [matchData, setMatches] = useState([]);
    const [playerData, setPlayer] = useState([]);

    const accountId = params.accountId;
    const url = 'http://94.11.9.194:5656';
    // const ip = 'http://127.0.0.1:5656';

    /**
     *  Player info effect
     */
    useEffect(() => {
        fetch(`${url}/player/${accountId}`).then((res) => {
            res.text().then((text) => {
                const player = JSON.parse(text).results;
                setPlayer(
                    <div className="playerData">
                        <img
                            src={player.avatar}
                            alt="avatar"
                            className="avatar"
                        />
                        <p>{player.name}</p>
                        <h4>Member since {player.created_at}</h4>
                    </div>
                );
            });
        });
    }, []);

    /**
     *  Match list effect
     */
    useEffect(() => {
        fetch(`${url}/matches/${accountId}`).then((res) => {
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
            {playerData}
            <p className="matches_title">
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
