import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

function Matches() {
    const params = useParams();
    const [playerSummary, setPlayerSummary] = useState(<div></div>);
    const [matchList, setMatchList] = useState(<div></div>);

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
                setPlayerSummary(
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
                // Create the match history element
                const matchListBody = matches.map((match) => {
                    return (
                        <tr key={match.match_id}>
                            <td>
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.hero}
                                </Link>
                            </td>
                            <td
                                style={{
                                    color:
                                        match.result === 'won'
                                            ? 'darkgreen'
                                            : 'darkred',
                                }}
                            >
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.result}
                                </Link>
                            </td>
                            <td>
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.length}
                                </Link>
                            </td>
                            <td>
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.start_time}
                                </Link>
                            </td>
                        </tr>
                    );
                });
                // Add the table headings and set the state
                setMatchList(
                    <div>
                        <table cellSpacing={0} className="MatchList">
                            <thead>
                                <tr key="labels">
                                    <th>Hero</th>
                                    <th>Result</th>
                                    <th>Duration</th>
                                    <th>Time</th>
                                </tr>
                            </thead>
                            <tbody>{matchListBody}</tbody>
                        </table>
                    </div>
                );
            });
        });
    }, []);

    return (
        <div className="Page">
            {playerSummary}
            <p className="matches_title">
                Matches:
                <br />
            </p>
            {matchList}
        </div>
    );
}

export default Matches;
