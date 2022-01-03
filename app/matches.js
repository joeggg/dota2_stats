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
                    <div className="PlayerData">
                        <img
                            src={player.avatar}
                            alt="avatar"
                            className="avatar"
                        />
                        <span className="PlayerName">
                            {player.name} <br></br>
                            <h4 className="PlayerDetails">
                                Member since {player.created_at}
                            </h4>
                        </span>
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
                            <td className="MatchesRow">
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.hero}
                                </Link>
                            </td>
                            <td
                                className="MatchesRow"
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
                            <td className="MatchesRow">
                                <Link
                                    to={`match/${match.match_id}`}
                                    className="MatchLink"
                                >
                                    {match.length}
                                </Link>
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
            <br />
            <p className="MatchTitle">
                Matches
                <br />
            </p>
            {matchList}
        </div>
    );
}

export default Matches;
