import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

function Scoreboard() {
    const params = useParams();
    const [matchScoreboard, setMatchScoreboard] = useState(<div></div>);

    const accountId = params.accountId;
    const matchId = params.matchId;
    const url = 'http://94.11.9.194:5656';
    // const ip = 'http://127.0.0.1:5656';

    /**
     *  Match scoreboard effect
     */
    useEffect(() => {
        fetch(`${url}/match/${matchId}?id=${accountId}`).then((res) => {
            res.text().then((text) => {
                const match = JSON.parse(text).results;
                // Create the scoreboard element
                const scoreboard = Object.entries(match.players).map(
                    ([id, player]) => {
                        return (
                            <tr key={id}>
                                <td>{player.hero}</td>
                                <td>{player.level}</td>
                                <td>{player.kills}</td>
                                <td>{player.deaths}</td>
                                <td>{player.assists}</td>
                                <td>{player.net_worth}</td>
                                <td>{player.gpm}</td>
                                <td>{player.xpm}</td>
                                <td>{player.hero_damage}</td>
                                <td>{player.tower_damage}</td>
                                <td>{player.healing}</td>
                            </tr>
                        );
                    }
                );
                // Set the match scoreboard state and current display defaults to match list
                setMatchScoreboard(
                    <table cellSpacing={0} className="MatchData">
                        <thead className="ScoreboardHeader">
                            <tr>
                                <th>Hero</th>
                                <th>Level</th>
                                <th>Kills</th>
                                <th>Deaths</th>
                                <th>Assists</th>
                                <th>Net worth</th>
                                <th>GPM</th>
                                <th>XPM</th>
                                <th>Hero damage</th>
                                <th>Tower damage</th>
                                <th>Hero healing</th>
                            </tr>
                        </thead>
                        <tbody>{scoreboard}</tbody>
                    </table>
                );
            });
        });
    }, []);

    return (
        <div className="Page">
            <button className="BackButton">
                <Link to={`/players/${accountId}`}>Back to matches</Link>
            </button>
            <p className="matches_title">
                Match scoreboard:
                <br />
            </p>
            {matchScoreboard}
        </div>
    );
}

export default Scoreboard;
