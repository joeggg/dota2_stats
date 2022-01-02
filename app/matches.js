import { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { useParams } from 'react-router-dom';

function Matches() {
    const params = useParams();
    const [playerSummary, setPlayerSummary] = useState(<div></div>);
    const [, setMatchList] = useState(<div></div>);
    const [matchScoreboard, setMatchScoreboard] = useState(<div></div>);
    const [currentDisplay, setCurrentDisplay] = useState(<div></div>);

    const accountId = params.accountId;
    const url = 'http://94.11.9.194:5656';
    // const ip = 'http://127.0.0.1:5656';

    /**
     *  Switching panel effect
     */
    useEffect(() => {
        ReactDOM.render(
            currentDisplay,
            document.getElementById('currentDisplay')
        );
    });

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
                                <button
                                    className="linkButton"
                                    onClick={() => {
                                        setCurrentDisplay(matchScoreboard);
                                    }}
                                >
                                    {match.hero}
                                </button>
                            </td>
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
                // Add the table headings
                const matchListData = (
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
                // Create the scoreboard element
                const matchScoreboardData = (
                    <table cellSpacing={0} className="MatchData">
                        Match scoreboard here {getMatchScoreboard(matches[0])}
                    </table>
                );
                // Set the match list/scoreboard state and current display defaults to match list
                setMatchList(matchListData);
                setMatchScoreboard(matchScoreboardData);
                setCurrentDisplay(matchListData);
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
            <div id="currentDisplay"></div>
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

/**
 *  Takes a match data object and returns the scoreboard as a
 *  JSX element
 *
 * @param {Object} match
 * @returns {JSX.Element}
 */
function getMatchScoreboard(match) {
    return <div></div>;
}

export default Matches;
