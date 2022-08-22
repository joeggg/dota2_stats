import * as React from 'react'
import { Link, useParams } from 'react-router-dom';

import { url } from './consts'
import ParseResults from './parseResults';

interface Match {
    players: any[],
    winner: string
}

function Scoreboard(): React.ReactElement {
    const params = useParams();
    const [matchData, setMatchData] = React.useState({} as Match);
    const [matchScoreboard, setMatchScoreboard] = React.useState(<div></div>);
    const [parseResults, setParseResults] = React.useState(<div></div>);

    const accountId: string = params.accountId!;
    const matchId: string = params.matchId!;

    /**
     *  Match scoreboard effect
     */
    React.useEffect(() => {
        fetch(`${url}/match/${matchId}?account_id=${accountId}`).then((res) => {
            res.text().then((text) => {
                const matchObj = JSON.parse(text);
                const match: Match = matchObj!.match;
                // const PlayerDetails = matchObj.player;
                // Create the scoreboard element
                const scoreboard = match.players.map((player: any) => {
                    const name = 'ScoreRow';
                    let colour: string;
                    let id = player.id;
                    if (player.slot === 5 || player.slot === 0) {
                        id = 'GapRow';
                    }
                    if (player.slot < 5) {
                        colour = 'darkgreen';
                    } else {
                        colour = 'darkred';
                    }
                    return (
                        <tr key={player.id}>
                            <td
                                className={name}
                                id={id}
                                style={{ color: colour }}
                            >
                                {player.hero}
                            </td>
                            <td className={name} id={id}>
                                {player.level}
                            </td>
                            <td className={name} id={id}>
                                {player.kills}
                            </td>
                            <td className={name} id={id}>
                                {player.deaths}
                            </td>
                            <td className={name} id={id}>
                                {player.assists}
                            </td>
                            <td className={name} id={id}>
                                {player.net_worth}
                            </td>
                            <td className={name} id={id}>
                                {player.gpm}
                            </td>
                            <td className={name} id={id}>
                                {player.xpm}
                            </td>
                            <td className={name} id={id}>
                                {player.hero_damage}
                            </td>
                            <td className={name} id={id}>
                                {player.tower_damage}
                            </td>
                            <td className={name} id={id}>
                                {player.healing}
                            </td>
                        </tr>
                    );
                });
                // Set the match scoreboard state and current display defaults to match list
                setMatchData(match);
                setMatchScoreboard(
                    <table cellSpacing={0} className="Matchdata">
                        <thead>
                            <tr>
                                <th className="ScoreHeader">Hero</th>
                                <th className="ScoreHeader">Level</th>
                                <th className="ScoreHeader">Kills</th>
                                <th className="ScoreHeader">Deaths</th>
                                <th className="ScoreHeader">Assists</th>
                                <th className="ScoreHeader">Net worth</th>
                                <th className="ScoreHeader">GPM</th>
                                <th className="ScoreHeader">XPM</th>
                                <th className="ScoreHeader">Hero damage</th>
                                <th className="ScoreHeader">Tower damage</th>
                                <th className="ScoreHeader">Hero healing</th>
                            </tr>
                        </thead>
                        <tbody>{scoreboard}</tbody>
                    </table>
                );
            });
        });
    }, []);

    /**
     * Parser results
     */
    React.useEffect(() => {
        fetch(`${url}/match/${matchId}/parse`).then(res => res.json().then(data => {
            if (data.status === "complete") {
                setParseResults(ParseResults(data.result))
            } else {
                setParseResults(<div><p className="MidText">No parse results yet</p> </div >)
            }
        }));
    }, []);

    const onParse = () => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        };
        fetch(`${url}/match/${matchId}/parse`, requestOptions)
            .then(res => res.json());
    };

    return (
        <div className="Page">
            <div className='ButtonContainer'>
                <button className="Button" id="Back">
                    <Link to={`/players/${accountId}`}>
                        <p className='ButtonText'>Back to matches</p>
                    </Link>
                </button>
                <button className="Button" id='Parse' onClick={onParse} style={{ width: "150px" }}>
                    <Link to={`/parse?id=${matchId}`}>
                        <p className='ButtonText' >Parse replay</p>
                    </Link>
                </button>
            </div>
            <p className="MatchesTitle">Match scoreboard:</p>
            <p
                className="ResultsTitle"
                style={{
                    color: matchData.winner === 'Radiant' ? 'green' : 'red',
                }}
            >
                {matchData.winner} win!
            </p>
            {matchScoreboard}
            {parseResults}
        </div >
    );
}

export default Scoreboard;
