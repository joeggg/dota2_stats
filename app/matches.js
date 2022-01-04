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
                    <div>
                        <div className="PlayerData">
                            <img
                                src={player.avatar}
                                alt="avatar"
                                className="avatar"
                            />
                            <span className="PlayerName">
                                {player.name} <br></br>
                            </span>
                        </div>
                        <h4 className="PlayerDetails">
                            Member since {player.created_at}
                        </h4>
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
                const matchListBody = matches.map((matchData) => {
                    const match = matchData.match;
                    const player = matchData.player;
                    const total = player.kills + player.deaths + player.assists;
                    return (
                        <tr key={match.match_id}>
                            <td className="MatchesRow">
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {player.hero}
                                </Link>
                            </td>
                            <td
                                className="MatchesRow"
                                style={{
                                    color:
                                        player.result === 'won'
                                            ? 'darkgreen'
                                            : 'darkred',
                                }}
                            >
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {player.result}
                                </Link>
                            </td>
                            <td className="MatchesRow">
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.length}
                                </Link>
                            </td>
                            <td className="MatchesRow">
                                <div className="KDA">
                                    <div
                                        className="Bar"
                                        id="Kills"
                                        style={{
                                            width: `${
                                                (100 * player.kills) / total
                                            }%`,
                                        }}
                                    >
                                        <p className="KDAStat">
                                            {player.kills}
                                        </p>
                                    </div>
                                    <div
                                        className="Bar"
                                        id="Deaths"
                                        style={{
                                            width: `${
                                                (100 * player.deaths) / total
                                            }%`,
                                        }}
                                    >
                                        <p className="KDAStat">
                                            {player.deaths}
                                        </p>
                                    </div>
                                    <div
                                        className="Bar"
                                        id="Assists"
                                        style={{
                                            width: `${
                                                (100 * player.assists) / total
                                            }%`,
                                        }}
                                    >
                                        <p className="KDAStat">
                                            {player.assists}
                                        </p>
                                    </div>
                                </div>
                            </td>
                            <td className="MatchesRow">
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
                                    <th className="MatchesHeader">Hero</th>
                                    <th className="MatchesHeader">Result</th>
                                    <th className="MatchesHeader">Duration</th>
                                    <th className="MatchesHeader">K D A</th>
                                    <th className="MatchesHeader">Time</th>
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
            <br />
            {playerSummary}
            <p className="MatchesTitle">
                Matches
                <br />
            </p>
            {matchList}
        </div>
    );
}

export default Matches;
